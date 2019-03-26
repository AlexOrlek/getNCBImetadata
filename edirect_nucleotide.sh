#!/bin/bash
set -e
set -u
set -o pipefail

file=${1}
batchsize=${2}
emailaddress=${3}
outdir=${4}
sourcedir=${5}

accessions=($(cut -f 1 "$file"))

mkdir -p "${outdir}"
> "${outdir}/nucleotidemetadata.tsv"
echo -e "Accession\tCreateDate\tSequencingTechnology\tAssemblyMethod\tAnnotationPipeline\tAnnotationMethod\tBioprojectAccession\tBiosampleAccession\tAssemblyAccession\tPubmedID" >> "${outdir}/nucleotidemetadata.tsv"

len=${#accessions[@]}
chunklen=${batchsize}

econtact -email ${emailaddress} -tool accessionmetadatadownload

for i in $(eval echo {0..$len..$chunklen})
do
    sum=$(( ($i + $chunklen) + 1 ))
    if [ $i -eq $len ]; then
	break
    elif [ $sum -eq $len ]; then
	echo $i
	chunklen=$(( $chunklen + 1 ))
	chunkedaccessions=${accessions[@]:$i:$chunklen} #slice accessions array
	chunkedaccessionsstring=$(echo $chunkedaccessions | sed 's/ /,/g')  #converting array to comma-separated string to use as query
	#echo $chunkedaccessionsstring
	esearch -db nuccore -query $chunkedaccessionsstring | efetch -format xml | python ${sourcedir}/xmlhandling_nucleotide.py >> "${outdir}/nucleotidemetadata.tsv"
	break
    else
	echo $i
	chunkedaccessions=${accessions[@]:$i:$chunklen} #slice accessions array
	chunkedaccessionsstring=$(echo $chunkedaccessions | sed 's/ /,/g')  #converting array to comma-separated string to use as query
	#echo $chunkedaccessionsstring
	esearch -db nuccore -query $chunkedaccessionsstring | efetch -format xml | python ${sourcedir}/xmlhandling_nucleotide.py >> "${outdir}/nucleotidemetadata.tsv"
	sleep 1
    fi
done



#OLD CODE

#chunkedaccessionsinput=$(echo $chunkedaccessions | sed 's/ /\n/g')  #converting array to data column to use as epost input
#echo "$chunkedaccessionsinput" | epost -db nuccore -format acc | efetch -format xml | python xmlhandling_accession.py >> "${outdir}/metadata/accessionmetadata.tsv" #!epost misorders accessions

#chunkedaccessionsinput=$(echo $chunkedaccessions | sed 's/ /\n/g')  #converting array to data column to use as epost input
#echo "$chunkedaccessionsinput" | epost -db nuccore -format acc | efetch -format xml | python xmlhandling_accession.py >> "${outdir}/metadata/accessionmetadata.tsv" #!epost misorders accessions
