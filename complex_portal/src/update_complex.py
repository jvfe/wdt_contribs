# %%
import pandas as pd
from utils import (
    get_complex_portal_datasets,
    return_missing_from_wikidata,
    get_wikidata_species,
)

datasets = get_complex_portal_datasets()

# %%
cov_2 = pd.read_table(datasets["sars-cov-2"])
yeast = pd.read_table(datasets["schizosaccharomyces pombe"])

# %%
cov_2_missing = return_missing_from_wikidata(cov_2)
species = cov_2_missing["Taxonomy identifier"].unique()[0]
cov_2_missing["species_qid"] = get_wikidata_species(species)
