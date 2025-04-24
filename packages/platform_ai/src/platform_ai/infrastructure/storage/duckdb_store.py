import duckdb
from pathlib import Path
from typing import Any


class DuckDBStore:
    def __init__(self, db_path: str = "./data/duckdb/analytics.db"):
        self.conn = duckdb.connect(db_path)
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    def run_query(self, sql: str) -> Any:
        return self.conn.execute(sql).fetchall()

    def create_table_if_not_exists(self, table_name: str, schema: str):
        self.conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})")
