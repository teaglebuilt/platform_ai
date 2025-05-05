from dataclasses import dataclass
from typing import Literal

from platform_ai.domain.ports.framework import AgentFramework

FeatureType = Literal["repo", "local"]

@dataclass
class AgentFeature:
    framework: AgentFramework

    def execute(self, feature_path: str, feature_type: FeatureType):
        return self.framework.run_agent_feature(
            feature_path=feature_path,
            feature_type=feature_type,
            feature_settings={"verbose": True}
        )
