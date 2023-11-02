import json
import os

import pytest

from parser_json.main import main

# get the current path were the test is being called from
current_dir = os.path.dirname(__file__)

# construct the path to the .json files
valid_json_path = os.path.join(current_dir, "step2", "valid.json")
valid2_json_path = os.path.join(current_dir, "step2", "valid2.json")
invalid_json_path = os.path.join(current_dir, "step2", "invalid.json")
invalid2_json_path = os.path.join(current_dir, "step2", "invalid2.json")


def test_one_object_returns_dict():
    result = main(valid_json_path)
    print(result, "RESULT")
    f = open(valid_json_path)

    data = json.load(f)
    assert result == data


def test_more_object_returns_dict():
    result = main(valid2_json_path)
    assert result["key"] == "value"


def test_reject_files_trailing_comma():
    with pytest.raises(Exception) as result:
        main(invalid_json_path)
        print(result.value)
    assert str(result.value) == "Error: JSON file cannot have trailing comma"


def test_reject_missing_quotes():
    with pytest.raises(Exception) as result:
        main(invalid2_json_path)
        print(result.value)
    assert str(result.value) == "Unexpected char or missing quotes around string"
