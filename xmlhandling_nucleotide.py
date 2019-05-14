from sys import stdin
import xml.etree.cElementTree as etree
import codecs
import sys

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

        #pubmed links/title/createdate/updatedate/moleculetype/length/topology/completeness/source organism/source molecule
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
        #Title
        output=seqentry.find('.//Seq-descr/Seqdesc/Seqdesc_title')
        title='-'
        if output!=None:
            title=mystrip(output.text)
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
        #moleculetype/length/topology
        output=seqentry.find('.//Bioseq_inst/Seq-inst')
        moleculetype='-'
        length='-'
        topology='-'
        if output!=None:
            moleculetype=output.find('./Seq-inst_mol').attrib['value']
            if moleculetype!=None:
                moleculetype=mystrip(moleculetype)
            length=output.find('./Seq-inst_length')
            if length!=None:
                length=mystrip(length.text)
            topology=output.find('./Seq-inst_topology').attrib['value']
            if topology!=None:
                topology=mystrip(topology)
        #completeness
        completeness='-'
        output=seqentry.find('.//Seq-descr/Seqdesc/Seqdesc_molinfo/MolInfo')
        if output!=None:
            out=output.find('./MolInfo_completeness').attrib['value']
            if out!=None:
                completeness=mystrip(out)
        #source organism/source molecule
        sourcegenome='-'
        sourcetaxon='-'
        sourcetaxid='-'
        output=seqentry.find('.//Seq-descr/Seqdesc/Seqdesc_source/BioSource')
        if output!=None:
            out=output.find('./BioSource_genome').attrib['value']
            if out!=None:
                sourcegenome=mystrip(out)
            out=output.find('./BioSource_org/Org-ref/Org-ref_taxname')
            if out!=None:
                sourcetaxon=mystrip(out.text)
            out=output.find('./BioSource_org/Org-ref/Org-ref_db/Dbtag/Dbtag_tag/Object-id/Object-id_id')
            if out!=None:
                sourcetaxid=mystrip(out.text)

        print '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s|%s\t%s\t%s\t%s\t%s\t%s'%(accessionversion,title,createdate,updatedate,moleculetype,length,topology,completeness,sourcegenome,sourcetaxon,sourcetaxid,';'.join(assemblymethods),';'.join(coverages),'; '.join(seqtechs),';'.join(annotationpipelines),';'.join(annotationversions),';'.join(annotationmethods),';'.join(bioprojects),';'.join(biosamples),';'.join(sras),';'.join(assemblys),'; '.join(pmids))  #';'.join is used to capture cases where there are multiple entries that may be of interest; in other cases I'm only ever interested in one entry (title)

missingaccessions=list(set(accessions).difference(set(includedaccessions)))
if len(missingaccessions)>0:
    for missingaccession in missingaccessions:
        f2.write('%s\n'%missingaccession)
f2.close()


#NOTES
#added fields:
#sras title createdate updatedate moleculetype length topology completeness sourcegenome sourcetaxon sourcetaxid

#OLD CODE - extracting fields that can be extracted trivially using edirect -format docsum

        # #create date
        # out=seqentry.find('.//Seq-descr/Seqdesc/Seqdesc_create-date/Date/Date_std/Date-std')
        # createdate='-'
        # if out!=None:
        #     year=out.find('./Date-std_year')
        #     month=out.find('./Date-std_month')
        #     day=out.find('./Date-std_day')
        #     if year!=None and month!=None and day!=None:
        #         createdate=mystrip(day.text)+'-'+mystrip(month.text)+'-'+mystrip(year.text)

        # #Title
        # out=seqentry.find('.//Seq-descr/Seqdesc/Seqdesc_title')
        # title='-'
        # if out!=None:
        #     title=mystrip(out.text)



#OLD CODE - TRYING TO EXTRACT ACCESSION USING FULL PATH

        # accessiontype=None
        # ###extract refseq accession###
        # accessionnode=seqentry.find('.//Seq-entry_seq/Bioseq/Bioseq_id/Seq-id/Seq-id_other/Textseq-id/Textseq-id_accession')
        # version=seqentry.find('.//Seq-entry_seq/Bioseq/Bioseq_id/Seq-id/Seq-id_other/Textseq-id/Textseq-id_version')
        # if accessionnode !=None:
        #     accessiontype='refseq'
        #     if version!=None:
        #         accession=mystrip(accessionnode.text,nonehandling='accession')+mystrip('.'+version.text,nonehandling='blank')
        #     else:
        #         accession=mystrip(accessionnode.text,nonehandling='accession')
        # ###extract genbank accession###
        # nodes=seqentry.iterfind('.//Seq-entry_set/Bioseq-set/Bioseq-set_seq-set/Seq-entry/Seq-entry_seq/Bioseq/Bioseq_id/') #Seq-id/Seq-id_genbank - must be direct path with no children in between
        # for indxa, node in enumerate(nodes): #iterating through seq-id
        #     if indxa==0:
        #         for subnode in node:
        #             if subnode.tag=='Seq-id_genbank':
        #                 #print indxa, node.tag  #Seq-id (must be indx0)
        #                 accessionnode=subnode.find('Textseq-id/Textseq-id_accession')
        #                 version=subnode.find('Textseq-id/Textseq-id_version')
        #                 if accessionnode!=None:
        #                     if version!=None:
        #                         accessiontype='genbank'
        #                         accession=mystrip(accessionnode.text,nonehandling='accession')+mystrip('.'+version.text,nonehandling='blank')
        #                     else:
        #                         accession=mystrip(accessionnode.text,nonehandling='accession')
        # ###extract data based on accession type###
        # if accessiontype==None:
        #     #print 'Error: accession missing'
        #     continue
        # ###extract refseq data###
        # #if accessiontype=='refseq':
        #     #print 'refseq'



        

