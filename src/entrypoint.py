import sys
import json
import argparse
from pathlib import Path

from train.trainer import run_train
from loaders.crew_loader import construct_crew_from_config


def run_main(args=sys.argv[1:]) -> None:
    parser = argparse.ArgumentParser(description='Main entrypoint')

    subparsers = parser.add_subparsers(dest='command')
    feature_parser = subparsers.add_parser('feature', help='run ai feature')
    feature_parser.add_argument('--path', required=False)
    feature_parser.add_argument('--verbose', required=False)

    train_parser = subparsers.add_parser('train', help='running training iteration')
    train_parser.add_argument('--loader', required=True)

    parsed_args = parser.parse_args(args)
    if parsed_args.command == 'train':
        run_train(parsed_args)
    if parsed_args.command == 'feature':
        feature_path = parsed_args.path
        verbose = parsed_args.verbose
        feature_crew = construct_crew_from_config(type="repo", config_dir=Path(feature_path), verbose=verbose or True)
        print("crew", feature_crew)
        result = feature_crew.kickoff()
        print(f"Raw Output: {result.raw}")
        if result.json_dict:
            print(f"JSON Output: {json.dumps(result.json_dict, indent=2)}")
        if result.pydantic:
            print(f"Pydantic Output: {result.pydantic}")
        print(f"Tasks Output: {result.tasks_output}")
        print(f"Token Usage: {result.token_usage}")


if __name__ == "__main__":
    run_main(sys.argv)
