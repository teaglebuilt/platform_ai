from pathlib import Path
from typing import Literal
from domain.ports.framework import AgentFramework, FeatureResult, FeatureSettings
from infrastructure.frameworks.crewai.crewai_loader import construct_crew_from_config


class CrewAdapter(AgentFramework):

    def run_agent_feature(
        self,
        feature_path: str,
        feature_type: Literal['repo'],
        feature_settings: FeatureSettings
    ) -> FeatureResult:
        construct_crew_from_config(
            type=feature_type,
            config_dir=Path(feature_path),
            verbose=feature_settings.get("verbose", True)
        )
        return {"result": ""}
