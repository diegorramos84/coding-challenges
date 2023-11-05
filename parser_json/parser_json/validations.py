import inspect
import re
import sys

from .constants import *


def is_valid_json_file(content):
    content = content.strip()
    try:
        json_not_empty(content)
        starts_with_bracket_or_braces(content)
        return True
    except ValueError as e:
        print(e)
        sys.exit(1)


def json_not_empty(content):
    if not content or content.isspace():
        raise Exception("Error: The JSON file is empty or contains only whitespaces")
    else:
        return True


def starts_with_bracket_or_braces(content):
    wrapped_in_brackets = content.startswith(JSON_LEFTBRACKET) and content.endswith(
        JSON_RIGHTBRACKET
    )
    wrapped_in_braces = content.startswith(JSON_LEFTBRACE) and content.endswith(
        JSON_RIGHTBRACE
    )
    if wrapped_in_braces or wrapped_in_brackets:
        return True
    else:
        raise Exception("Error: The JSON file doest not start and ends with {} por []")


def check_trailing_comma(string):
    if len(string) == 2:
        char = string[0]
        next_char = string[1]
        if (
            char == JSON_COMMA
            and string[1] == JSON_RIGHTBRACE
            or string[1] == JSON_RIGHTBRACKET
        ):
            raise Exception("Error: JSON file cannot have trailing comma")


def find_illegal_escapes(json_string):
    print(json_string, "HRE")
    # pattern2 = r'\\[0-9]|\t|\\(?!["\\/bfnrtu])|\n'
    pattern = r'\\\\[0-9]|\t|\\(?!["\\/bfnrtu])|\n'
    illegal_escapes = re.findall(pattern, json_string)
    if illegal_escapes:
        raise Exception(f"Illegal illegal escapes in string: {illegal_escapes}")
