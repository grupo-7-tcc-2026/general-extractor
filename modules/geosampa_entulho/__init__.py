import pandas as pd
from modules.custom_io.Boto3Cursor import Boto3Cursor

FILE_KEY = "geoportal_sac_remocao_entulho.geojson"

def extrair(s3_cursor: Boto3Cursor, distr_df: pd.DataFrame):
    df_entulho_raw = s3_cursor.ler_gdf(FILE_KEY)
    pass