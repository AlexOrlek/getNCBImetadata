#!/usr/bin/env python                                                                                                                                                                                              
import argparse, os, sys, subprocess, signal
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
    attributefilepresent='False'
    attributefilepath='NA'
else:
    attributefilepresent='True'
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
            



            
if args.accessiontype=='nucleotide':
    runsubprocess(['bash','%s/edirect_nucleotide.sh'%sourcedir,str(args.accessions),str(args.batchsize),str(args.emailaddress),outputpath,sourcedir,accessiontype])
elif args.accessiontype=='biosample':
    runsubprocess(['bash','%s/edirect_biosample.sh'%sourcedir,str(args.accessions),str(args.batchsize),str(args.emailaddress),outputpath,sourcedir,attributefilepresent,attributefilepath])
else:
    print('invalid accession type')
    sys.exit()
