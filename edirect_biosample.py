import sys, time
import pandas as pd
from pythonmods import runsubprocess

file=sys.argv[1]
batchsize=sys.argv[2]
emailaddress=sys.argv[3]
outdir=sys.argv[4]
sourcedir=sys.argv[5]
attributefilepresent=bool(sys.argv[6])

if attributefilepresent==True:
    attributefile=sys.argv[7]

accessionsdf=pd.read_csv('%s'%file,header=None,sep='\t')
accessions=accessionsdf.iloc[:,0].tolist()

runsubprocess(['mkdir -p %s'%outdir],shell=True)

f=open('%s/biosamplemetadata.tsv'%outdir,'w')
header=['Accession','AccessionIDNumber','SampleNameIdentifier','Model','Package','LastUpdateDate','PublicationDate','SubmissionDate','Title','Comment','TaxonomyID','TaxonomyName','OrganismName','AffiliationName','ContactEmail','ContactFirstName','ContactLastName']
if attributefilepresent==True:
    attributesdf=pd.read_csv('%s'%attributefile,header=None,sep='\t')
    attributes=attributesdf.iloc[:,0].tolist()
    header.extend(attributes)
f.write('%s\n'%'\t'.join(header))
f.close()
f=open('%s/missingaccessions.txt'%outdir,'w')
f.close()


accessionslen=len(accessions)
chunklen=int(batchsize)

runsubprocess(['econtact -email %s -tool biosamplemetadatadownload'%emailaddress],shell=True)


for i in range(0,accessionslen,chunklen):
    start=i+1
    print(start)
    stop=i+chunklen
    if(stop>accessionslen):
        stop=accessionslen
    #slice accessions list
    chunkedaccessionsstring=','.join(accessions[i:i+chunklen])
    #run edirect command
    sedcommand='sed -n "%s,%s"p "%s"'%(start,stop,file)
    if attributefilepresent==True:
        runsubprocess(['%s | epost -db biosample -format acc | efetch -format xml | python %s/xmlhandling_biosample.py %s %s %s %s >> %s/biosamplemetadata.tsv'%(sedcommand,sourcedir,chunkedaccessionsstring,outdir,attributefilepresent,attributefile,outdir)],shell=True)
    else:
        runsubprocess(['%s | epost -db biosample -format acc | efetch -format xml | python %s/xmlhandling_biosample.py %s %s %s >> %s/biosamplemetadata.tsv'%(sedcommand,sourcedir,chunkedaccessionsstring,outdir,attributefilepresent,outdir)],shell=True)
    #sleep
    time.sleep(1)
