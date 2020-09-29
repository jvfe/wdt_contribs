# %%
import pandas as pd
from utils import (
    get_complex_portal_datasets,
    return_missing_from_wikidata,
    get_wikidata_item_by_propertyvalue,
)

datasets = get_complex_portal_datasets()


def process_species_complextab(complextab_dataframe):
    """Clean and process complextab data

    Takes in a complextab dataframe from one of the species datasets,
    removes entries present in Wikidata and processes it into a "long"
    format, more friendly for editing.

    """
    species_missing_raw = return_missing_from_wikidata(complextab_dataframe)

    # Cleaning molecules column, they follow this format: uniprot_id(quantity)|another_uniprot_id(n)...
    molecules_column = "Identifiers (and stoichiometry) of molecules in complex"

    species_missing_raw[molecules_column] = species_missing_raw[
        molecules_column
    ].str.split("|")

    species_missing_raw = species_missing_raw.explode(molecules_column)

    species_missing_raw["has_part_quantity"] = species_missing_raw[
        molecules_column
    ].str.extract(r"\(([\d]+)\)", expand=False)

    species_missing_raw["uniprot_id"] = species_missing_raw[
        molecules_column
    ].str.replace(r"\(.*\)", "")

    # Also need to group the resulting molecules, to avoid duplicates
    species_missing = (
        species_missing_raw.groupby(
            ["#Complex ac", "Recommended name", "Taxonomy identifier", "uniprot_id"]
        )
        .agg(has_part_quantity=pd.NamedAgg("has_part_quantity", "count"))
        .reset_index()
    )

    return species_missing


# %%
cov2_complextab = pd.read_table(datasets["sars-cov-2"], na_values=["-"])
cov2 = process_species_complextab(cov2_complextab)
cov2["found_in_taxon"] = [
    get_wikidata_item_by_propertyvalue("P685", int(taxid))
    for taxid in cov2["Taxonomy identifier"].to_list()
]
cov2["has_part"] = [
    get_wikidata_item_by_propertyvalue("P352", uniprot_id)
    for uniprot_id in cov2["uniprot_id"].to_list()
]

# %%
complex_dfs = [
    cov2[cov2["#Complex ac"] == unique_complex]
    for unique_complex in cov2["#Complex ac"].unique()
]