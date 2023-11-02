import sys

from .lexer import *
from .parser import *
from .validations import *


def main(filename):
    with open(filename, "r") as myFile:
        content = myFile.read()
        if is_valid_json_file(content):
            print("Validation passed, continuing with processing...")
            tokens = lex(content)
            print(tokens, "TOKEns")
            return my_parse(tokens)[0]
        else:
            sys.exit(1)
