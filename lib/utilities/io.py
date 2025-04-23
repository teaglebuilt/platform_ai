import yaml
from pathlib import Path
from typing import Union, Any


def parse_yaml(file_path: Path) -> Union[dict[str, Any], list, None]:
    with file_path.open('r') as f:
        return yaml.safe_load(f)
