from modules.custom_io.Boto3Cursor import Boto3Cursor

def persist_results(s3_cursor: Boto3Cursor, **kwargs):
    for key, df in kwargs.items():
        s3_cursor.gravar(key, df)
