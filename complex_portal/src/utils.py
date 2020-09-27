from wikidataintegrator import wdi_core
from wikidata2df import wikidata2df
from collections import defaultdict
from functools import lru_cache, reduce
from ftplib import FTP
import pandas as pd


def get_wikidata_complexes():

    get_macromolecular = """
    SELECT ?item ?ComplexPortalID
    WHERE 
    {
    ?item wdt:P7718 ?ComplexPortalID .
    }"""
    wikidata_complexes = wikidata2df(get_macromolecular)

    return wikidata_complexes


@lru_cache(maxsize=None)
def get_wikidata_species(ncbi_tax_id):

    query_result = wdi_core.WDItemEngine.execute_sparql_query(
        f'SELECT distinct ?item WHERE {{ ?item wdt:P685 "{ncbi_tax_id}" }}'
    )
    try:
        match = query_result["results"]["bindings"][0]
    except ValueError:
        raise Exception("Couldn't find item for this tax id")
    qid = match["item"]["value"]

    qid = qid.split("/")[4]
    return qid


def get_complex_portal_datasets():

    domain = "ftp.ebi.ac.uk"
    complex_data = "pub/databases/intact/complex/current/complextab/"

    ftp = FTP(domain)
    ftp.login()
    ftp.cwd(complex_data)
    files = ftp.nlst()

    cp_datasets = defaultdict()

    string_replacements = (".tsv", ""), ("_", " ")

    for species in files:
        if "README" not in species:

            current_key = reduce(
                lambda a, kv: a.replace(*kv), string_replacements, species
            )

            cp_datasets[current_key] = f"ftp://{domain}/{complex_data}{species}"

    return cp_datasets


def return_missing_from_wikidata(complexp_dataframe):

    wikidata_complexes = get_wikidata_complexes()

    merged_data = pd.merge(
        wikidata_complexes,
        complexp_dataframe,
        how="outer",
        left_on=["ComplexPortalID"],
        right_on=["#Complex ac"],
        indicator=True,
    )
    missing_from_wikidata = merged_data[merged_data["_merge"] == "right_only"][
        complexp_dataframe.columns
    ]

    return missing_from_wikidata