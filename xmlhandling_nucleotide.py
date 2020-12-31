from sys import stdin
import xml.etree.cElementTree as etree
import codecs
import sys

if sys.version_info < (3, 0):
    UTF8Writer = codecs.getwriter('utf8')
    sys.stdout = UTF8Writer(sys.stdout)

accessions=sys.argv[1]
outdir=sys.argv[2]
accessions=accessions.split(',') #accession.version or accession
accessiontype=sys.argv[3] #accession or accessionversion


tree=etree.parse(stdin)
root=tree.getroot()
assert root.tag=='Bioseq-set', "xml is of type %s rather than of type Bioseq-set: make sure multiple accessions are efetched" %root.tag


def mystrip(x, nonehandling='default'):
    if x!=None:
        x=x.strip()
    else:
        if nonehandling=='default':
            x='-'
        if nonehandling=='blank':
            x=''
        if nonehandling=='accession':
            sys.exit('accession text is missing from xml file')
    return x


f2=open('%s/missingaccessions.txt'%outdir,'a')
includedaccessions=[]
for seqset in root:
    for seqentry in seqset: #only iterating through outer nest - most accessions will be extracted but some may be nested within the xml
        accessionout=seqentry.find('.//Textseq-id/Textseq-id_accession')
        versionout=seqentry.find('.//Textseq-id/Textseq-id_version')
        if accessionout==None or versionout==None:
            continue
        accession=accessionout.text
        accessionversion=accessionout.text+'.'+versionout.text
        if accessiontype=='accessionversion':
            if accessionversion not in accessions:
                continue
            elif accessionversion in includedaccessions:
                continue
            else:
                includedaccessions.append(accessionversion)
        else: #accession only
            if accession not in accessions:
                continue
            elif accession in includedaccessions:
                continue
            else:
                includedaccessions.append(accession)
        
        #get seqtech, assembly method; annotation methods; biosample/bioproject/assembly accession
        seqtechs=[]
        coverages=[]
        assemblymethods=[]
        annotationpipelines=[] #there is info on pipeline (e.g ncbi prokaryotic...) and software version of this pipeline e.g. 4.6
        annotationversions=[] #e.g. 4.6
        annotationmethods=[] #e.g. "Best-placed reference protein set; GeneMarkS+"  different versions of a pipeline may use different methods; different pipelines will use different methods
        biosamples=[]
        bioprojects=[]
        assemblys=[]
        sras=[]
        output=seqentry.iterfind('.//Seq-descr/Seqdesc/Seqdesc_user/User-object/User-object_data/User-field')
        for indx, out in enumerate(output):
            try:
                label=out.find('./User-field_label/Object-id/Object-id_str').text
            except:
                continue
            #get sequencing/assembly/annotation method data
            if label=='Sequencing Technology':
                seqtech=out.find('./User-field_data/User-field_data_str')
                if seqtech!=None:
                    seqtechs.append(mystrip(seqtech.text))
            if label=='Genome Coverage':
                coverage=out.find('./User-field_data/User-field_data_str')
                if coverage!=None:
                    coverages.append(mystrip(coverage.text))
            if label=='Assembly Method':
                assemblymethod=out.find('./User-field_data/User-field_data_str')
                if assemblymethod!=None:
                    assemblymethods.append(mystrip(assemblymethod.text))
            if label=='Annotation Pipeline':
                annotationpipeline=out.find('./User-field_data/User-field_data_str')
                if annotationpipeline!=None:
                    annotationpipelines.append(mystrip(annotationpipeline.text))
            if label=='Annotation Software revision':
                annotationversion=out.find('./User-field_data/User-field_data_str')
                if annotationversion!=None:
                    annotationversions.append(mystrip(annotationversion.text))
            if label=='Annotation Method':
                annotationmethod=out.find('./User-field_data/User-field_data_str')
                if annotationmethod!=None:
                    annotationmethods.append(mystrip(annotationmethod.text))
                    
            #get bioproject/biosample/assembly/SRA database accessions
            if label=='BioProject':
                bioproject=out.find('./User-field_data/User-field_data_strs/User-field_data_strs_E')
                if bioproject!=None:
                    bioprojects.append(mystrip(bioproject.text))
            if label=='BioSample':
                biosample=out.find('./User-field_data/User-field_data_strs/User-field_data_strs_E')
                if biosample!=None:
                    biosamples.append(mystrip(biosample.text))
            if label=='Assembly':
                assembly=out.find('./User-field_data/User-field_data_strs/User-field_data_strs_E')
                if assembly!=None:
                    assemblys.append(mystrip(assembly.text))
            if label=='Sequence Read Archive':
                sra=out.find('./User-field_data/User-field_data_strs/User-field_data_strs_E')
                if sra!=None:
                    sras.append(mystrip(sra.text))
            
            
        if len(seqtechs)==0:
            seqtechs.append('-')
        if len(coverages)==0:
            coverages.append('-')
        if len(assemblymethods)==0:
            assemblymethods.append('-')
        if len(annotationpipelines)==0:
            annotationpipelines.append('-')
        if len(annotationversions)==0:
            annotationversions.append('-')
        if len(annotationmethods)==0:
            annotationmethods.append('-')
        if len(biosamples)==0:
            biosamples.append('-')
        if len(bioprojects)==0:
            bioprojects.append('-')
        if len(assemblys)==0:
            assemblys.append('-')
        if len(sras)==0:
            sras.append('-')

        #pubmed links/createdate/updatedate/moleculetype/length/completeness/source organism/source molecule
        #pubmedlinks
        pmids=[]
        output=seqentry.iterfind('.//Seq-descr/Seqdesc/Seqdesc_pub/Pubdesc/Pubdesc_pub/Pub-equiv/Pub/Pub_pmid')
        if output!=None:
            for indx, out in enumerate(output):
                pmid=out.find('./PubMedId')
                if pmid!=None:
                    pmid=pmid.text
                    if pmid!=None:
                        pmid='https://www.ncbi.nlm.nih.gov/pubmed/'+pmid.strip()
                        pmids.append(pmid)
        if len(pmids)==0:
            pmids.append('-')           
        #createdate
        output=seqentry.find('.//Seq-descr/Seqdesc/Seqdesc_create-date/Date/Date_std/Date-std')
        createdate='-'
        if output!=None:
            year=output.find('./Date-std_year')
            month=output.find('./Date-std_month')
            day=output.find('./Date-std_day')
            if year!=None and month!=None and day!=None:
                createdate=mystrip(year.text)+'-'+mystrip(month.text)+'-'+mystrip(day.text)
        #updatedate
        output=seqentry.find('.//Seq-descr/Seqdesc/Seqdesc_update-date/Date/Date_std/Date-std')
        updatedate='-'
        if output!=None:
            year=output.find('./Date-std_year')
            month=output.find('./Date-std_month')
            day=output.find('./Date-std_day')
            if year!=None and month!=None and day!=None:
                updatedate=mystrip(year.text)+'-'+mystrip(month.text)+'-'+mystrip(day.text)
        #moleculetype/length
        output=seqentry.find('.//Bioseq_inst/Seq-inst')
        moleculetype='-'
        length='-'
        topology='-'
        if output!=None:
            out=output.find('./Seq-inst_mol')
            if out!=None:
                moleculetype=mystrip(out.attrib['value'])
            out=output.find('./Seq-inst_length')
            if out!=None:
                length=mystrip(out.text)
        #completeness
        completeness='-'
        output=seqentry.find('.//Seq-descr/Seqdesc/Seqdesc_molinfo/MolInfo')
        if output!=None:
            out=output.find('./MolInfo_completeness')
            if out!=None:
                completeness=mystrip(out.attrib['value'])
        #source organism/source molecule
        sourcegenome='-'
        sourcetaxon='-'
        sourcetaxid='-'
        output=seqentry.find('.//Seq-descr/Seqdesc/Seqdesc_source/BioSource')
        if output!=None:
            out=output.find('./BioSource_genome')
            if out!=None:
                sourcegenome=mystrip(out.attrib['value'])
            out=output.find('./BioSource_org/Org-ref/Org-ref_taxname')
            if out!=None:
                sourcetaxon=mystrip(out.text)
            out=output.find('./BioSource_org/Org-ref/Org-ref_db/Dbtag/[Dbtag_db="taxon"]/Dbtag_tag/Object-id/Object-id_id')
            if out!=None:
                sourcetaxid=mystrip(out.text)


        print('%s'%'\t'.join(accessionversion,createdate,updatedate,moleculetype,length,completeness,sourcegenome,sourcetaxon,sourcetaxid,';'.join(assemblymethods),';'.join(coverages),'; '.join(seqtechs),';'.join(annotationpipelines),'|'.join(';'.join(annotationversions),';'.join(annotationmethods)),';'.join(bioprojects),';'.join(biosamples),';'.join(sras),';'.join(assemblys),'; '.join(pmids)))  #';'.join is used to capture cases where there are multiple entries that may be of interest; in other cases I'm only ever interested in one entry (title)

missingaccessions=list(set(accessions).difference(set(includedaccessions)))
if len(missingaccessions)>0:
    for missingaccession in missingaccessions:
        f2.write('%s\n'%missingaccession)
f2.close()
