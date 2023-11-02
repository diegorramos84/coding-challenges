import json
import os

import pytest

from parser_json.main import main

# get the current path were the test is being called from
current_dir = os.path.dirname(__file__)

# construct the path to the .json files
valid_json_path = os.path.join(current_dir, "step3", "valid.json")

invalid_json_path = os.path.join(current_dir, "step3", "invalid.json")


def test_object_returns_dict():
    result = main(valid_json_path)

    f = open(valid_json_path)

    data = json.load(f)

    print(result)
    assert result == data


def test_reject_missing_quotes():
    with pytest.raises(Exception) as result:
        main(invalid_json_path)
        print(result.value)
    assert str(result.value) == "Unexpected char or missing quotes around string"
