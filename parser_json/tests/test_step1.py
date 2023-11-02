import os
import sys

import pytest

from parser_json.validations import is_valid_json_file

# get the current path were the test is being called from
current_dir = os.path.dirname(__file__)

# construct the path to the .json files
valid_json_path = os.path.join(current_dir, "step1", "valid.json")
invalid_json_path = os.path.join(current_dir, "step1", "invalid.json")


def test_json_is_list_or_object():
    with pytest.raises(SystemExit) as result:
        is_valid_json_file(valid_json_path)
        assert result.type == SystemExit
        assert result.value.code == 0


def test_json_is_not_empty():
    with pytest.raises(SystemExit) as result:
        is_valid_json_file(invalid_json_path)
        assert result.type == SystemExit
        assert result.value.code == 0
