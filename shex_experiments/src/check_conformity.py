from pyshex.shex_evaluator import ShExEvaluator
from pyshex.user_agent import SlurpyGraphWithAgent
from pyshex.utils.sparql_query import SPARQLQuery
import pandas as pd


def test_query_against_shex(schema, sparql):

    endpoint = "https://query.wikidata.org/sparql"

    result_list = []
    for r in ShExEvaluator(
        SlurpyGraphWithAgent(endpoint),
        schema,
        SPARQLQuery(endpoint, sparql).focus_nodes(),
    ).evaluate():
        conforms = True if r.result else False
        result_list.append([r.focus, conforms, r.reason])

    result_df = pd.DataFrame.from_records(
        result_list, columns=["item", "conforms", "reason"]
    )
    return result_df


if __name__ == "__main__":

    sparql = "SELECT * WHERE { ?item wdt:P31 wd:Q189118 .} LIMIT 20"

    with open("../shex/cell_type.sx") as shex_file:
        schema = shex_file.read()

    res = test_query_against_shex(schema, sparql)