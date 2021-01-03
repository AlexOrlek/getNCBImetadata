#!/usr/bin/env python                                                                                                                                                                       
import argparse, os, sys, signal, time
import pandas as pd
sourcedir=os.path.dirname(os.path.abspath(__file__))
cwdir=os.getcwd()
sys.path.append(sourcedir)

from pythonmods import runsubprocess

def default_sigpipe():
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

def batchsizeint(x):
    x = int(x)
    if x < 2:
         raise argparse.ArgumentTypeError("%s is too small; batch size must be greater than 1" %x)
    if x > 100:
         raise argparse.ArgumentTypeError("%s is too large; batch size must not exceed 100" %x)
    return x


parser = argparse.ArgumentParser(description='Run pipeline scripts')
parser.add_argument('-a','--accessions', help='Text file with column containing accessions for which metadata are to be retrieved (required)', required=True, type=str)
parser.add_argument('-t','--accessiontype', help='Type of accession (either nucleotide or biosample) (required)', choices=['nucleotide','biosample'], required=True, type=str)
parser.add_argument('-o','--out', help='Output directory (required)', required=True, type=str)
parser.add_argument('-b','--batchsize', help='Number of accession metadata records to retrieve per edirect query (default: 100; min: 2; max: 100)', default=100, type=batchsizeint)
parser.add_argument('-e','--emailaddress', help="User's email address which will be provided as an argument to edirect econtact -email (required)", required=True, type=str)
parser.add_argument('--biosampleattributes', help="Path to file containing column of harmonized names of biosample attributes to be retrieved (not required)", required=False, type=str)

#parser.add_argument('--noaccessionversions', action='store_true', help='If flag provided, this specifies that input accessions do not include the .version suffix (default: input accessions must be in the formataccession.version')

args = parser.parse_args()
outputpath=os.path.relpath(args.out, cwdir)

#check that multiple accessions are provided
counter=0
with open(args.accessions) as f:
    for indx, line in enumerate(f):
        counter=counter+1
        if indx>1:
            break
if counter<2:
    print('Error: multiple accessions must be provided')
    sys.exit()


#if nucleotide input, check whether accessions are in format accession or accession.version; check all accessions in same format
if args.accessiontype=='nucleotide':
    with open(args.accessions) as f:
        for indx, line in enumerate(f):
            accession=line.strip().split('\t')[0]
            if indx==0:
                accession=accession.split('.')
                accessionlen=len(accession)
                continue
            accession=accession.split('.')
            if len(accession)!=accessionlen:
                print('Error: accessions are not a consistent format; all accessions must be in either "accession" or "accession.version" format')
                sys.exit()

    if accessionlen==1:
        accessiontype='accession'
    elif accessionlen==2:
        accessiontype='accessionversion'
    else:
        print('Error: unknown accession format')
        sys.exit()

#if biosample input check whether a biosample attributes file has been provided

if args.biosampleattributes==None:
    attributefilepresent=False
    attributefilepath='NA'
else:
    attributefilepresent=True
    attributefilepath=str(args.biosampleattributes)
    #check all provided attribute names are valid (listed in attributenames.tsv)
    attributes=[]
    with open('%s/attributenames.tsv'%sourcedir) as f:
        for line in f:
            attribute=line.strip().split('\t')[0]
            attributes.append(attribute)
    with open(attributefilepath) as f:
        for line in f:
            attribute=line.strip().split('\t')[0]
            if attribute not in attributes:
                sys.exit('Harmonized attribute name: %s is invalid (not listed in attributenames.tsv)'%attribute)
            


###run Edirect commands

