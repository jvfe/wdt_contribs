# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Cadastrando pesquisadores de universidades públicas brasileiras no Wikidata
#
# Como primeiro caso, iremos utilizar a UFRN, visto que a instituição fornece um portal de [dados abertos](http://dados.ufrn.br/) de fácil acesso e migração.
# Os dados já foram reconciliados usando OpenRefine (22/08/20).
# %%
import pandas as pd

# %%
ufrn = pd.read_csv("../results/pesquisadores_ufrn_reconciled.csv")

# %% [markdown]
# Primeiro vamos só migrar a informação para pesquisadores que já tem páginas.
# %%
com_item = ufrn.copy().dropna(subset=["pesquisador_qid"])


# %% [markdown]
# Vamos adicionar P106 (Ocupação) igual a Q1650915 (Pesquisador),
# P108 (Empregador) igual a Q3847505 (UFRN)
# e referenciar (S854) o portal de dados abertos como a fonte.

# %%
with open("../results/item_exists.qs", "w") as qs_file:
    for _, row in com_item.iterrows():

        nome = f'{row["pesquisador_qid"]}|Lpt-br|"{row["nome"]}"\n'
        ocupacao = f"{row['pesquisador_qid']}|P106|Q1650915\n"
        empregador = f'{row["pesquisador_qid"]}|P108|Q3847505|S854|"http://dados.ufrn.br/dataset/pesquisadores"|S813|+2020-08-22T00:00:00Z/11'

        qs_file.writelines([nome, ocupacao, empregador, "\n"])
