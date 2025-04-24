import os
import yaml
from pathlib import Path
from typing import Union, Any


def parse_yaml(file_path: Path) -> Union[dict[str, Any], list, None]:
    with file_path.open('r') as f:
        return yaml.safe_load(f)


def parse_config(directory: str, config: str):
    if directory:
        config_file_path = os.path.join(directory, config)
    else:
        current_folder = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(current_folder, config)

    if not os.path.exists(config_file_path):
       raise FileNotFoundError(f"file is missing at {config_file_path}")

    manifest = parse_yaml(Path(config_file_path))
    return manifest
