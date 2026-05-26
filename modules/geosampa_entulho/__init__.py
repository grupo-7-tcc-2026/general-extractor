import pandas as pd
from modules.custom_io.Boto3Cursor import Boto3Cursor

FILE_KEY = "geoportal_sac_remocao_entulho.geojson"

def extrair(s3_cursor: Boto3Cursor, distr_df: pd.DataFrame):
    df_entulho_raw = s3_cursor.ler_gdf(FILE_KEY)

    df_entulho = df_entulho_raw.drop(columns="id").rename(columns={
        "cd_identificador": "id", "dt_abertura": "dt_solicitacao", "tx_situacao_solicitacao": "status" ,
        "dc_tema": "tema", "dc_servico": "servico", "dc_assunto": "assunto", "dt_parecer": "dt_coleta"
    })[["id", "dt_solicitacao", "status", "tema", "servico", "assunto", "dt_coleta", "geometry"]].copy()

    juncao = df_entulho.merge(distr_df, how="cross", suffixes=("", "_distrito"))
    juncao = juncao[juncao.apply(lambda x: x["geometry_distrito"].contains(x["geometry"]), axis=1)]

    return juncao.rename(columns={"nome": "nome_distrito"}).drop(columns=["geometry_distrito", "lat", "long"])