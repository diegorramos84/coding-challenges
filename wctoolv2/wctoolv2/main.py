import sys
from typing import Optional

import typer
from typing_extensions import Annotated


def bytes_in_file(content):
    # convert string to bytes and count the number of bytes in the file
    return len(content.encode('utf-8'))

def lines_in_file(content):
    # creates a list of all lines in a file
    lines = content.split('\n')
    return len(lines)

def words_in_file(content):
    words = content.split()
    return len(words)

def chars_in_file(content):
    return len(content)

def main(
    filename: Annotated[Optional[str], typer.Argument(show_default=False)] = None,
    c: Annotated[bool, typer.Option("-c", help="count text file bytes", show_default=False)] = False,
    l: Annotated[bool, typer.Option("-l",help="count text file lines", show_default=False)] = False,
    w: Annotated[bool, typer.Option("-w",help="count text file words", show_default=False)] = False,
    m: Annotated[bool, typer.Option("-m",help="count text file chars", show_default=False)] = False,
    ):

    if filename:
        with open(filename, 'r') as myfile:
            content = myfile.read()
            file = filename
    else:
        content = sys.stdin.read()
        file = None

    if content:
        if c:
            bytes = bytes_in_file(content)
            if file is not None:
                print(bytes, file)
            else:
                print(bytes)
        elif l:
            lines = lines_in_file(content)
            if file is not None:
                print(lines, file)
            else:
                print(lines)
        elif w:
            word = words_in_file(content)
            if file is not None:
                print(word, file)
            else:
                print(word)
        elif m:
            chars = chars_in_file(content)
            if file is not None:
                print(chars, file)
            else:
                print(chars)
        else:
            bytes = bytes_in_file(content)
            lines = lines_in_file(content)
            word = words_in_file(content)
            if file is not None:
                print(lines, word, bytes, file)
            else:
                print(lines, word, bytes)


if __name__ == "__main__":
    typer.run(main)
