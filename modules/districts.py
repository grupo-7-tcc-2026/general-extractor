from modules.custom_io.Boto3Cursor import Boto3Cursor

FILE_KEY = "geoportal_distrito_municipal_v2.geojson"

def get_district_records(s3_cursor: Boto3Cursor):
    df_dist_raw = s3_cursor.ler_gdf(FILE_KEY).to_crs(epsg=4326)
    return _treat(df_dist_raw)

def _treat(df_dist_raw):
    df_dist_treated = df_dist_raw.drop(columns="id").rename(columns={
        "cd_identificador_distrito": "id", "nm_distrito_municipal": "nome", "nm_regiao_05": "região"
    })[["id", "nome", "região", "geometry"]].copy()
    df_dist_treated["lat"] = df_dist_treated.centroid.x
    df_dist_treated["long"] = df_dist_treated.centroid.y
    return df_dist_treated, df_dist_treated.apply(lambda x: tuple(x), axis=1).to_list()
