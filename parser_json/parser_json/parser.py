from .constants import *

MAX_DEPTH = 19


def parse_list(tokens, depth):
    if depth > MAX_DEPTH:
        raise Exception("Nesting too deep")
    json_list = []
    t = tokens[0]

    # iterate until we find a right bracket, return when we find one, plug the rest
    if t == JSON_RIGHTBRACKET:
        return json_list, tokens[1:]

    while True:
        json, tokens = my_parse(tokens, depth)
        json_list.append(json)

        t = tokens[0]
        if t == JSON_COMMA:
            if len(tokens) < 2 or tokens[1] in [JSON_COMMA, JSON_RIGHTBRACKET]:
                raise Exception("Error: Trailing comma in object")
            tokens = tokens[1:]
        elif t == JSON_RIGHTBRACKET:
            return json_list, tokens[1:]
        else:
            raise Exception(
                "Expected comma or closing bracket in list, got {}".format(t)
            )


def parse_object(tokens, depth):
    if depth > MAX_DEPTH:
        raise Exception("Nesting too deep")
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

        json_value, tokens = my_parse(tokens[1:], depth)

        json_object[json_key] = json_value

        t = tokens[0]

        if t == JSON_COMMA:
            if len(tokens) < 2 or tokens[1] in [JSON_COMMA, JSON_RIGHTBRACE]:
                raise Exception("Error: Trailing comma in object")
            tokens = tokens[1:]
        elif t == JSON_RIGHTBRACE:
            return json_object, tokens[1:]
        else:
            raise Exception(
                "Expected comma or closing brace in object, got {}".format(t)
            )


def my_parse(tokens, depth=0):
    t = tokens[0]

    # check if list or object
    if t == JSON_LEFTBRACKET:
        return parse_list(tokens[1:], depth + 1)
    elif t == JSON_LEFTBRACE:
        return parse_object(tokens[1:], depth + 1)
    else:
        return t, tokens[1:]
