import ast
import re
import sys

import typer
from typing_extensions import Annotated

app = typer.Typer()


def check_valid_json(file):
    with open(file, "r") as myFile:
        content = myFile.read()
        # check if the content starts and ends with curly brackets
        if (
            len(content) > 0
            and content[0] == "{"
            or content[0] == "["
            and content[-1] == "}"
            or content[-1] == "]"
        ):
            return True

        else:
            return False


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


def contains_illegal_expression(file):
    with open(file, "r") as myFile:
        content = myFile.read()
        try:
            parsed = ast.literal_eval(content)

            if isinstance(parsed, dict):
                return True
            else:
                return False
        except Exception as e:
            print("Illegal expression found")
            return False


def contains_hexadecimal(file):
    with open(file, "r") as myFile:
        content = myFile.read()
        try:
            # Attempt to parse the string
            parsed = ast.literal_eval(content)

            if isinstance(parsed, dict):
                for value in parsed.values():
                    if isinstance(value, int) and hex(value) != hex(value).lower():
                        return True
        except Exception as e:
            pass
    print("Hexadecimal number(s) found")
    return False


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
    print(result)
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


@app.command()
def main(filename: Annotated[str, typer.Argument()]):
    if filename:
        is_valid = check_valid_json(filename)
        # has_no_apostrophes = check_for_apostrophe(filename)
        # has_no_unquoted_keys = find_unquoted_keys(filename)
        # has_no_trailing_commas = check_for_trailing_commas(filename)
        # has_no_illegal_expression = contains_illegal_expression(filename)
        # has_no_hexadecimal = contains_hexadecimal(filename)
        # print(has_no_hexadecimal)

        if (
            is_valid
            # and has_no_apostrophes
            # and has_no_unquoted_keys
            # and has_no_trailing_commas
            # and has_no_illegal_expression
            # and has_no_hexadecimal
        ):
            print("Valid JSON")
            parser(filename)
            sys.exit(0)

        else:
            print("Invalid JSON")
            sys.exit(1)


if __name__ == "__main__":
    app()
