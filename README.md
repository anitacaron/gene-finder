## Gene Finder

Find terms using a label. For the moment, it's only looking at the label, not at the synonym.

### Install

1. Clone repository, change to gene-finder folder.

2. Create virtual envirement:

`python -m venv venv`

3. Install requirements:

`pip install -r requirements.txt`

### Using gene-finder script

Run command passing ontology purl URL, file with list of labels and output path for a csv file. Check `test/genes.txt` for an example.

`python gene_finder.py --ontology http://purl.obolibrary.org/obo/rbo.owl --labels tests/genes.txt --output test/terms.csv`