#TESTING

###
            # #testing
            # output=seqentry.findall('.//User-field')
            # indices=[]
            # for indx, out in enumerate(output):
            #     indices.append(indx)
            # print max(indices)#3448 for the first accession
            

            # output=seqentry.findall('.//Bioseq_descr/Seq-descr/Seqdesc/Seqdesc_user/User-object/User-object_data/User-field')
            # indices=[]
            # for indx, out in enumerate(output):
            #     indices.append(indx)
            # print max(indices) #much fewer fields... ~30

###


            
            #output=seqentry.findall('.//Object-id_str')
            #for indx, out in enumerate(output):
            #    #print indx, out.tag, out.text
            #    if out.text=='Sequencing Technology':
                    

            #seqtech=seqentry.find('//Seq-entry_seq/Bioseq/Bioseq_descr/Seq-descr/Seqdesc/Seqdesc_user/User-object/User-object_data/User_field/User-field_label')
            #if seqtech!=None:
            #    print seqtech.text
        #if accessiontype=='genbank':
        #   seqtech=seqentry.find('//Seq-entry_seq/Bioseq/Bioseq_descr/Seq-descr/Seqdesc/Seqdesc_user/User-object/User-object_data/User_field/User-field_label')
        #   if seqtech!=None:
        #       print seqtech.text


        
            
#OLD CODE

##ONLY NEED TO USE FINDALL IF MULTIPLE VALUES EXPECTED
#accessions=seqentry.findall('./Seq-entry_seq/Bioseq/Bioseq_id/Seq-id/Seq-id_other/Textseq-id/Textseq-id_accession')
#for accession in accessions:
#    print accession.text

#OLD CODE
###this code works but better to first split by seq-entry                        

    #get data from refseq Seq-set
    #accessions=seqset.findall('Seq-entry/Seq-entry_seq/Bioseq/Bioseq_id/Seq-id/Seq-id_other/Textseq-id/Textseq-id_accession')
    #for accession in accessions:
    #    accessions_refseq.append(accession.text)



# #get data from genbank Seq-set
    # nodes=seqset.findall('Seq-entry/Seq-entry_set/Bioseq-set/Bioseq-set_seq-set/Seq-entry/Seq-entry_seq/Bioseq/Bioseq_id')  #Seq-id/Seq-id_genbank - must be direct path with no children in between
    # for indxa, node in enumerate(nodes): #seq-id
    #     #print node.tag, indxa
    #     for indxb, subnode in enumerate(node):
    #         #print subnode.tag, indxb #only reach indxb 0
    #         if indxb==0:
    #             for subsubnode in subnode:
    #                 if subsubnode.tag=='Seq-id_genbank':
    #                     print indxa, node.tag, indxb, subnode.tag, subsubnode.tag #Bioseq_id Seq-id (must be indx0) Seq-id_genbank
    #                     accession=subsubnode.find('Textseq-id/Textseq-id_accession')
    #                     print accession.text



#combine data
#accessions=accessions_refseq+accessions_genbank
#print accessions
            
            

        

####OLDER CODE



    # for indx, subnode in enumerate(nodes):
    
    #     if indx==0 and subnode.tag=='Seq-id':
    #         for indx, subsubnode in enumerate(subnode):
    #             if indx==0 and subsubnode.tag=='Seq-id_genbank':
    #                 print 'gotit'


# for seqset in root:
#     for seqentry in seqset:
#         #print seqentry
#         #for element in seqentry.iter('Textseq-id_accession'):
#             #print element.text #this prints accessions but includes Seq-id_other nodes
#         for element in seqentry.iter('./Seq-entry_seq/Bioseq/Bioseq_id/Seq-id/Seq-id_other'):
#             for subelement in element.iter('Textseq-id_accession'):
#                 print subelement.text
#         for element in seqentry.iter('./Seq-entry_seq/Bioseq/Bioseq_id/Seq-id/Seq-id_genbank'):
#             for subelement in element.iter('Textseq-id_accession'):
#                 print subelement.text




        # try:
        #     accession=seqentry.find('Textseq.id-accession').text
        #     print(accession)
        # except:
        #     print 'missing'





# for seq in root.iter('Seq-entry'):
#     try:
#        accession=seq.find('Textseq.id-accession').text
#        print(accession)
#     except:
#         print 'missing'
    

#FAIL
#from Bio import Entrez
#records = Entrez.read()
#print records[0]
