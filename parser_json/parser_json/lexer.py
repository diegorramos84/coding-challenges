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
    # start the loop if a quote is found
    if string[0] == JSON_QUOTE:
        string = string[1:]  # remove the quote
    else:
        return None, string

    for char in string:
        if char == JSON_QUOTE:  # end string if a final quote is found
            return (
                json_string,
                string[len(json_string) + 1 :],
            )  # return the json_string and the rest of the string for further analysis. We also remove the closing quote
        else:
            json_string += char
    raise Exception("Expected end-of-string quote")


def lex_number(string):
    json_number = ""

    number_chars = [str(d) for d in range(0, 10)] + ["-", "e", "."]

    for char in string:
        if char in number_chars:
            json_number += char
        else:
            break

    rest = string[len(json_number) :]

    if not len(json_number):
        return None, string

    if "." in json_number:
        return float(json_number), rest

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
        check_trailing_comma(string)

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
