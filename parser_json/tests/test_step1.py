import os
import sys

import pytest

from parser_json.validations import json_not_empty, starts_with_bracket_or_braces

# get the current path were the test is being called from
current_dir = os.path.dirname(__file__)

# construct the path to the .json files
valid_json_path = os.path.join(current_dir, "step1", "valid.json")
invalid_json_path = os.path.join(current_dir, "step1", "invalid.json")


def test_json_is_list_or_object():
    with open(valid_json_path, "r") as myFile:
        content = myFile.read()
        content = content.strip()
        result = starts_with_bracket_or_braces(content)
        assert result == True


def test_json_is_not_empty():
    result = json_not_empty(invalid_json_path)
    print(result, "RESULT")
    assert result == True
