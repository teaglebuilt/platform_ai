from typing import Type, ClassVar, Any, Optional
from pathlib import Path
import fnmatch

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from langchain_core.documents import Document


class DirectoryReaderInput(BaseModel):
    """Input schema for CustomDirectoryReaderTool."""
    directory: str = Field(default=".", description="Path to the directory to read")


class LocalRepoReaderTool(BaseTool):
    name: str = "CustomDirectoryReaderTool"
    description: str = "Reads clean source files from the repo, excluding .git, __pycache__, .venv, etc."
    args_schema: Type[BaseModel] = DirectoryReaderInput
    directory: Optional[str] = None

    exclude_dirs: ClassVar[set[str]] = {".git", ".venv", "__pycache__", "node_modules", ".vscode", "dist", "build"}
    exclude_files: ClassVar[set[str]] = {"*.pyc", "*.log", "*.sqlite3", "*.db", "*.lock", "*.tmp"}

    def __init__(self, directory: str, **kwargs):
        super().__init__(**kwargs)
        self.directory = directory

    def _is_excluded_dir(self, path: Path) -> bool:
        return any(part in self.exclude_dirs for part in path.parts)

    def _is_excluded_file(self, path: Path) -> bool:
        return any(fnmatch.fnmatch(path.name, pattern) for pattern in self.exclude_files)

    def _read_file(self, path: Path) -> str | None:
        try:
            return path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"⚠️ Skipped unreadable file: {path} ({e})")
            return None

    def _run(self, **kwargs: Any) -> list[Document] | str:
        directory = kwargs.get("directory", self.directory)
        if directory is None:
            return "Error: No path to repo provided. Please provide a directory path either in the constructor or as an argument."

        root = Path(directory)
        documents = []

        for path in root.rglob("*"):
            if path.is_dir() or self._is_excluded_dir(path) or self._is_excluded_file(path):
                continue

            content = self._read_file(path)
            if content:
                documents.append(Document(page_content=content, metadata={"source": str(path)}))

        return documents
