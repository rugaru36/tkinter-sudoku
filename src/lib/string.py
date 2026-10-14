from enum import Enum
import logging
from typing import Literal, TypeVar, cast, get_args

def safe_str_to_int(str: str, to_log_error: bool = False):
    try:
        val = int(str)
        return val
    except ValueError:
        if to_log_error:
            logging.exception('')
        return None

T = TypeVar("T", bound=Enum)

def safe_str_to_enum(s: str, enum: type[T]) -> T | None:
    try:
        return enum(s)
    except ValueError:
        return None
