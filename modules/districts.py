import os
from io import BytesIO
import geopandas as gpd
import boto3

FILE_KEY = "geoportal_distrito_municipal_v2.geojson"

def get_district_records():
    df_dist_raw = _load()
    return _treat(df_dist_raw)

def _load() -> gpd.GeoDataFrame:
    bucket_name = os.getenv("S3_ORIGIN_BUCKET")
    if bucket_name is None:
        raise Exception("Defina \"S3_ORIGIN_BUCKET\" no .env.")

    s3_client = boto3.client("s3")
    res = s3_client.get_object(Bucket=bucket_name, Key=FILE_KEY)
    code = res["ResponseMetadata"]["HTTPStatusCode"]
    if code != 200:
        raise Exception(f"Não foi possível encontrar \'{FILE_KEY}\' no S3...")

    content = res["Body"].read()
    gdf = gpd.read_file(BytesIO(content))

    # Convertendo de notação métrica (EPSG:31983) para coordenadas (EPSG:4326)
    return gdf.to_crs(epsg=4326)

def _treat(df_dist_raw):
    df_dist_treated = df_dist_raw.drop(columns="id").rename(columns={
        "cd_identificador_distrito": "id", "nm_distrito_municipal": "nome", "nm_regiao_05": "região"
    })[["id", "nome", "região", "geometry"]].copy()
    df_dist_treated["lat"] = df_dist_treated.centroid.x
    df_dist_treated["long"] = df_dist_treated.centroid.y
    df_dist_treated.drop(columns="geometry", inplace=True)
    return df_dist_treated, df_dist_treated.apply(lambda x: tuple(x), axis=1).to_list()