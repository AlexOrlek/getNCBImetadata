import sys, time
import pandas as pd
from pythonmods import runsubprocess

file=sys.argv[1]
batchsize=sys.argv[2]
emailaddress=sys.argv[3]
outdir=sys.argv[4]
sourcedir=sys.argv[5]
accessiontype=sys.argv[6]

accessionsdf=pd.read_csv('%s'%file,header=None,sep='\t')
accessions=accessionsdf.iloc[:,0].tolist()

runsubprocess(['mkdir -p %s'%outdir],shell=True)

f=open('%s/nucleotidemetadata.tsv'%outdir,'w')
f.write('Accession\tCreateDate\tUpdateDate\tMoleculeType\tLength\tCompleteness\tSourceGenomeType\tSourceTaxon\tSourceTaxID\tAssemblyMethod\tGenomeCoverage\tSequencingTechnology\tAnnotationPipeline\tAnnotationMethod\tBioprojectAccession\tBiosampleAccession\tSRAAccession\tAssemblyAccession\tPubMedID\n')
f.close()
f=open('%s/missingaccessions.txt'%outdir,'w')
f.close()


accessionslen=len(accessions)
chunklen=int(batchsize)

runsubprocess(['econtact -email %s -tool nucleotidemetadatadownload'%emailaddress],shell=True)

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
    runsubprocess(['%s | epost -db nuccore -format acc | efetch -format xml | python %s/xmlhandling_nucleotide.py %s %s %s >> %s/nucleotidemetadata.tsv'%(sedcommand,sourcedir,chunkedaccessionsstring,outdir,accessiontype,outdir)],shell=True)
    #sleep
    time.sleep(1)
