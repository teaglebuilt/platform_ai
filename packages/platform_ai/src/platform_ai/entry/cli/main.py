import typer
import duckdb
from pathlib import Path

from platform_ai.infra.storage.store_helpers import migrate_lance_to_duckdb

cli = typer.Typer()


@cli.command()
def feature():
    pass


@cli.command("memory")
def sync_memory(
    lance_table_path: str = typer.Option(
        "./data/generated/lancedb", help="Path to LanceDB table directory"
    ),
    duckdb_path: str = typer.Option(
        "./data/generated/analytics.db", help="Path to DuckDB database"
    ),
    target_table: str = typer.Option(
        "memory_log", help="DuckDB table to materialize into"
    )
):
    if not Path(lance_table_path).exists():
        typer.secho(f"Lance table not found at {lance_table_path}", fg=typer.colors.RED)
        raise typer.Exit(1)

    migrate_lance_to_duckdb(
        lance_table_path=lance_table_path,
        duckdb_path=duckdb_path,
        table_name=target_table or "memory",
        duckdb_table="memory_log"
    )
