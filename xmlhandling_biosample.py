from sys import stdin
import xml.etree.cElementTree as etree
import codecs
import sys

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

accessions=sys.argv[1]
accessions=accessions.split(',') #biosample accessions
outdir=sys.argv[2]


tree=etree.parse(stdin)
root=tree.getroot()

assert root.tag=='BioSampleSet', "xml is of type %s rather than of type BioSampleSet: make sure multiple accessions are efetched" %root.tag


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


for biosample in root:
    accession=None
    accessionnode=biosample.find('./Ids/Id[@db="BioSample"][@is_primary="1"]')
    if accessionnode==None:
        continue
    accession=mystrip(accessionnode.text,nonehandling='accession')
    if accession not in accessions:
        continue
    else:
        includedaccessions.append(accession)
    #print accession
    ##extract model and pacakge
    models=[]
    packages=[]
    model=biosample.find('.//Models/Model')
    if model!=None:
        models.append(mystrip(model.text))
    package=biosample.find('.//Package')
    if package!=None:
        packages.append(mystrip(package.text))
    if len(models)==0:
        models.append('-')
    if len(packages)==0:
        packages.append('-')
    ##extract description/organism details
    titles=[]
    taxids=[]
    taxnames=[]
    orgnames=[]
    description=biosample.find('.//Description')
    if description!=None:
        title=description.find('./Title')
        if title!=None:
            titles.append(mystrip(title.text))
        organism=description.find('./Organism')
        if organism!=None:
            orgattrib=organism.attrib
            if 'taxonomy_id' in orgattrib:
                taxids.append(mystrip(organism.attrib['taxonomy_id']))
            if 'taxonomy_name' in orgattrib:
                taxnames.append(mystrip(organism.attrib['taxonomy_name']))
            orgname=organism.find('./OrganismName')
            if orgname!=None:
                orgnames.append(mystrip(orgname.text))
    if len(titles)==0:
        titles.append('-')
    if len(taxids)==0:
        taxids.append('-')
    if len(taxnames)==0:
        taxnames.append('-')
    if len(orgnames)==0:
        orgnames.append('-')
    ###extract contact details
    owners=[]
    emails=[]
    firstnames=[]
    lastnames=[]
    owner=biosample.find('.//Owner/Name')
    if owner!=None:
        owners.append(mystrip(owner.text))
    contact=biosample.find('.//Owner/Contacts/Contact')
    if contact!=None:
        if 'email' in contact.attrib:
            emails.append(mystrip(contact.attrib['email']))
        firstname=contact.find('./Name/First')
        lastname=contact.find('./Name/Last')
        if firstname!=None:
            firstnames.append(mystrip(firstname.text))
        if lastname!=None:
            lastnames.append(mystrip(lastname.text))
    if len(owners)==0:
        owners.append('-')
    if len(emails)==0:
        emails.append('-')
    if len(firstnames)==0:
        firstnames.append('-')
    if len(lastnames)==0:
        lastnames.append('-')
    ###extract metadata attributes
    dates=[]
    hosts=[]
    sources=[]
    sampletypes=[]
    locations=[]
    latlons=[]
    broadenvironments=[]
    localenvironments=[]
    environmentalmediums=[]
    output=biosample.iterfind('.//Attributes')
    for indx, out in enumerate(output):
        try:
            labels=out.findall('./Attribute')
        except:
            continue
        for label in labels:
            labelattrib=label.attrib
            if 'harmonized_name' in labelattrib:
                if labelattrib['harmonized_name']=='collection_date':
                    dates.append(mystrip(label.text))
                if labelattrib['harmonized_name']=='host':
                    hosts.append(mystrip(label.text))
                if labelattrib['harmonized_name']=='isolation_source':
                    sources.append(mystrip(label.text))
                if labelattrib['harmonized_name']=='sample_type':
                    sampletypes.append(mystrip(label.text))                
                if labelattrib['harmonized_name']=='geo_loc_name':
                    locations.append(mystrip(label.text))
                if labelattrib['harmonized_name']=='lat_lon':
                    latlons.append(mystrip(label.text))
                if labelattrib['harmonized_name']=='env_broad_scale': #broad-scale environmental context
                    broadenvironments.append(mystrip(label.text))
                if labelattrib['harmonized_name']=='env_local_scale': #local-scale environmental context
                    localenvironments.append(mystrip(label.text))
                if labelattrib['harmonized_name']=='env_medium': #environmental medium
                    environmentalmediums.append(mystrip(label.text))

    if len(dates)==0:
        dates.append('-')
    if len(hosts)==0:
        hosts.append('-')
    if len(sources)==0:
        sources.append('-')
    if len(sampletypes)==0:
        sampletypes.append('-')        
    if len(locations)==0:
        locations.append('-')
    if len(latlons)==0:
        latlons.append('-')
    if len(broadenvironments)==0:
        broadenvironments.append('-')
    if len(localenvironments)==0:
        localenvironments.append('-')
    if len(environmentalmediums)==0:
        environmentalmediums.append('-')
