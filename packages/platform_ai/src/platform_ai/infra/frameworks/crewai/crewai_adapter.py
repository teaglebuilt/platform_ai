from pathlib import Path
from typing import Literal
from platform_ai.domain.ports.framework import AgentFramework, FeatureResult, FeatureSettings
from platform_ai.infra.frameworks.crewai.crewai_loader import construct_crew_from_config
from platform_ai.infra.frameworks.crewai.tool_provider import CrewAIToolProvider


class CrewAdapter(AgentFramework):

    def __init__(self) -> None:
        self.tool_provider = CrewAIToolProvider()

    def run_agent_feature(
        self,
        feature_path: str,
        feature_type: Literal['repo'],
        feature_settings: FeatureSettings
    ) -> FeatureResult:
        feature_crew = construct_crew_from_config(
            type=feature_type,
            config_dir=Path(feature_path),
            tools=self.tool_provider.get_tools(feature_type),
            verbose=feature_settings.get("verbose", True)
        )
        feature_crew.kickoff()
        return {"result": ""}
