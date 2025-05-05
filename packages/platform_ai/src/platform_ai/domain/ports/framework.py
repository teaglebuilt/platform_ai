from typing import Protocol, TypedDict, Literal, runtime_checkable


class FeatureSettings(TypedDict):
    verbose: bool


class FeatureResult(TypedDict):
    result: str


@runtime_checkable
class AgentFramework(Protocol):
    def run_agent_feature(
        self,
        feature_path: str,
        feature_type: Literal['repo', 'local'],
        feature_settings: FeatureSettings) -> FeatureResult:
        ...
