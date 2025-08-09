import os
import pandas as pd
import boto3
from pathlib import Path
from datetime import datetime, timezone

def write_parquet_to_s3(df: pd.DataFrame, bucket: str, key: str):
    if df is None or df.empty:
        return
    tmp = Path("/tmp/out.parquet")
    df.to_parquet(tmp, index=False)
    s3 = boto3.client("s3")
    s3.upload_file(str(tmp), bucket, key)

def load_to_s3(dfs: dict):
    bucket = os.getenv("S3_BUCKET")
    prefix = os.getenv("S3_PREFIX", "hubspot_export")
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for name, df in dfs.items():
        key = f"{prefix}/{name}/dt={ts}/{name}.parquet"
        write_parquet_to_s3(df, bucket, key)
        print(f"Uploaded s3://{bucket}/{key}")
