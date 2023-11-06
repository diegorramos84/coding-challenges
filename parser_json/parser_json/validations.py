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


def check_invalid_escapes_in_json(json_text):
    # Define a regular expression pattern to match JSON string values within double quotes
    string_pattern = re.compile(r'"([^"\\]*(?:\\.[^"\\]*)*)"')

    # Find all string values within double quotes
    matches = string_pattern.findall(json_text)

    invalid_escapes = []

    # Iterate through the matched strings
    for match in matches:
        # Check for invalid escape sequences within the matched string
        invalid_escape_pattern = re.compile(r'\\[^"\\/bfnrtu]')
        invalid_escape_match = invalid_escape_pattern.search(match)

        if invalid_escape_match:
            invalid_escapes.append(match)

    return invalid_escapes


def check_invalid_escaped_tabs_in_json(json_text):
    # Define a regular expression pattern to match JSON string values within double quotes
    string_pattern = re.compile(r'"([^"\\]*(?:\\.[^"\\]*)*)"')

    # Find all string values within double quotes
    matches = string_pattern.findall(json_text)

    invalid_escapes = []

    # Iterate through the matched strings
    for match in matches:
        # Check for unescaped tab characters within the matched string
        if "\t" in match:
            invalid_escapes.append(match)

    return invalid_escapes


def detect_spaces(input_string):
    # Check for spaces in the input string
    problematic_chars = [char for char in input_string if char == " "]

    if problematic_chars:
        raise Exception("SPACES")
    else:
        return True
