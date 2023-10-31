import ast
import re
import sys

import typer
from typing_extensions import Annotated

app = typer.Typer()

MAX_ALLOWED_DEPTH = 10


def is_valid_json(content):
    if not content or content.isspace():
        return False

    stack = []  # Stack to keep track of opening and closing brackets
    in_string = False  # Flag to indicate if we are inside a string
    escape = False  # Flag to indicate if the current character is escaped
    last_char = ""
    depth = 0

    # check if jason starts with "" instead of {} or []
    is_payload_string = content.startswith('"') and content.endswith('"')

    for char in content:
        if in_string:
            if char == "\\" and not escape:
                escape = True
            elif char == "'" and not escape:
                return False  # Return False if single quotes are used around strings
            elif char == '"' and not escape:
                in_string = False
            else:
                escape = False
        else:
            if char in ('"'):
                in_string = True
            elif char in ("{", "[", "("):
                stack.append(char)
                depth += 1  # increment nesting depth by 1
            elif char in ("}", "]", ")"):
                if not stack:
                    return False
                opening_bracket = stack.pop()
                if (
                    (char == "}" and opening_bracket != "{")
                    or (char == "]" and opening_bracket != "[")
                    or (char == ")" and opening_bracket != "(")
                ):
                    return False
                depth -= 1  # it means we closed a bracket so reduce nesting depth
            elif not char.isspace() and not stack:
                return False
        if depth > MAX_ALLOWED_DEPTH:
            print(f"Error: nesting level above max allowed: {depth}")
            return False
    return not stack and not in_string and not is_payload_string


def check_valid_json(file):
    with open(file, "r") as file:
        content = file.read()

    return is_valid_json(content)


def check_content_outbounds(file):
    with open(file, "r") as file:
        content = file.read()
    if content[-1] == '"':
        print(f"the JSON file {content} ends with a quotation mark")
        return False
    else:
        return True


def find_unquoted_keys(file):
    pattern = r"\b\w+\s*:"  # This pattern matches unquoted keys

    with open(file, "r") as myFile:
        content = myFile.read()
        unquoted_keys = re.findall(pattern, content)

        if unquoted_keys:
            print("The following keys must be quoted:")
            for key in unquoted_keys:
                print(key)
                return False

        if ' , "' in content:
            print("Found missing value")
            return False
        else:
            return True


def check_for_apostrophe(file):
    with open(file, "r") as content:
        for i, line in enumerate(content, start=1):
            if "'" in line:
                print(f"unexpected char found in line {i}: {line.strip()}")
            else:
                return True


def check_for_wrong_boolean_format(file, value):
    with open(file, "r") as content:
        for i, line in enumerate(content, start=1):
            if value == "True" in line or value == "False" in line:
                print(f"unexpected boolean format found in line {i}: {line.strip()}")
                sys.exit(1)


def check_for_trailing_commas(file):
    with open(file, "r") as myFile:
        content = myFile.read()
        if content[-2] == ",":
            print("No trailing commas allowed")
        else:
            return True


def check_for_illegal_chars(filename):
    with open(filename, "r") as file:
        content = file.read()
        single_quote_count = content.count("'")
        escaped_single_quote_count = content.count("\\'")
        # Check for single quotes surrounding values, considering escaped single quotes
        if single_quote_count > escaped_single_quote_count:
            return False
        return True


def contains_hexadecimal(file):
    with open(file, "r") as myFile:
        content = myFile.read()
        try:
            # Attempt to parse the string
            parsed = ast.literal_eval(content)

            if isinstance(parsed, dict):
                for value in parsed.values():
                    if isinstance(value, int) and hex(value) != hex(value).lower():
                        print("file contains hexadecimal")
                        return False  # file contains a hexadecimal
        except Exception as e:
            pass
    return True


# check for '\t' chars
def contains_tab_in_string(string):
    in_string = False
    escaped = False

    for char in string:
        if char == "\\" and not escaped:
            escaped = True
        elif char == '"' and not escaped:
            in_string = not in_string
        elif char == "t" and not escaped and in_string:
            return True
        elif char == "\t" and in_string:
            return True
        else:
            escaped = False

    return False


def contains_line_break_in_string(string):
    in_string = False
    escaped = False

    for char in string:
        if char == "\\" and not escaped:
            escaped = True
        elif char == '"' and not escaped:
            in_string = not in_string
        elif char == "n" and not escaped and in_string:
            return True
        else:
            escaped = False

    return False


def check_incomplete_number_format(value):
    value = value.strip("[").strip("]").strip("{").strip("}")
    if re.match(r"^[{\[]?\d+(\.\d+)?[eE][-+]?[}\]]?$", value):
        print(f"Error mid parsing: the value: {value} is an incomplete number format")
        sys.exit(1)


