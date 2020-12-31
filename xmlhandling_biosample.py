from sys import stdin
import xml.etree.cElementTree as etree
import codecs
import sys

if sys.version_info < (3, 0):
    UTF8Writer = codecs.getwriter('utf8')
    sys.stdout = UTF8Writer(sys.stdout)

accessions=sys.argv[1]
accessions=accessions.split(',') #biosample accessions
outdir=sys.argv[2]
attributefilepresent=sys.argv[3]

attributes=[]
if attributefilepresent=='True':
    attributefile=sys.argv[4]
    with open(attributefile) as f:
        for line in f:
            data=line.strip().split('\t')
            attribute=data[0].strip()
            attributes.append(data[0])
    

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
    #print(accession)
    #get dates and accession id number
    lastupdatedate='-'
    publicationdate='-'
    submissiondate='-'
    accessionnumber='-'
    biosampleattrib=biosample.attrib
    if 'last_update' in biosampleattrib:
        lastupdatedate=mystrip(biosampleattrib['last_update'])
    if 'publication_date' in biosampleattrib:
        publicationdate=mystrip(biosampleattrib['publication_date'])
    if 'submission_date' in biosampleattrib:
        submissiondate=mystrip(biosampleattrib['submission_date'])
    if 'id' in biosampleattrib:
        accessionnumber=mystrip(biosampleattrib['id'])
    #get sample name (under identifier tag) (there may also be sample name provided as attribute - see below)
    samplenamenode=biosample.find('./Ids/Id[@db_label="Sample name"]')
    if samplenamenode!=None:
        samplenameidentifier=mystrip(samplenamenode.text)
    else:
        samplenameidentifier='-'
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
    comments=[]
    taxids=[]
    taxnames=[]
    orgnames=[]
    description=biosample.find('.//Description')
    if description!=None:
        title=description.find('./Title')
        if title!=None:
            titles.append(mystrip(title.text))
        comment=description.find('./Comment/Paragraph')
        if comment!=None:
            comments.append(mystrip(comment.text))
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
    if len(comments)==0:
        comments.append('-')
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
    if len(attributes)>0:
        #initialise attribute dictionary
        attributedict={}
        for attribute in attributes:
            attributedict[attribute]=[]
        #append attributes to dictionary if present
        output=biosample.iterfind('.//Attributes')
        for indx, out in enumerate(output):
            try:
                labels=out.findall('./Attribute')
            except:
                continue
            for label in labels:
                labelattrib=label.attrib
                if 'harmonized_name' in labelattrib:
                    for attribute in attributes:
                        if labelattrib['harmonized_name']==attribute:
                            attributedict[attribute].append(mystrip(label.text))
        #gather output
        attributeoutputlist=[]
        for attribute in attributes:
            values=attributedict[attribute]
            if len(values)==0:
                attributeoutputlist.append('-')
            else:
                attributeoutputlist.append(';'.join(values))

    #write to file
    if len(attributes)>0:
        print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s'%(accession,accessionnumber,samplenameidentifier,models[0],packages[0],lastupdatedate,publicationdate,submissiondate,'; '.join(titles),'; '.join(comments),'; '.join(taxids),'; '.join(taxnames),'; '.join(orgnames),owners[0],emails[0], firstnames[0],lastnames[0],'\t'.join(attributeoutputlist)))
    else:
        print('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s'%(accession,accessionnumber,samplenameidentifier,models[0],packages[0],lastupdatedate,publicationdate,submissiondate,'; '.join(titles),'; '.join(comments),'; '.join(taxids),'; '.join(taxnames),'; '.join(orgnames),owners[0],emails[0], firstnames[0],lastnames[0]))

        
#write missing accessions to file

missingaccessions=list(set(accessions).difference(set(includedaccessions)))
if len(missingaccessions)>0:
    for missingaccession in missingaccessions:
        f2.write('%s\n'%missingaccession)
f2.close()

