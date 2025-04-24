from infrastructure.storage.lancedb_store import LanceDBStore
from infrastructure.storage.duckdb_store import DuckDBStore


def get_store(type: str):
    match type.lower():
        case "vector" | "memory" | "lancedb":
            return LanceDBStore()
        case "analytics" | "dashboard" | "duckdb":
            return DuckDBStore()
        case _:
            raise ValueError(f"Unknown store type: {type}")
