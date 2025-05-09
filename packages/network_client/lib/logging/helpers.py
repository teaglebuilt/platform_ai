import logging
import json
from typing import Any, Dict, Optional


def get_logger(name: Optional[str] = None) -> logging.Logger:
    if name is None:
        return logging.getLogger("unifi_controller_api")
    elif name.startswith("unifi_controller_api"):
        return logging.getLogger(name)
    else:
        return logging.getLogger(f"unifi_controller_api.{name}")


def log_extra_fields(
    logger: logging.Logger,
    obj_name: str,
    obj_id: str,
    extra_fields: Dict[str, Any],
    max_length: int = 300,
):
    if not extra_fields:
        logger.debug(f"No extra fields for {obj_name} {obj_id}")
        return

    truncated_fields = {}
    for key, value in extra_fields.items():
        if isinstance(value, (dict, list)):
            try:
                value_str = json.dumps(value)
                if len(value_str) > max_length:
                    value_str = value_str[:max_length] + "... [truncated]"
                truncated_fields[key] = value_str
            except (TypeError, ValueError):
                truncated_fields[key] = f"<complex structure: {type(value).__name__}>"
        elif isinstance(value, str) and len(value) > max_length:
            truncated_fields[key] = value[:max_length] + "... [truncated]"
        else:
            truncated_fields[key] = value

    logger.debug(
        f"Extra fields for {obj_name} {obj_id}: {json.dumps(truncated_fields, indent=2)}"
    )


def log_api_response(
    logger: logging.Logger,
    url: str,
    response_data: Dict[str, Any],
    status_code: int,
    truncate: bool = True,
    max_length: int = 500,
):
    try:
        response_str = json.dumps(response_data)
        if truncate and len(response_str) > max_length:
            response_str = response_str[:max_length] + "... [truncated]"

        logger.debug(
            f"API Response from {url} (Status: {status_code}):\n{response_str}"
        )
    except (TypeError, ValueError) as e:
        logger.debug(
            f"API Response from {url} (Status: {status_code}) - Error serializing: {e}"
        )
