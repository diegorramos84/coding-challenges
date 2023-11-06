from decimal import Decimal

from .constants import *
from .validations import *

JSON_QUOTE = '"'
JSON_WHITESPACE = [" ", "\t", "\b", "\n", "\r"]
JSON_SYNTAX = [
    JSON_COMMA,
    JSON_COLON,
    JSON_LEFTBRACKET,
    JSON_RIGHTBRACKET,
    JSON_LEFTBRACE,
    JSON_RIGHTBRACE,
]


FALSE_LEN = len("false")
TRUE_LEN = len("true")
NULL_LEN = len("null")


def lex_string(string):
    json_string = ""
    escape = False  # Flag to track if an escape sequence is being processed
    # start the loop if a quote is found
    if string[0] == JSON_QUOTE:
        string = string[1:]  # remove the quote
    else:
        return None, string
    for char in string:
        if escape:
            if char.isspace():
                raise Exception("Invalid space within escape sequence")
            # If an escape sequence is being processed, treat it as a literal
            json_string += "\\" + char
            escape = False  # Reset the escape flag after processing
        elif char == JSON_QUOTE:
            return (
                json_string,
                string[len(json_string) + 1 :],
            )
        elif char == "\\":
            escape = True
        else:
            json_string += char
    raise Exception("Expected end-of-string quote")


def lex_number(string):
    json_number = ""

    number_chars = [str(d) for d in range(0, 10)] + ["-", "+", "e", "E", "."]

    for char in string:
        if char in number_chars:
            json_number += char
        else:
            break

    rest = string[len(json_number) :]

    if not len(json_number):
        return None, string

    if "." in json_number or "e" in json_number or "E" in json_number:
        return Decimal(json_number), rest

    if len(json_number) > 1 and json_number[0] not in ["-", "+", "e", "E", "."]:
        if int(json_number[0]) == 0:
            raise Exception("Error: Numbers cannot have leading zeroes")

    return int(json_number), rest


def lex_bool(string):
    string_len = len(string)

    # comparing with true and false length to avoid "index out of range errors"
    if string_len >= TRUE_LEN and string[:TRUE_LEN] == "true":
        return True, string[TRUE_LEN:]
    elif string_len >= FALSE_LEN and string[:FALSE_LEN] == "false":
        return False, string[FALSE_LEN:]

    return None, string


def lex_null(string):
    string_len = len(string)

    # comparing with true and false length to avoid "index out of range errors"
    if string_len >= NULL_LEN and string[:NULL_LEN] == "null":
        return True, string[NULL_LEN:]
    return None, string


def lex(string):
    tokens = []

    while len(string):
        # send string to function, if its a match, process it and returns it back
        # if not just return it back
        json_string, string = lex_string(string)
        if json_string is not None:
            print(type(json_string), "JSON STRING")
            check = detect_spaces(json_string)
            if check:
                tokens.append(json_string)
                continue

        json_string, string = lex_number(string)
        if json_string is not None:
            tokens.append(json_string)
            continue

        json_string, string = lex_bool(string)
        if json_string is not None:
            tokens.append(json_string)
            continue

        json_string, string = lex_null(string)
        if json_string is not None:
            tokens.append(None)
            continue

        # if none of the functions processed it we get it here

        char = string[0]
        check_trailing_comma(string)

        # and check if its white space, part of the syntax or invalid char
        if char in JSON_WHITESPACE:
            string = string[1:]

        # if char in JSON_ILLEGAL_ESCAPES:
        #     raise Exception(f"Illegal backslash scape: {char}")
        elif char in JSON_SYNTAX:
            tokens.append(char)
            string = string[1:]
        # Skip the comma and the first quote of the next token
        else:
            raise Exception("Unexpected char or missing quotes around string")
    return tokens
