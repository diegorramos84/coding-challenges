from .constants import *


def parse_list(tokens):
    json_list = []
    t = tokens[0]

    # iterate until we find a right bracket, return when we find one, plug the rest
    if t == JSON_RIGHTBRACKET:
        return json_list, tokens[1:]

    while True:
        json, tokens = my_parse(tokens)
        json_list.append(json)

        t = tokens[0]
        if t == JSON_RIGHTBRACKET:
            return json_list, tokens[1:]
        elif t != JSON_COMMA:
            raise Exception("Expected comma after object in list")
        else:
            tokens = tokens[1:]


def parse_object(tokens):
    json_object = {}

    t = tokens[0]
    if t == JSON_RIGHTBRACE:
        return json_object, tokens[1:]

    while True:
        json_key = tokens[0]
        if type(json_key) is str:
            tokens = tokens[1:]
        else:
            raise Exception("Expected string key, got {}".format(json_key))

        if tokens[0] != JSON_COLON:
            raise Exception("Expected colon after key in object got: {}".format(t))

        json_value, tokens = my_parse(tokens[1:])

        json_object[json_key] = json_value

        t = tokens[0]
        if t == JSON_RIGHTBRACE:
            return json_object, tokens[1:]
        elif t != JSON_COMMA:
            raise Exception("Expected commas after pair in object, got {}".format(t))

        tokens = tokens[1:]


def my_parse(tokens):
    t = tokens[0]

    # check if list or object
    if t == JSON_LEFTBRACKET:
        return parse_list(tokens[1:])
    elif t == JSON_LEFTBRACE:
        return parse_object(tokens[1:])
    else:
        return t, tokens[1:]