#17
    print '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s'%(accession,models[0],packages[0],'; '.join(titles),'; '.join(taxids),'; '.join(taxnames),'; '.join(orgnames),owners[0],emails[0], firstnames[0],lastnames[0],'; '.join(dates),'; '.join(hosts),'; '.join(sources),'; '.join(sampletypes),'; '.join(locations),'; '.join(latlons),'; '.join(broadenvironments),'; '.join(localenvironments),'; '.join(environmentalmediums))


#write missing accessions to file

missingaccessions=list(set(accessions).difference(set(includedaccessions)))
if len(missingaccessions)>0:
    for missingaccession in missingaccessions:
        f2.write('%s\n'%missingaccession)
f2.close()






#OLD - now using hamronzed name rather than attribute name
            # if 'attribute_name' in labelattrib:
            #     if labelattrib['attribute_name']=='collection_date':
            #         dates.append(mystrip(label.text))
            #     if labelattrib['attribute_name']=='host':
            #         hosts.append(mystrip(label.text))
            #     if labelattrib['attribute_name']=='isolation_source':
            #         sources.append(mystrip(label.text))
            #     if labelattrib['attribute_name']=='sample_type':
            #         sampletypes.append(mystrip(label.text))                
            #     if labelattrib['attribute_name']=='geo_loc_name':
            #         locations.append(mystrip(label.text))
            #     if labelattrib['attribute_name']=='lat_lon':
            #         latlons.append(mystrip(label.text))
            #     if labelattrib['attribute_name']=='env_biome': #broad-scale environmental context
            #         broadenvironments.append(mystrip(label.text))

#OLD

    #print accession
    #print models[0], packages[0]
    #print '; '.join(titles),'; '.join(taxids),'; '.join(taxnames),'; '.join(orgnames)
    #print emails[0], firstnames[0],lastnames[0]
    #print '; '.join(dates),'; '.join(hosts),'; '.join(sources),'; '.join(sampletypes),'; '.join(locations),'; '.join(latlons),'; '.join(environments) #allowing for multiple entries

    
#other things that could be extracted: contact details/collected_by, model, package, strain,isolate,sample_type, (broad-scale) environmental context
#!need to find out more about the different packages

#OLD
    
#reminder of structure of accession xml
    
#<Bioseq-set>
#  <Bioseq-set_seq-set>   #there is just one of these tags
#    <Seq-entry>

    
# for seqset in root:
#     for seqentry in seqset:
#         accessiontype=None
#         ###extract refseq accession###
#         accessionnode=seqentry.find('./Seq-entry_seq/Bioseq/Bioseq_id/Seq-id/Seq-id_other/Textseq-id/Textseq-id_accession')
#         version=seqentry.find('./Seq-entry_seq/Bioseq/Bioseq_id/Seq-id/Seq-id_other/Textseq-id/Textseq-id_version')
#         if accessionnode !=None:
#             accessiontype='refseq'
#             if version!=None:
#                 accession=accessionnode.text+'.'+version.text
#             else:
#                 accession=accessionnode.text
#         ###extract genbank accession###
#         nodes=seqentry.iterfind('./Seq-entry_set/Bioseq-set/Bioseq-set_seq-set/Seq-entry/Seq-entry_seq/Bioseq/Bioseq_id/') #Seq-id/Seq-id_genbank - must be direct path with no children in between
#         for indxa, node in enumerate(nodes): #iterating through seq-id
#             if indxa==0:
#                 for subnode in node:
#                     if subnode.tag=='Seq-id_genbank':
#                         #print indxa, node.tag  #Seq-id (must be indx0)
#                         accessionnode=subnode.find('Textseq-id/Textseq-id_accession')
#                         version=subnode.find('Textseq-id/Textseq-id_version')
#                         if accessionnode!=None:
#                             if version!=None:
#                                 accessiontype='genbank'
#                                 accession=accessionnode.text+'.'+version.text
#                             else:
#                                 accession=accessionnode.text
#         ###extract data based on accession type###
#         if accessiontype==None:
#             #print 'Error: accession missing'
#             continue
#         ###extract refseq data###
#         #if accessiontype=='refseq':
#             #print 'refseq'

