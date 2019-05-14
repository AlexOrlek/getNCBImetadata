# getNCBImetadata
Retrieves NCBI metadata from [nucleotide](https://www.ncbi.nlm.nih.gov/nucleotide/) or [biosample](https://www.ncbi.nlm.nih.gov/biosample/) accession ids.

# Table of contents

* [Requirements](#Requirements)
* [Installation](#Installation)
* [Quick start](#Quick-start)
* [Output](#Output)
* [License](#License)


# Requirements

* Linux or MacOS (with the [Bash shell](https://en.wikibooks.org/wiki/Bash_Shell_Scripting#What_is_Bash?), which is the default shell on MacOS and many Linux distributions)
* [Python](https://www.python.org/) 2.7 or Python 3
* [edirect](https://www.ncbi.nlm.nih.gov/books/NBK179288/)
* A computer with internet access via the HTTPS protocol - required for retrieving data from NCBI<br>


# Installation

```bash
git clone https://github.com/AlexOrlek/getNCBImetadata.git
cd getNCBImetadata
```
You should find the getmetadata.py executable script within the repository directory. If you add the path of this directory to your [$PATH variable](https://www.computerhope.com/issues/ch001647.htm), then the executable can be run by calling `getmetadata.py [`*`arguments...`*`]` from any directory location. Note also that the edirect directory must also be available in your $PATH variable.


# Quick start

Metadata can be retrieved by running the following code:

`getmetadata.py -a accessions.txt -t nucleotide -o outdir -e first.last@company.com`

accessions.txt is a text file where the first column contains NCBI accession ids. Either Refseq or Genbank nucleotide accessions can be provided. Nucleotide accessions can be provided in either "accession" or "accession.version" format.<br>
The `-t` flag specifies whether `nucleotide` or	`biosample` accessions are provided in accessions.txt.<br>
The `-e` flag should be your own email address; this is provided to NCBI so that they can monitor usage.

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
* `AccessionVersion`
* Submission data: `Model`, `Package`
* `Description`
* Taxonomic data: `taxonomy_id`, `taxonomy_name`, `OrganismName`
* Affiliation data: `Owner/Name`, `email`, `Contact/Name/First`, `Contact/Name/Last`
* Attribute data: `collection_date`, `host`, `isolation_source`, `sample_type`, `geo_loc_name`, `lat_lon`, `env_broad_scale`,`env_local_scale`,`env_medium`<br>


# License

[MIT License](https://en.wikipedia.org/wiki/MIT_License)
