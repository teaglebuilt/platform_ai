from typing import TypeVar, Generic
import sys
from pydantic import BaseModel

from loaders import get_loader, Loaders

A = TypeVar("A", bound=BaseModel)


class Trainer(Generic[A]):
    def __init__(self, args: A):
        self.args = args
        self.loader = self.determine_loader(args)

    def determine_loader(self, args: A):
        if args.source_type == "repo":
            return get_loader(Loaders.GIT)
        elif args.source_type == "file":
            return get_loader(Loaders.LOCALDIR)
        elif args.source_type == "url":
            return get_loader(Loaders.URL)
        else:
            raise ValueError(f"Unsupported source_type: {args.source_type}")


def get_trainer(args: list[str]) -> Trainer:
    return Trainer(args=args)


def run_train(args=sys.argv) -> None:
    trainer = get_trainer(args)
    print("trainer", trainer)


if __name__ == "__main__":
    import sys
    run_train(sys.argv)
