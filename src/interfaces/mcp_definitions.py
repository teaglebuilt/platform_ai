from typing import TypedDict
from dataclasses import dataclass

class ErrorDetailsNested(TypedDict, total=False):
    """Type definition for nested error details."""

    command: str
    exit_code: int
    stderr: str


class ErrorDetails(TypedDict, total=False):
    """Type definition for detailed error information matching the spec."""

    message: str
    code: str
    details: ErrorDetailsNested


@dataclass
class CommandHelpResult:
    """Type definition for command help results."""

    help_text: str
    status: str = "success"
    error: ErrorDetails | None = None