# getNCBImetadata
Retrieves NCBI metadata from [nucleotide](https://www.ncbi.nlm.nih.gov/nucleotide/) or [biosample](https://www.ncbi.nlm.nih.gov/biosample/) accession ids.

# Table of contents

* [Requirements](#Requirements)
* [Installation](#Installation)
* [Quick start](#Quick-start)
* [License](#License)


# Requirements

* Linux or MacOS (with the [Bash shell](https://en.wikibooks.org/wiki/Bash_Shell_Scripting#What_is_Bash?), which is the default shell on MacOS and many Linux distributions)
* [Python](https://www.python.org/) 2.7 or Python 3
* [edirect](https://www.ncbi.nlm.nih.gov/books/NBK179288/)<br>


# Installation

```bash
git clone https://github.com/AlexOrlek/getNCBImetadata.git
cd getNCBImetadata
```
You should find the getmetadata.py executable script within the repository directory. If you add the path of this directory to your [$PATH variable](https://www.computerhope.com/issues/ch001647.htm), then \
the executable can be run by calling `getmetadata.py [`*`arguments...`*`]` from any directory location. Note also that the edirect directory must also be available in your $PATH variable.


# Quick start

Metadata can be retrieved by running the following code:

`getmetadata.py -a accessions.txt -t nucleotide -o outdir -e first.last@company.com`

accessions.txt is a text file where the firt column contains NCBI accession ids. Either Refseq or Genbank nucleotide accessions can be provided.<br>
The `-t` flag specifies whether `nucleotide` or	`biosample` accessions are provided in accessions.txt.<br>
The `-e` flag should be your own email address; this is provided to NCBI so that they can monitor usage.

# License

[MIT License](https://en.wikipedia.org/wiki/MIT_License)
