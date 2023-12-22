"""
Script to find genes terms by quering label and synonyms in ontology
"""
import logging
from argparse import ArgumentParser
from pathlib import Path

import pandas as pd
from rdflib import OWL, RDF, RDFS, Graph
from rdflib.plugins.sparql import prepareQuery
from requests import head


def load_ontology(ontology: str) -> Graph:
    """
        Load ontology locally using its purl url
    """
    g = Graph()
    g.parse(location=ontology, format="application/rdf+xml")

    return g


def search_ontology(ontology: Graph, labels: list) -> list:
    """
        Search terms in the ontology
    """
    def expand_filter(labels):
        contains_txt = [f"CONTAINS(STR(?label), '{label}')" for label in labels]
        return f"FILTER({' || '.join(contains_txt)})"

    namespace = {
        "rdf": RDF,
        "owl": OWL,
        "rdfs": RDFS
    }
    simple_query = f"""
        SELECT DISTINCT ?term ?label
        WHERE {{
            ?term rdf:type owl:Class .
            ?term rdfs:label ?label .
            {expand_filter(labels)}
        }}
    """
    q = prepareQuery(
        simple_query,
        initNs=namespace
    )

    qres = ontology.query(q)
    results = [{"term": row.term, "label": row.label} for row in qres]

    return results


def save_results(results: list, output_file: Path):
    """
        Save search result in a CSV file
    """
    df = pd.DataFrame.from_records(results)
    df.to_csv(output_file, index=False)


def main(ontology: str, labels_list: list, output_file: Path):
    """
        Main function
    """
    ont = load_ontology(ontology)
    result = search_ontology(ont, labels_list)
    save_results(result, output_file)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-ont", "--ontology", help="ontology purl")
    parser.add_argument("-l", "--labels", help="txt file with list of labels to search")
    parser.add_argument("-o", "--output", help="csv output file path")

    args = parser.parse_args()

    with head(args.ontology, allow_redirects=True, timeout=600) as res:
        res = res.status_code == 200

    with open(args.labels, "r", encoding="utf-8") as file:
        labels = file.read()

    if not res and not labels:
        logging.error("Ontology doesn't exist and labels file is empty.")

    main(args.ontology, labels.split("\n"), args.output)
