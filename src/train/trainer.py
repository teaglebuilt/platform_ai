from typing import TypedDict
import sys
from pydantic import BaseModel

from loaders.data_loader import get_data_loader, DataLoaders


class TrainingCommandLineArguments(TypedDict):
    loader: str


class TrainingArgs(BaseModel):
    source_type: str


class Trainer[T: TrainingArgs]:
    def __init__(self, args: T):
        self.loader = self.determine_loader(args)

    def determine_loader(self, args: T):
        if args.source_type == "repo":
            return get_data_loader(DataLoaders.GIT.value)
        elif args.source_type == "file":
            return get_data_loader(DataLoaders.LOCALDIR.value)
        elif args.source_type == "url":
            return get_data_loader(DataLoaders.URL.value)
        else:
            raise ValueError(f"Unsupported source_type: {args.source_type}")


def get_trainer(entrypoint_args: TrainingCommandLineArguments) -> Trainer:
    training_arguments = TrainingArgs(
        source_type=entrypoint_args["loader"]
    )
    return Trainer[TrainingArgs](training_arguments)


def run_train(training_args) -> None:
    trainer = get_trainer({
        "loader": training_args.loader
    })
    print("trainer", trainer)
