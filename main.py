import os
from modules import open_meteo, districts, geosampa_entulho
from modules.custom_io import persist_results
from modules.custom_io.Boto3Cursor import Boto3Cursor
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    toggle_open_meteo_stage = os.getenv("OPEN_METEO_STAGE") == "1"
    toggle_litter_stage = os.getenv("LITTER_STAGE") == "1"
    s3_cursor = Boto3Cursor()
    trusted_dfs ={}

    print("Extrator de Dados V. 2.4.1\n")

    print("\tEtapa distritos...")
    distr_df, distr_records = districts.get_district_records(s3_cursor)
    trusted_dfs["trusted_district"] = distr_df.drop(columns="geometry")
    print("\tEtapa concluída\n")

    if toggle_open_meteo_stage:
        trusted_dfs["trusted_climate"] = open_meteo.extract(distr_records)

    if toggle_litter_stage:
        trusted_dfs["trusted_litter"] = geosampa_entulho.extrair(s3_cursor, distr_df)

    print("\tGravando resultados...")
    persist_results.persist_results(s3_cursor, **trusted_dfs)
    print("Concluído!")
