# %%
from wikidataintegrator import wdi_core

# %%
my_first_wikidata_item = wdi_core.WDItemEngine(wd_item_id="Q5")
my_first_wikidata_item.get_wd_json_representation()

# %%
# Thanks Tiago
def get_wikidata_item(wikidata_property, value):
    query_result = wdi_core.WDItemEngine.execute_sparql_query(
        f'SELECT distinct ?item WHERE {{ ?item wdt:{wikidata_property} "{value}" }}'
    )
    try:
        match = query_result["results"]["bindings"][0]
    except:
        return "not found"
    qid = match["item"]["value"]

    qid = qid.split("/")[4]
    return qid


# %%
get_wikidata_item("P356", "10.1101/2020.03.16.993386")
