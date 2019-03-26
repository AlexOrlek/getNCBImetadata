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
parser.add_argument('-e','--emailaddress', help="User's email address which will be provided as an argument to edirect econtact -email", required=True, type=str)
args = parser.parse_args()
outputpath=os.path.relpath(args.out, cwdir)

if args.accessiontype=='nucleotide':
    runsubprocess(['bash','%s/edirect_nucleotide.sh'%sourcedir,str(args.accessions),str(args.batchsize),str(args.emailaddress),outputpath,sourcedir])
elif args.accessiontype=='biosample':
    runsubprocess(['bash','%s/edirect_biosample.sh'%sourcedir,str(args.accessions),str(args.batchsize),str(args.emailaddress),outputpath,sourcedir])
else:
    print('invalid accession type')
    sys.exit()
