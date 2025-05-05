# from typing import Literal
# from pathlib import Path
# from domain.ports.tool import ToolProvider
# from frameworks.crewai.tool_provider import CrewAIToolProvider

# class ToolBox:
#     def get_tool_provider(self, feature_path: str, framework: Literal["crewai"]) -> list[ToolProvider]:
#         match framework:
#             case "crewai":
#                 return CrewAIToolProvider()