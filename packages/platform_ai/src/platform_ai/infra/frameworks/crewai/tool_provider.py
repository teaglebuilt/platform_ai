from typing import Literal

from crewai.tools import BaseTool
from crewai_tools import FileReadTool

from platform_ai.infra.frameworks.crewai.tools.repo_reader import LocalRepoReaderTool


class CrewAIToolProvider:
    def get_tools(self, type: Literal["repo", "local"]) -> list[BaseTool]:
        match type:
            case "repo":
                repo_tool = LocalRepoReaderTool()
                file_tool = FileReadTool()
                return [repo_tool, file_tool]
            case "local":
                return []
            case _:
                raise ValueError(f"Unsupported tool type: {type}")