if args.accessiontype=='nucleotide':
    print('retrieving nucleotide accession metadata from NCBI')

    accessionsdf=pd.read_csv('%s'%str(args.accessions),header=None,sep='\t')
    accessions=accessionsdf.iloc[:,0].tolist()

    runsubprocess(['mkdir -p %s'%outputpath],shell=True)
    f=open('%s/nucleotidemetadata.tsv'%outputpath,'w')
    f.write('Accession\tCreateDate\tUpdateDate\tMoleculeType\tLength\tCompleteness\tSourceGenomeType\tSourceTaxon\tSourceTaxID\tAssemblyMethod\tGenomeCoverage\tSequencingTechnology\tAnnotationPipeline\tAnnotationMethod\tBioprojectAccession\tBiosampleAccession\tSRAAccession\tAssemblyAccession\tPubMedID\n')
    f.close()
    f=open('%s/missingaccessions.txt'%outputpath,'w')
    f.close()

    accessionslen=len(accessions)
    chunklen=int(args.batchsize)

    runsubprocess(['econtact -email %s -tool nucleotidemetadatadownload'%str(args.emailaddress)],shell=True)

    for i in range(0,accessionslen,chunklen):
        start=i+1
        print(start)
        stop=i+chunklen
        if(stop>accessionslen):
            stop=accessionslen
        #slice accessions list
        chunkedaccessionsstring=','.join(accessions[i:i+chunklen])
        #run edirect command
        sedcommand='sed -n "%s,%s"p "%s"'%(start,stop,str(args.accessions))
        runsubprocess(['%s | epost -db nuccore -format acc | efetch -format xml | python %s/xmlhandling_nucleotide.py %s %s %s >> %s/nucleotidemetadata.tsv'%(sedcommand,sourcedir,chunkedaccessionsstring,outputpath,accessiontype,outputpath)],shell=True)
        #sleep
        time.sleep(1)

elif args.accessiontype=='biosample':
    print('retrieving biosample accession metadata from NCBI')

    accessionsdf=pd.read_csv('%s'%str(args.accessions),header=None,sep='\t')
    accessions=accessionsdf.iloc[:,0].tolist()

    runsubprocess(['mkdir -p %s'%outputpath],shell=True)
    f=open('%s/biosamplemetadata.tsv'%outputpath,'w')
    header=['Accession','AccessionIDNumber','SampleNameIdentifier','Model','Package','LastUpdateDate','PublicationDate','SubmissionDate','Title','Comment','TaxonomyID','TaxonomyName','OrganismName','AffiliationName','ContactEmail','ContactFirstName','ContactLastName']
    if attributefilepresent==True:
        attributesdf=pd.read_csv('%s'%attributefilepath,header=None,sep='\t')
        attributes=attributesdf.iloc[:,0].tolist()
        header.extend(attributes)
    f.write('%s\n'%'\t'.join(header))
    f.close()
    f=open('%s/missingaccessions.txt'%outputpath,'w')
    f.close()

    accessionslen=len(accessions)
    chunklen=int(args.batchsize)

    runsubprocess(['econtact -email %s -tool biosamplemetadatadownload'%str(args.emailaddress)],shell=True)

    for i in range(0,accessionslen,chunklen):
        start=i+1
        print(start)
        stop=i+chunklen
        if(stop>accessionslen):
            stop=accessionslen
        #slice accessions list
        chunkedaccessionsstring=','.join(accessions[i:i+chunklen])
        #run edirect command
        sedcommand='sed -n "%s,%s"p "%s"'%(start,stop,str(args.accessions))
        if attributefilepresent==True:
            runsubprocess(['%s | epost -db biosample -format acc | efetch -format xml | python %s/xmlhandling_biosample.py %s %s %s %s >> %s/biosamplemetadata.tsv'%(sedcommand,sourcedir,chunkedaccessionsstring,outputpath,attributefilepresent,attributefilepath,outputpath)],shell=True)
        else:
            runsubprocess(['%s | epost -db biosample -format acc | efetch -format xml | python %s/xmlhandling_biosample.py %s %s %s >> %s/biosamplemetadata.tsv'%(sedcommand,sourcedir,chunkedaccessionsstring,outputpath,attributefilepresent,outputpath)],shell=True)
        #sleep
        time.sleep(1)
else:
    print('invalid accession type')
    sys.exit()

print('Finished!')