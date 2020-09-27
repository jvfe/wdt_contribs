# %%
import pandas as pd
from utils import (
    get_complex_portal_datasets,
    return_missing_from_wikidata,
    get_wikidata_item_by_propertyvalue,
)

datasets = get_complex_portal_datasets()

# %%
cov_2 = pd.read_table(datasets["sars-cov-2"])
yeast = pd.read_table(datasets["schizosaccharomyces pombe"])

# %%
cov_2_missing_raw = return_missing_from_wikidata(cov_2)
species = cov_2_missing_raw["Taxonomy identifier"].unique()[0]
cov_2_missing_raw["species_qid"] = get_wikidata_item_by_propertyvalue(
    "P685", int(species)
)
part_of_column = "Identifiers (and stoichiometry) of molecules in complex"
cov_2_missing_raw[part_of_column] = cov_2_missing_raw[part_of_column].str.split("|")
cov_2_missing = cov_2_missing_raw.explode(part_of_column)
cov_2_missing["part_of_quantity"] = cov_2_missing[part_of_column].str.extract(
    r"\(([\d]+)\)", expand=False
)
cov_2_missing["uniprot_id"] = cov_2_missing[part_of_column].str.replace(r"\(.*\)", "")
grouped_quantities = (
    cov_2_missing.groupby(["#Complex ac", "uniprot_id"])
    .agg(part_of_quantity=pd.NamedAgg("part_of_quantity", "count"))
    .reset_index()
)
# %%