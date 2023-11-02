import json
import os

import pytest

from parser_json.main import main

# get the current path were the test is being called from
current_dir = os.path.dirname(__file__)

# construct the path to the .json files
valid_json_path = os.path.join(current_dir, "step4", "valid.json")
valid2_json_path = os.path.join(current_dir, "step4", "valid2.json")
valid3_json_path = os.path.join(current_dir, "step4", "valid3.json")
valid4_json_path = os.path.join(current_dir, "step4", "valid4.json")

invalid_json_path = os.path.join(current_dir, "step4", "invalid.json")


def test_valid_json_with_nested_empty_object_and_list():
    result = main(valid_json_path)

    f = open(valid_json_path)

    data = json.load(f)

    assert result == data


def test_valid_json_with_nested_object_and_list():
    result = main(valid2_json_path)

    f = open(valid2_json_path)

    data = json.load(f)

    assert result == data


# # comma inside list
def test_valid_json_with_nested_object_and_list_with_nested_object():
    result = main(valid3_json_path)

    f = open(valid3_json_path)

    data = json.load(f)

    assert result == data


# # comma inside dict
def test_non_empty_object_returns_dict_nested():
    result = main(valid4_json_path)

    f = open(valid4_json_path)

    data = json.load(f)

    assert result == data


def test_single_quote_inside_list():
    with pytest.raises(Exception) as result:
        main(invalid_json_path)
        print(result.value)
    assert str(result.value) == "Unexpected char or missing quotes around string"
