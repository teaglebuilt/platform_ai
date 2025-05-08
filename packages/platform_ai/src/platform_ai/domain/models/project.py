from pathlib import Path
from typing import Annotated
from pydantic import BaseModel


class Project(BaseModel):
    name: str
    path: Annotated[Path, "local path of git repository"]
    remote_url: Annotated[str, "remote url of git repository"]
