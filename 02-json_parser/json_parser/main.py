import ast
import sys

import typer
from typing_extensions import Annotated

app = typer.Typer()


def check_valid_json(file):
    with open(file, "r") as myFile:
        content = myFile.read()
        # check if the content starts and ends with curly brackets
        if len(content) > 0 and content[0] == "{" and content[-1] == "}":
            return True
        else:
            return False


def check_for_apostrophe(file):
    with open(file, "r") as content:
        for i, line in enumerate(content, start=1):
            if "'" in line:
                print(f"unexpected char found in line {i}: {line.strip()}")
                sys.exit(1)


def check_for_wrong_boolean_format(file, value):
    with open(file, "r") as content:
        for i, line in enumerate(content, start=1):
            if value == "True" in line or value == "False" in line:
                print(f"unexpected boolean format found in line {i}: {line.strip()}")
                sys.exit(1)


def check_for_trailing_commas(content):
    if content[-2] == ",":
        print("No trailing commas")
        sys.exit(1)


def parse_value(value, my_dict, key):
    if value.startswith("{") and value.endswith("}"):
        value = ast.literal_eval(value)
        my_dict[key] = value
    else:
        value = value.strip('\n}"')
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


# custom script to deal with commas inside object or array
def custom_split(input_str):
    result = []
    current_item = ""
    bracket_count = 0
    # TODO need to figure this bit out for nested objects
    in_quotes = False

    # iterate character by character
    for char in input_str:
        # if the char is a comma and the count of brackets is 0
        if char == "," and bracket_count == 0 and not in_quotes:
            # add the char to the current_item(value)
            result.append(current_item.strip())
            # reset the current value
            current_item = ""
        else:
            # move to the next chat
            current_item += char

            # brackets counter
            if char == "[" and not in_quotes:
                bracket_count += 1
            elif char == "]" and not in_quotes:
                bracket_count -= 1
            elif char == '"':
                in_quotes = not in_quotes
    result.append(current_item.strip())
    return result


def parser(file):
    with open(file, "r") as myFile:
        content = myFile.read()

        check_for_trailing_commas(content)

        # pairs = content.split(",")
        pairs = custom_split(content)

        my_dict = {}

        for pair in pairs:
            # content.split(':') divides the content in the :, producing a list
            # str.strip remove whitespaces from the list created
            print(pair, "pair")
            key, value = map(str.strip, pair.split(":", 1))
            # checking if values are in the correct json format

            check_for_wrong_boolean_format(file, value)
            check_for_apostrophe(file)

            # removing \n, ", and {} from key and values
            key = key.strip(' \n{"')

            parse_value(value, my_dict, key)

        print(my_dict)
        return my_dict


@app.command()
def main(filename: Annotated[str, typer.Argument()]):
    if filename:
        is_valid = check_valid_json(filename)
        check_for_apostrophe(filename)
        if is_valid:
            print("Valid JSON")
            parser(filename)
            sys.exit(0)
        else:
            print("Invalid JSON")
            sys.exit(1)


if __name__ == "__main__":
    app()
