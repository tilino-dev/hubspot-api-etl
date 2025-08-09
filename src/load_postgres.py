import os
from sqlalchemy import create_engine, text
import pandas as pd

TABLE_MAP = {
    "contacts": "hubspot_contacts",
    "deals": "hubspot_deals",
}

def upsert_dataframe(df: pd.DataFrame, table: str, engine):
    if df is None or df.empty:
        return 0
    with engine.begin() as conn:
        temp_table = f"{table}_staging"
        df.to_sql(temp_table, conn, if_exists="replace", index=False)
        pk = "hs_object_id"
        cols = [c for c in df.columns if c != pk]
        set_clause = ", ".join([f"{c}=excluded.{c}" for c in cols])
        insert_sql = f"""
        insert into {table} ({', '.join(df.columns)})
        select {', '.join(df.columns)} from {temp_table}
        on conflict ({pk}) do update set {set_clause};
        drop table {temp_table};
        """
        conn.execute(text(insert_sql))
        return len(df)

def load(dfs: dict):
    db = os.getenv("DB_CONN", "postgresql+psycopg2://user:pass@localhost:5432/dbname")
    engine = create_engine(db, future=True)
    total = 0
    for name, df in dfs.items():
        table = TABLE_MAP.get(name)
        if table:
            total += upsert_dataframe(df, table, engine)
    print(f"Upserted {total} rows into Postgres")
