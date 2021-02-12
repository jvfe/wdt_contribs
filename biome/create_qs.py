import pandas as pd


def main():
    researchers = pd.read_csv("data/biome.csv")

    with open("biome.qs", "w") as qs_file:
        for _, row in researchers.iterrows():

            researc = row["item"]
            affiliation = "|P1416|Q105465464"
            reference = '|S854|"https://bioinfo.imd.ufrn.br/index.php?page=people"'
            retrieved = "|S813|+2021-02-12T00:00:00Z/11"

            current_qs = f"{researc}{affiliation}{reference}{retrieved}\n"
            qs_file.write(current_qs)


if __name__ == "__main__":
    main()
