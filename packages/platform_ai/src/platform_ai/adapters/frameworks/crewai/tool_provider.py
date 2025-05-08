from typing import Literal

from crewai.tools import BaseTool

from platform_ai.adapters.frameworks.crewai.tools.repo_reader import LocalRepoReaderTool


class CrewAIToolProvider:
    def get_tools(self, type: Literal["repo", "local"], path: str) -> list[BaseTool]:
        match type:
            case "repo":
                repo_tool = LocalRepoReaderTool(directory=path)
                return [repo_tool]
            case "local":
                return []
            case _:
                raise ValueError(f"Unsupported tool type: {type}")
