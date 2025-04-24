import typer
import duckdb
from pathlib import Path

cli = typer.Typer()


@cli.command()
def feature():
    pass


@cli.command("memory")
def sync_memory(
    lance_table_path: str = typer.Option(
        "../data/generated/lancedb", help="Path to LanceDB table directory"
    ),
    duckdb_path: str = typer.Option(
        "./data/generated/analytics.db", help="Path to DuckDB database"
    ),
    target_table: str = typer.Option(
        "memory_log", help="DuckDB table to materialize into"
    ),
    preview: bool = typer.Option(False, help="Preview data instead of syncing")
):
    conn = duckdb.connect(duckdb_path)
    conn.execute("INSTALL lance; LOAD lance;")

    # Validate path exists
    if not Path(lance_table_path).exists():
        typer.secho(f"Lance table not found at {lance_table_path}", fg=typer.colors.RED)
        raise typer.Exit(1)

    if preview:
        result = conn.execute(f"SELECT * FROM '{lance_table_path}' LIMIT 5").df()
        typer.echo(result)
    else:
        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {target_table} AS
            SELECT id, text, vector
            FROM '{lance_table_path}'
        """)
        typer.secho(f"Synced {lance_table_path} → {duckdb_path}:{target_table}", fg=typer.colors.GREEN)
