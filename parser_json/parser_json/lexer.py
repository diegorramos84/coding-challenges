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

    if string[0] == JSON_QUOTE:
        string = string[1:]  # remove the quote
    else:
        return None, string

    i = 0
    while i < len(string):
        char = string[i]
        if escape:
            if char in 'ntrbf"\\/u':
                # Handle standard escape characters and Unicode
                json_string += {
                    "n": "\n",
                    "t": "\t",
                    "r": "\r",
                    "b": "\b",
                    "f": "\f",
                    '"': '"',
                    "\\": "\\",
                    "/": "/",
                }.get(char, "")
                if char == "u":  # Special handling for Unicode
                    if i + 4 >= len(string):
                        raise Exception(
                            "Invalid Unicode escape sequence: insufficient characters"
                        )
                    unicode_hex = string[i + 1 : i + 5]
                    try:
                        unicode_char = chr(int(unicode_hex, 16))
                        json_string += unicode_char
                        i += 4
                    except ValueError:
                        raise Exception(
                            f"Invalid Unicode escape sequence: \\u{unicode_hex}"
                        )
            else:
                raise Exception(f"Invalid escape sequence: \\{char}")
            escape = False
        elif char == "\\":
            escape = True
        elif char == JSON_QUOTE:
            return json_string, string[i + 1 :]
        elif char in ["\n", "\t"]:
            # Raise exception for unescaped newline and tab characters
            raise Exception(f"Unescaped control character in string: {char}")
        else:
            json_string += char
        i += 1

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
        return float(json_number), rest

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

        # and check if its white space, part of the syntax or invalid char
        if char in JSON_WHITESPACE:
            string = string[1:]

        elif char in JSON_SYNTAX:
            tokens.append(char)
            string = string[1:]
        # Skip the comma and the first quote of the next token
        else:
            raise Exception("Unexpected char or missing quotes around string")
    return tokens
