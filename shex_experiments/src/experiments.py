from wikidata2df import wikidata2df
from pyshex import ShExEvaluator
from rdflib import Graph
from tqdm import tqdm


def validate_items(schema, sparql):

    items_to_validate = wikidata2df(sparql)["item"].to_list()
    results = []
    for item in tqdm(items_to_validate):
        entity_url = f"http://www.wikidata.org/entity/{item}"

        rdfdata = Graph()
        rdfdata.parse(f"{entity_url}.ttl")

        for result in ShExEvaluator(
            rdf=rdfdata,
            schema=schema,
            focus=entity_url,
        ).evaluate():
            shex_result = dict()
            if result.result:
                shex_result["result"] = True
            else:
                shex_result["result"] = False
            shex_result["reason"] = result.reason

        results.append([item, shex_result["result"], shex_result["reason"]])

    return results