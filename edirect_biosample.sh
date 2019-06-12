#!/bin/bash
set -e
set -u
set -o pipefail

file=${1}
batchsize=${2}
emailaddress=${3}
outdir=${4}
sourcedir=${5}
attributefilepresent=${6}
if [ ${attributefilepresent} == 'True' ]; then
    attributefile=${7}
fi

accessions=($(cut -f 1 "$file"))

mkdir -p "${outdir}"
> "${outdir}/biosamplemetadata.tsv"
> "${outdir}/missingaccessions.txt"


header=('Accession' 'AccessionIDNumber' 'SampleNameIdentifier' 'Model' 'Package' 'LastUpdateDate' 'PublicationDate' 'SubmissionDate' 'Title' 'Comment' 'TaxonomyID' 'TaxonomyName' 'OrganismName' 'AffiliationName' 'ContactEmail' 'ContactFirstName' 'ContactLastName')
if [ ${attributefilepresent} == 'True' ]; then
    attributes=($(cut -f1 "${attributefile}"))
    header=("${header[@]}" "${attributes[@]}")
    echo ${header[@]} | tr ' ' "\t" >> "${outdir}/biosamplemetadata.tsv"
else
    echo ${header[@]} | tr ' ' "\t" >> "${outdir}/biosamplemetadata.tsv"
fi


len=${#accessions[@]}
chunklen=${batchsize}


econtact -email ${emailaddress} -tool biosamplemetadatadownload

for i in $(eval echo {0..$len..$chunklen})
do
    sum=$(( ($i + $chunklen) + 1 ))
    if [ $i -eq $len ]; then
	break
    elif [ $sum -eq $len ]; then
	echo $i
	chunklen=$(( $chunklen + 1 ))
	chunkedaccessions=${accessions[@]:$i:$chunklen} #slice accessions array
	chunkedaccessionsinput=$(echo $chunkedaccessions | sed 's/ /\n/g')  #converting array to data column to use as epost input
	chunkedaccessionsstring=$(echo $chunkedaccessions | sed 's/ /,/g')  #converting array to comma-separated string to use as query
	#echo $chunkedaccessionsstring
	if [ ${attributefilepresent} == 'True' ]; then
	    echo "$chunkedaccessionsinput" | epost -db biosample -format acc | efetch -format xml | python ${sourcedir}/xmlhandling_biosample.py ${chunkedaccessionsstring} ${outdir} ${attributefilepresent} ${attributefile} >> "${outdir}/biosamplemetadata.tsv"
	else
	    echo "$chunkedaccessionsinput" | epost -db biosample -format acc | efetch -format xml | python ${sourcedir}/xmlhandling_biosample.py ${chunkedaccessionsstring} ${outdir} ${attributefilepresent} >> "${outdir}/biosamplemetadata.tsv"
	fi
	break
    else
	echo $i
	chunkedaccessions=${accessions[@]:$i:$chunklen} #slice accessions array
	chunkedaccessionsinput=$(echo $chunkedaccessions | sed 's/ /\n/g')  #converting array to data column to use as epost input
	chunkedaccessionsstring=$(echo $chunkedaccessions | sed 's/ /,/g')  #converting array to comma-separated string to use as query
	#echo $chunkedaccessionsstring
	if [ ${attributefilepresent} == 'True' ]; then
	    echo "$chunkedaccessionsinput" | epost -db biosample -format acc | efetch -format xml | python ${sourcedir}/xmlhandling_biosample.py ${chunkedaccessionsstring} ${outdir} ${attributefilepresent} ${attributefile} >> "${outdir}/biosamplemetadata.tsv"
	else
	    echo "$chunkedaccessionsinput" | epost -db biosample -format acc | efetch -format xml | python ${sourcedir}/xmlhandling_biosample.py ${chunkedaccessionsstring} ${outdir} ${attributefilepresent} >> "${outdir}/biosamplemetadata.tsv"
	fi
	sleep 1
    fi
done





#OLD CODE

#echo -e "Accession\tAccessionIDNumber\tSampleNameIdentifier\tModel\tPackage\tLastUpdateDate\tPublicationDate\tSubmissionDate\tDescription\tComment\tTaxonomyID\tTaxonomyName\tOrganismName\tAffiliationName\tContactEmail\tContactFirstName\tContactLastName\tCollectionDate\tHost\tIsolationSource\tSampleName\tStrain\tSampleType\tGeographicLocation\tLatitudeLongitude\tBroadScaleEnvironmentalContext\tLocalScaleEnvironmentalContext\tEnvironmentalMedium\tProjectName\tCultureCollection\tBiomaterialProvider\tBiomaterialReference\tSpecimenVoucher\tReferenceMaterial" >> "${outdir}/biosamplemetadata.tsv"


#echo "$chunkedaccessionsinput" | epost -db biosample -format acc | efetch -format xml >> testbiosample.xml
#esearch -db biosample -query $chunkedaccessionsstring | efetch -format xml >> testbiosample.xml #esearch fails



#file="${outdir}/biosampleaccessions_final.txt"

#    elif [ $i -gt 0 ]; then
#	break

#rm -f testbiosample_epost.xml
#> testbiosample_epost.xml
#rm -f testbiosample.xml
#> testbiosample.xml
