import typer
from pathlib import Path
from typing import cast
from platform_ai.infra.storage.store_helpers import migrate_lance_to_duckdb
from platform_ai.infra.frameworks.registry import select_framework
from platform_ai.application.use_cases.agent_feature import AgentFeature, FeatureType

cli = typer.Typer()


@cli.command("feature")
def agent_feature(
    framework: str = typer.Option(default="crewai", help="agent framework to use"),
    feature_type: str = typer.Option(default="repo", help="type of feature"),
    feature_path: str = typer.Argument(..., help="path to feature config")
):
    framework_type = select_framework(framework)
    feature = AgentFeature(framework=framework_type)

    feature.execute(feature_path=feature_path, feature_type=cast(FeatureType, feature_type))


@cli.command("memory")
def sync_memory(
    lance_table_path: str = typer.Option(
        "./generated/lancedb", help="Path to LanceDB table directory"
    ),
    duckdb_path: str = typer.Option(
        "./generated/analytics.db", help="Path to DuckDB database"
    ),
    target_table: str = typer.Option(
        "memory", help="DuckDB table to materialize into"
    )
):
    if not Path(lance_table_path).exists():
        typer.secho(f"Lance table not found at {lance_table_path}", fg=typer.colors.RED)
        raise typer.Exit(1)

    migrate_lance_to_duckdb(
        lance_table_path=lance_table_path,
        duckdb_path=duckdb_path,
        table_name=target_table or "memory",
        duckdb_table="memory"
    )