def parse_value(value, my_dict, key):
    check_incomplete_number_format(value)
    # nested lists
    if isinstance(value, list):
        value = [parse_value(elem, {}, None) for elem in value]
    # nested objects
    if value.startswith("{") and value.endswith("}"):
        value = ast.literal_eval(value)
        my_dict[key] = value
    else:
        # if it is not an object clean for trailing }
        value = value.strip('}"')
        # check to see if its an list
        if value.startswith("[") and value.endswith("]"):
            value = ast.literal_eval(value)
        elif value.isdigit():
            # check for digits with leading zeroes
            if value.startswith("0") and len(value) > 1:
                print(
                    f"Error mid parsing: the value for key '{key}' cannot have leading zeroes"
                )
                sys.exit(1)
            else:
                value = int(value)
        elif value == "null":
            value = None
        elif value == "true":
            value = True
        elif value == "false":
            value = False

        # check for math without quotes
        elif (
            value[0] != '"'
            and value[-1] != '"'
            and any(op in value for op in ["+", "-", "*", "/", "%", "**"])
        ):
            print(
                f"Error mid parsing: the value for key '{key}' contains a mathematical operation without quotes"
            )
            sys.exit(1)

        # check for illegal evocations
        elif "()" in value:
            print(
                f"Error mid parsing: the value for key '{key}' contains an illegal invocation"
            )
            sys.exit(1)

        # check for hex numbers

        elif value.startswith("0x"):
            print(
                f"Error mid parsing: the value for key '{key}' is a hexadecimal number"
            )
            sys.exit(1)
        my_dict[key] = value
    return my_dict


def split_json_string(json_str):
    result = []
    nesting_level = 0
    current_token = ""

    for char in json_str:
        if char == "{" or char == "[":
            nesting_level += 1
        elif char == "}" or char == "]":
            nesting_level -= 1

        current_token += char

        if nesting_level == 1 and char == ",":
            result.append(current_token.strip())
            current_token = ""

    result.append(current_token.strip())
    return result


def check_for_linebreaks_in_string(file):
    with open(file, "r") as myFile:
        content = myFile.read()

        inside_string = False
        escape = False

        for i, char in enumerate(content):
            if char == '"':
                inside_string = not inside_string
            elif char == "\\" and inside_string:
                escape = not escape
            elif char == "\n" and inside_string and not escape:
                print(
                    f"Error mid parsing: Line break found inside string at position {i}"
                )
                sys.exit(1)

        if inside_string:
            print("Error mid parsing: Unclosed string")
            sys.exit(1)


def check_for_tabs_in_string(file):
    with open(file, "r") as myFile:
        content = myFile.read()

        inside_string = False
        escape = False

        for i, char in enumerate(content):
            if char == '"':
                inside_string = not inside_string
            elif char == "\t" and inside_string:
                print(
                    f"Error mid parsing: Tab character found inside string at position {i}"
                )
                sys.exit(1)
            elif char == "\\" and inside_string:
                print(
                    f"Error mid parsing: Escaped tab character found inside string at position {i}"
                )
                sys.exit(1)
        if inside_string:
            print("Error mid parsing: Unclosed string")
            sys.exit(1)


def parser(file):
    with open(file, "r") as myFile:
        content = myFile.read()

        check_for_tabs_in_string(file)
        check_for_linebreaks_in_string(file)

        cleaned_content = re.sub(r"\n\s*", "", content)
        print(cleaned_content, "CLEAN")

        pairs = split_json_string(cleaned_content)

        my_dict = {}

        for pair in pairs:
            if pair[0] == "[" and pair[-1] == "]" and ":" in pair:
                print(f"Error mid parsing: list contains colons instead of commas")
                sys.exit(1)

            if ":" not in pair and "," in pair:
                print(
                    f"Invalid JSON: Found a comma instead of a colon in pair '{pair}'"
                )
                sys.exit(1)

            if ":" in pair:
                key, value = map(str.strip, pair.rstrip(",").split(":", 1))
                key = key.strip('{"')

                # if key-pair had a double colon, one will be carried over
                if ":" in key or ":" in value[0]:
                    print(f"Error mid parsing: double colon")
                    sys.exit(1)
                check_for_wrong_boolean_format(file, value)

                parse_value(value, my_dict, key)
            elif ":" not in pair and pair[0] == "{" and pair[-1] == "}":
                print(f"Error mid parsing: missing colon")
                sys.exit(1)
            else:
                parse_value(pair, my_dict, None)
        return my_dict


def validate_json(filename):
    try:
        is_valid = check_valid_json(filename)
        has_no_apostrophes = check_for_apostrophe(filename)
        has_no_unquoted_keys = find_unquoted_keys(filename)
        has_no_trailing_commas = check_for_trailing_commas(filename)
        has_no_illegal_chars = check_for_illegal_chars(filename)
        has_no_hexadecimal = contains_hexadecimal(filename)
        has_no_extra_content = check_content_outbounds(filename)
        # has_no_tabs_strings = check_for_tabs(filename)
        # print(has_no_tabs_strings, "TABS")

        return (
            is_valid
            and has_no_apostrophes
            and has_no_unquoted_keys
            and has_no_trailing_commas
            and has_no_illegal_chars
            and has_no_hexadecimal
            and has_no_extra_content
            # and has_no_tabs_strings
        )
    except Exception as e:
        print(f"Error during JSON validation: {e}")
        return False


@app.command()
def main(filename: Annotated[str, typer.Argument()]):
    if filename and validate_json(filename):
        print("Initials checks: PASS")
        return parser(filename)
    else:
        print("Invalid JSON")
        sys.exit(1)


if __name__ == "__main__":
    app()
