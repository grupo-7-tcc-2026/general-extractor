from io import BytesIO
from modules.io.Boto3Cursor import Boto3Cursor
import geopandas as gpd

FILE_KEY = "geoportal_distrito_municipal_v2.geojson"

def get_district_records(s3_cursor: Boto3Cursor):
    found_bytes = s3_cursor.ler(FILE_KEY)
    df_dist_raw = gpd.read_file(BytesIO(found_bytes)).to_crs(epsg=4326)
    return _treat(df_dist_raw)

def _treat(df_dist_raw):
    df_dist_treated = df_dist_raw.drop(columns="id").rename(columns={
        "cd_identificador_distrito": "id", "nm_distrito_municipal": "nome", "nm_regiao_05": "região"
    })[["id", "nome", "região", "geometry"]].copy()
    df_dist_treated["lat"] = df_dist_treated.centroid.x
    df_dist_treated["long"] = df_dist_treated.centroid.y
    df_dist_treated.drop(columns="geometry", inplace=True)
    return df_dist_treated, df_dist_treated.apply(lambda x: tuple(x), axis=1).to_list()
