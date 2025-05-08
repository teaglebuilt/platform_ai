import duckdb
import lancedb
import pyarrow as pa
from pathlib import Path

from platform_ai.infra.storage.lancedb_store import LanceDBStore
from platform_ai.infra.storage.duckdb_store import DuckDBStore


def get_store(type: str):
    match type.lower():
        case "vector" | "memory" | "lancedb":
            return LanceDBStore()
        case "analytics" | "dashboard" | "duckdb":
            return DuckDBStore()
        case _:
            raise ValueError(f"Unknown store type: {type}")


def migrate_lance_to_duckdb(
    lance_db_path: str,
    duckdb_path: str,
):
    db = lancedb.connect(lance_db_path)

    for lance_table_name in db.table_names():
        table = db.open_table(lance_table_name)
        arrow_table = pa.Table.from_pydict(table.to_arrow().to_pydict())
        duckdb_table_name = table.name

        conn = duckdb.connect(duckdb_path)

        conn.register(duckdb_table_name, arrow_table)
        conn.execute(f"""
            CREATE OR REPLACE TABLE {duckdb_table_name} AS
            SELECT * FROM {duckdb_table_name}
        """)

        print(f"✅ Migrated {len(arrow_table)} rows from LanceDB:{lance_table_name} → DuckDB:{duckdb_table_name}")
    print(f"✅ Completed Migrating {len(list(db.table_names()))} rows from LanceDB → DuckDB")