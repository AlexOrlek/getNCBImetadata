# getNCBImetadata
[![DOI](https://zenodo.org/badge/177838141.svg)](https://zenodo.org/badge/latestdoi/177838141)

Retrieves NCBI metadata from [nucleotide](https://www.ncbi.nlm.nih.gov/nucleotide/) or [biosample](https://www.ncbi.nlm.nih.gov/biosample/) accession ids.

# Table of contents

* [Requirements](#Requirements)
* [Installation](#Installation)
* [Quick start](#Quick-start)
* [Output](#Output)
* [License](#License)


# Requirements

* Linux or MacOS or Windows with Windows Subsystem for Linux ([WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10)) installed
* [Bash shell](https://en.wikibooks.org/wiki/Bash_Shell_Scripting#What_is_Bash?), which is the default shell on MacOS and many Linux distributions
* [Python](https://www.python.org/) 2.7 or Python 3
* [Edirect](https://www.ncbi.nlm.nih.gov/books/NBK179288/)
* A computer with internet access via the HTTPS protocol - required for retrieving data from NCBI<br>


# Installation

```bash
git clone https://github.com/AlexOrlek/getNCBImetadata.git
cd getNCBImetadata
```
You should find the getmetadata.py executable script within the repository directory. If you add the path of this directory to your [$PATH variable](https://www.computerhope.com/issues/ch001647.htm), then the executable can be run by calling `getmetadata.py [`*`arguments...`*`]` from any directory location. Note also that the edirect directory must also be available in your $PATH variable.


# Quick start

The `-t` flag specifies whether `nucleotide` or	`biosample` accessions are provided in accessions.txt.<br>
The `-e` flag should be your own email address; this is provided to NCBI so that they can monitor usage.<br>
accessions.txt is a text file where the first column contains NCBI (nucleotide or biosample) accession ids.<br>


Nucleotide metadata can be retrieved by running the following code:

`getmetadata.py -a accessions.txt -t nucleotide -o outdir -e first.last@company.com`

Either Refseq or Genbank nucleotide accessions can be provided. Nucleotide accessions can be provided in either "accession" or "accession.version" format.<br>


BioSample metadata can be retrieved by running the following code:

`getmetadata.py -a accessions.txt -t biosample -o outdir -e first.last@company.com --biosampleattributes attributes.txt`

The `--biosampleattributes` flag is optional. It is used to specify a path to a file containing harmonized attribute names in the first column. A full list of BioSample attribute harmonized names is provided [here](https://www.ncbi.nlm.nih.gov/biosample/docs/attributes/). The specified attributes will be retrieved, in addition to default retrieved fields (see [Output](#Output) for details).<br>


# Output

__Nucleotide metadata__

When nucleotide accessions are provided, the following fields are extracted:
* `AccessionVersion`
* Dates of first submission and last update: `Create Date`, `Update Date`
* Molecular characteristics: `Molecule Type` (e.g. dna), `Length`, `Completeness`, `Source Genome Type` (e.g. plasmid)
* Taxonomy data: `Source Taxon`, `Source Taxonomic ID`
* Genome assembly data: `Assembly Method`, `Genome Coverage`, `Sequencing Technology`
* Genome annotation data: `Annotation Pipeline`, `Annotation Method`
* DBLink data: `Bioproject Accession`, `Biosample Accession`, `Sequence Read Archive Accession`, `Assembly Accession`
* `PubMedID`<br>


__Biosample metadata__

When biosample accessions are provided, the following fields are extracted:
* Identifiers: `Accession`, `Accession ID`, `Sample name`
* Submission data: `Model`, `Package`
* Dates: `last_update`, `publication_date`, `submission_date` 
* `Title`
* `Comment`
* Taxonomic data: `taxonomy_id`, `taxonomy_name`, `OrganismName`
* Affiliation data: `Owner/Name`, `email`, `Contact/Name/First`, `Contact/Name/Last`
* Attribute data will be retrieved if a file containing harmonized attribute names is provided to the `--biosampleattributes` flag.


# License

[MIT License](https://en.wikipedia.org/wiki/MIT_License)
