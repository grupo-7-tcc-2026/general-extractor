import os
from modules import open_meteo, districts
from modules.io import persist_results
from modules.io.Boto3Cursor import Boto3Cursor
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    toggle_open_meteo_stage = os.getenv("OPEN_METEO_STAGE") == "1"
    s3_cursor = Boto3Cursor()
    trusted_dfs ={}

    print("Extrator de Dados V. 2.3")

    print("\tCarregando distritos...")
    distr_df, distr_records = districts.get_district_records(s3_cursor)
    trusted_dfs["trusted_district"] = distr_df

    if toggle_open_meteo_stage:
        trusted_dfs["trusted_climate"] = open_meteo.extract(distr_records)

    print("\tGravando resultados...")
    persist_results.persist_results(s3_cursor, **trusted_dfs)
    print("Concluído!")
