import os

import pytest

from json_parser.main import check_valid_json

# get the current path were the test is being called from
current_dir = os.path.dirname(__file__)

# construct the path to the .json files
valid_json_path = os.path.join(current_dir, "step1", "valid.json")
invalid_json_path = os.path.join(current_dir, "step1", "invalid.json")


def test_is_valid():
    result = check_valid_json(valid_json_path)
    assert result is True


def test_is_not_valid():
    result = check_valid_json(invalid_json_path)
    print(result, "RESULT")
    assert result is False
