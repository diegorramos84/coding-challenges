import json
import os

import pytest

from json_parser.main import parser

# get the current path were the test is being called from
current_dir = os.path.dirname(__file__)

# construct the path to the .json files
valid_json_path = os.path.join(current_dir, "step3", "valid.json")

invalid_json_path = os.path.join(current_dir, "step3", "invalid.json")


def test_object_returns_dict():
    result = parser(valid_json_path)

    f = open(valid_json_path)

    data = json.load(f)

    print(result)
    assert result == data


def test_reject_files_not_correct_format():
    with pytest.raises(SystemExit) as result:
        parser(invalid_json_path)
    assert result.type == SystemExit
    assert result.value.code == 1
