import json
import os

import pytest

from parser_json.main import main

# get the current path were the test is being called from
current_dir = os.path.dirname(__file__)

# construct the path to the .json files
folder_path = os.path.join(current_dir, "extra")

pass1_path = os.path.join(current_dir, "extra", "pass1.json")


def get_fail_json_files(dir):
    fail_json_files = []
    for filename in os.listdir(dir):
        if filename.startswith("fail") and filename.endswith(".json"):
            fail_json_files.append(os.path.join(dir, filename))
    return fail_json_files


@pytest.mark.parametrize("invalid_json_path", get_fail_json_files(folder_path))
def test_non_empty_object_returns_dict_wrong_format(invalid_json_path):
    with pytest.raises(Exception):
        main(invalid_json_path)


# def test_empty_object_returns_dict():
#     result = main(pass1_path)

#     f = open(pass1_path)

#     data = json.load(f)

#     assert result == data
