## Gene Finder

### Install

Create virtual envirement:

`python -m venv venv`

Install requirements:

`pip install -r requirements.txt`

### Using gene-finder script

Run command passing ontology purl URL, file with list of labels and output path for a csv file. Check `test/genes.txt` for an example.

`python gene_finder.py --ontology http://purl.obolibrary.org/obo/rbo.owl --labels tests/genes.txt --output test/terms.csv`