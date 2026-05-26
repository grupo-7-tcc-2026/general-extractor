import os
from modules import open_meteo, persist_results, districts
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    toggle_open_meteo_stage = os.getenv("OPEN_METEO_STAGE") == "1"
    trusted_dfs ={}

    print("Extrator de Dados V. 2.2")

    print("\tCarregando distritos...")
    distr_df, distr_records = districts.get_district_records()
    trusted_dfs["trusted_district"] = distr_df

    if toggle_open_meteo_stage:
        trusted_dfs["trusted_climate"] = open_meteo.extract(distr_records)

    print("\tGravando resultados...")
    persist_results.persist_results(**trusted_dfs)
    print("Concluído!")
