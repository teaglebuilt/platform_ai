import os
import yaml
from typing import cast
from pathlib import Path

import typer

from platform_ai.infra.storage.store_helpers import migrate_lance_to_duckdb
from platform_ai.adapters.frameworks.registry import select_framework
from platform_ai.application.use_cases.agent_feature import AgentFeature, FeatureType
from platform_ai.application.services.project_indexer import initialize

cli = typer.Typer()


@cli.command("init")
def initialize_platform():
    platform_config = Path(os.path.expanduser("~")) / ".platform" / "config.yaml"
    platform_config.parent.mkdir(parents=True, exist_ok=True)

    # if not platform_config.exists():
    #     raise FileNotFoundError(f"Platform config not found at {platform_config}")

    # config = yaml.safe_load(platform_config.read_text())
    initialize()
    watch_list = []
    ## create path if does not exist ^^^
    ## if organization then check for .git in sub folders of the path to index unless excluded.
    ## watchdog should watch all of them and manage synchronization
    """
    projects:
      homelab:
        type: repo
        path: github.com/teaglebuilt/homelab
      platform_ai:
        type: repo
        path: github.com/teaglebuilt/platform_ai
      realview:
        type: organization
        path: github.com/organizations/realview
        exclude: ""
    """


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
    lance_db_path: str = typer.Option(
        "/generated/lancedb", help="Path to LanceDB table directory"
    ),
    duckdb_path: str = typer.Option(
        "/data/generated/analytics.db", help="Path to DuckDB database"
    )
):
    if not Path(lance_db_path).exists():
        typer.secho(f"Lance db not found at {lance_db_path}", fg=typer.colors.RED)
        raise typer.Exit(1)

    migrate_lance_to_duckdb(
        lance_db_path=lance_db_path,
        duckdb_path=duckdb_path,
    )
