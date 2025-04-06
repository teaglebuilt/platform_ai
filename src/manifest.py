import os
import yaml
from typing import Literal

def read_yaml_file(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def parse_config(directory: str, config: Literal["agents.yaml", "tasks.yaml"]):
    if directory:
        config_file_path = os.path.join(directory, config)
    else:
        current_folder = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(current_folder, config)
    if os.path.exists(config_file_path):
        manifest = read_yaml_file(config_file_path)
    return manifest


def parse_manifest():
    current_folder = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(current_folder, "soa_manifest.yaml")
    if os.path.exists(config_file_path):
        manifest = read_yaml_file(config_file_path)
    return manifest
