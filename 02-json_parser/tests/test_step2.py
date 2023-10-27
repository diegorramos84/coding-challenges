import os

import pytest

from json_parser.main import parser

# get the current path were the test is being called from
current_dir = os.path.dirname(__file__)

# construct the path to the .json files
valid_json_path = os.path.join(current_dir, "step2", "valid.json")
valid2_json_path = os.path.join(current_dir, "step2", "valid2.json")
invalid_json_path = os.path.join(current_dir, "step2", "invalid.json")
invalid2_json_path = os.path.join(current_dir, "step2", "invalid2.json")


def test_one_object_returns_dict():
    result = parser(valid_json_path)
    assert result["key"] == "value"


def test_more_object_returns_dict():
    result = parser(valid2_json_path)
    assert result["key"] == "value"


def test_reject_files_trailing_comma():
    with pytest.raises(SystemExit) as result:
        parser(invalid_json_path)
    assert result.type == SystemExit
    assert result.value.code == 1