#         #get seqtech, biosample/bioproject/assembly accession
#         seqtechs=[]
#         biosamples=[]
#         bioprojects=[]
#         assemblys=[]
#         output=seqentry.iterfind('.//Seq-descr/Seqdesc/Seqdesc_user/User-object/User-object_data/User-field') #removed Bioseq_descr
#         for indx, out in enumerate(output):
#             try:
#                 label=out.find('./User-field_label/Object-id/Object-id_str').text
#             except:
#                 continue
#             if label=='Sequencing Technology':
#                 seqtech=out.find('./User-field_data/User-field_data_str')
#                 if seqtech!=None:
#                     seqtechs.append(seqtech.text)
#             if label=='BioProject':
#                 bioproject=out.find('./User-field_data/User-field_data_strs/User-field_data_strs_E')
#                 if bioproject!=None:
#                     bioprojects.append(bioproject.text)
#             if label=='BioSample':
#                 biosample=out.find('./User-field_data/User-field_data_strs/User-field_data_strs_E')
#                 if biosample!=None:
#                     biosamples.append(biosample.text)
#             if label=='Assembly':
#                 assembly=out.find('./User-field_data/User-field_data_strs/User-field_data_strs_E')
#                 if assembly!=None:
#                     assemblys.append(assembly.text)
            
#         if len(seqtechs)==0:
#             seqtechs.append('-')
#         if len(biosamples)==0:
#             biosamples.append('-')
#         if len(biosamples)>1:
#             biosamples=biosamples[0]
#         if len(bioprojects)==0:
#             bioprojects.append('-')
#         if len(bioprojects)>1:
#             bioprojects=bioprojects[0]
#         if len(assemblys)==0:
#             assemblys.append('-')
#         if len(assemblys)>1:
#             assemblys=assemblys[0]
#         #print '; '.join(seqtechs), bioprojects[0], biosamples[0], assemblys[0] #allowing for multiple seqtech entries
            
#         #create date
#         createdate=[]
#         output=seqentry.iterfind('.//Seq-descr/Seqdesc/Seqdesc_create-date/Date/Date_std/Date-std') #removed Bioseq_descr
#         for indx, out in enumerate(output):
#             if indx>0:
#                 break
#             year=out.find('./Date-std_year').text
#             month=out.find('./Date-std_month').text
#             day=out.find('./Date-std_day').text
#             date=day+'-'+month+'-'+year
#             createdate=date
#         if len(createdate)==0:
#             createdate='-'
#         #print createdate

#         #pubmed link/title (could also get more details about annotatoin and assembly methods but probably not necessary)
#         pmids=[]
#         output=seqentry.iterfind('.//Seq-descr/Seqdesc/Seqdesc_pub/Pubdesc/Pubdesc_pub/Pub-equiv/Pub/Pub_pmid') #removed Bioseq_descr
#         for indx, out in enumerate(output):
#             pmid=out.find('./PubMedId').text
#             pmid='https://www.ncbi.nlm.nih.gov/pubmed/'+pmid
#             pmids.append(pmid)
#         if len(pmids)==0:
#             pmids.append('-')
#         #print '; '.join(pmids) #allowing for multiple pubmed ids
            

#         print '%s\t%s\t%s\t%s\t%s\t%s\t%s'%(accession.strip(),createdate.strip(),'; '.join(seqtechs).strip(), bioprojects[0], biosamples[0], assemblys[0],'; '.join(pmids).strip())
        
#         #other data requires elink




#TESTING

#print root,'root' #<Element 'BioSampleSet' at 0x7fd30d4fe450>


# def count_nodes(element, tagname):
#     """Return the number of tagname nodes in the tree rooted at element"""
#     count = 0
#     for node in element.getiterator(tagname):
#         count += 1
#     return count

#mycount=count_nodes(tree, 'BioSample')
#print mycount #6
