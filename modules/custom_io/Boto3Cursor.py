import os
from io import BytesIO, StringIO
import boto3
import pandas as pd
import geopandas as gpd
from botocore.client import BaseClient

class Boto3Cursor:

    cursor: BaseClient
    origin_bucket_name: str
    target_bucket_name: str

    def __init__(self):
        origin_bucket_name_env = os.getenv("S3_ORIGIN_BUCKET")
        target_bucket_name_env = os.getenv("S3_TARGET_BUCKET")

        if origin_bucket_name_env is None or target_bucket_name_env is None:
            raise EnvironmentError("Defina as variáveis de .env dos BUCKETs")

        self.origin_bucket_name = origin_bucket_name_env
        self.target_bucket_name = target_bucket_name_env
        self.cursor = boto3.client("s3")

    def _ler(self, file_key: str) -> bytes:
        res = self.cursor.get_object(Bucket=self.origin_bucket_name, Key=file_key)
        code = res["ResponseMetadata"]["HTTPStatusCode"]
        if code != 200:
            raise FileNotFoundError(f"Não foi possível encontrar \'{file_key}\' no S3...")

        return res["Body"].read()

    def ler_df(self, file_key: str) -> pd.DataFrame:
        found_bytes = self._ler(file_key)
        return pd.read_file(BytesIO(found_bytes))

    def ler_gdf(self, file_key: str) -> pd.DataFrame:
        found_bytes = self._ler(file_key)
        return gpd.read_file(BytesIO(found_bytes)).to_crs(epsg=4326)

    def gravar(self, file_key: str, df: pd.DataFrame):
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False, sep="|")
        self.cursor.put_object(
            Bucket=self.target_bucket_name, Key=f"{file_key}.csv", Body=csv_buffer.getvalue()
        )
