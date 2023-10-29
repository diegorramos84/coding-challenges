import json
import os

import pytest

from json_parser.main import main

# get the current path were the test is being called from
current_dir = os.path.dirname(__file__)

# construct the path to the .json files
valid_json_path = os.path.join(current_dir, "step4", "valid.json")
valid2_json_path = os.path.join(current_dir, "step4", "valid2.json")
valid3_json_path = os.path.join(current_dir, "step4", "valid3.json")
valid4_json_path = os.path.join(current_dir, "step4", "valid4.json")

invalid_json_path = os.path.join(current_dir, "step4", "invalid.json")


def test_empty_object_returns_dict():
    result = main(valid_json_path)

    f = open(valid_json_path)

    data = json.load(f)

    assert result == data


def test_non_empty_object_returns_dict():
    result = main(valid2_json_path)

    f = open(valid2_json_path)

    data = json.load(f)

    assert result == data


# comma inside list
def test_non_empty_object_returns_list_nested():
    result = main(valid3_json_path)

    f = open(valid3_json_path)

    data = json.load(f)

    assert result == data


# comma inside dict
def test_non_empty_object_returns_dict_nested():
    result = main(valid4_json_path)

    f = open(valid4_json_path)

    data = json.load(f)

    assert result == data


def test_non_empty_object_returns_dict_wrong_format():
    with pytest.raises(SystemExit) as result:
        main(invalid_json_path)
    assert result.type == SystemExit
    assert result.value.code == 1
