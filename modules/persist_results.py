import io
import os
import boto3
import pandas as pd


def persist_results(**kwargs):
    bucket_name, cursor = _load_cursor()
    for key, df in kwargs.items():
        _persist_df(cursor, bucket_name, f"{key}.csv", df)

def _load_cursor():
    bucket_name = os.getenv("S3_TARGET_BUCKET")
    if bucket_name is None:
        raise Exception("Defina \"S3_TARGET_BUCKET\" no .env.")

    return bucket_name, boto3.client("s3")

def _persist_df(client, bucket_name, key, df: pd.DataFrame):
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    client.put_object(Bucket=bucket_name, Key=key, Body=csv_buffer.getvalue())
