import ast
import re
import sys

import typer
from typing_extensions import Annotated

app = typer.Typer()


# def is_valid_json(content):
#     if not content or content.isspace():
#         return False

#     stack = []

#     for char in content:
#         if char in "{[":
#             stack.append(char)
#         elif char in "]}":
#             if not stack:
#                 return False
#             if char == "}" and stack[-1] != "{":
#                 return False
#             if char == "]" and stack[-1] != "[":
#                 return False
#             stack.pop()
#     return not stack


def is_valid_json(content):
    if not content or content.isspace():
        return False

    stack = []  # Stack to keep track of opening and closing brackets
    in_string = False  # Flag to indicate if we are inside a string
    escape = False  # Flag to indicate if the current character is escaped

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

    return not stack and not in_string


def check_valid_json(file):
    with open(file, "r") as file:
        content = file.read()

    return is_valid_json(content)


def find_unquoted_keys(file):
    pattern = r"\b\w+\s*:"  # This pattern matches unquoted keys

    with open(file, "r") as myFile:
        content = myFile.read()
        unquoted_keys = re.findall(pattern, content)

        if unquoted_keys:
            print("The following keys must be quoted:")
            for key in unquoted_keys:
                print(key)
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


# def contains_no_illegal_expression(file):
#     with open(file, "r") as myFile:
#         content = myFile.read()
#         try:
#             parsed = ast.literal_eval(content)
#             if parsed:
#                 return True
#         except Exception as e:
#             print(f"Illegal expression found: {e}")
#             return False


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


def parse_value(value, my_dict, key):
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
            value = int(value)
        elif value == "null":
            value = None
        elif value == "true":
            value = True
        elif value == "false":
            value = False
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


def parser(file):
    with open(file, "r") as myFile:
        content = myFile.read()

        cleaned_content = re.sub(r"\n\s*", "", content)

        pairs = split_json_string(cleaned_content)

        my_dict = {}

        for pair in pairs:
            key, value = map(str.strip, pair.rstrip(",").split(":", 1))
            key = key.strip('{"')

            check_for_wrong_boolean_format(file, value)

            parse_value(value, my_dict, key)
        return my_dict


def validate_json(filename):
    is_valid = check_valid_json(filename)
    has_no_apostrophes = check_for_apostrophe(filename)
    has_no_unquoted_keys = find_unquoted_keys(filename)
    has_no_trailing_commas = check_for_trailing_commas(filename)
    has_no_illegal_chars = check_for_illegal_chars(filename)
    has_no_hexadecimal = contains_hexadecimal(filename)
    print(is_valid, "TEST")

    return (
        is_valid
        and has_no_apostrophes
        and has_no_unquoted_keys
        and has_no_trailing_commas
        and has_no_illegal_chars
        and has_no_hexadecimal
    )


@app.command()
def main(filename: Annotated[str, typer.Argument()]):
    if filename and validate_json(filename):
        print("Valid JSON")
        return parser(filename)

    else:
        print("Invalid JSON")
        sys.exit(1)


if __name__ == "__main__":
    app()
