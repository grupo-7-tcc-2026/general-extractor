from io import StringIO
import boto3
import pandas as pd
from botocore.client import BaseClient
from entities import Entity


class Boto3Cursor:

    cursor: BaseClient

    def __init__(self):
        self.cursor = boto3.client("s3")

    def ler(self, entity: Entity) -> bytes:
        res = self.cursor.get_object(
            Bucket=entity.bucket.bucket_name, Key=entity.key
        )
        code = res["ResponseMetadata"]["HTTPStatusCode"]
        if code != 200:
            raise FileNotFoundError(f"Não foi possível encontrar \'{entity.key}\' no S3...")
        return res["Body"].read()

    def gravar(self, entity: Entity, df: pd.DataFrame):
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False, sep="|")
        self.cursor.put_object(
            Bucket=entity.bucket.bucket_name, Key=f"{entity.key}.csv", Body=csv_buffer.getvalue()
        )
