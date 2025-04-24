import duckdb
import lancedb

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
    lance_table_path: str = "./data/generated/lancedb",
    duckdb_path: str = "./data/generated/analytics.db",
    table_name: str = "memory",
    duckdb_table: str = "memory_log"
):
    db = lancedb.connect(lance_table_path)
    table = db.open_table(table_name)
    arrow_table = table.to_arrow()

    conn = duckdb.connect(duckdb_path)

    conn.register("lance_mem", arrow_table)
    conn.execute(f"""
        CREATE OR REPLACE TABLE {duckdb_table} AS
        SELECT * FROM lance_mem
    """)

    print(f"✅ Migrated {len(arrow_table)} rows from LanceDB:{table_name} → DuckDB:{duckdb_table}")
