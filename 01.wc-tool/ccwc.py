#! /usr/bin/env python3

import sys


opts = [opt for opt in sys.argv[1:] if opt.startswith('-')]
args = [arg for arg in sys.argv[1:] if not arg.startswith('-')]


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

if args:
    with open(args[0], 'r') as myfile:
        content = myfile.read()
        filename = args[0]
else:
    content = sys.stdin.read()
    filename = None

if content:
    # 1 - bytes in a file
    if "-c" in opts:
        bytes = bytes_in_file(content)
        if filename is not None:
            print(bytes, filename)
        else:
            print(bytes)

    # 2 - lines in a file
    if "-l" in opts:
        lines = lines_in_file(content)
        if filename is not None:
            print(lines, filename)
        else:
            print(lines)

    # 3 - words in a file
    if "-w" in opts:
        word = words_in_file(content)
        if filename is not None:
            print(word, filename)
        else:
            print(word)

    # 4 - chars in a file
    if "-m" in opts:
        chars = chars_in_file(content)
        if filename is not None:
            print(chars, filename)
        else:
            print(chars)

    if not opts:
        bytes = bytes_in_file(content)
        lines = lines_in_file(content)
        word = words_in_file(content)
        if filename is not None:
            print(lines, word, bytes, filename)
        else:
            print(lines, word, bytes)
