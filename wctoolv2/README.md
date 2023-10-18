# wc unix tool

My dev notes:

This is the same application as 01.wc-tool but using poetry and typer

Install poetry
https://python-poetry.org/docs/

create new project with poetry

```bash
poetry new wctoolv2
cd wctoolv2
```

add typer to dependencies

```bash
poetry add "typer[all]"
```

start shell
```
poetry shell
```

project structure should look something like this

```
.
├── poetry.lock
├── pyproject.toml
├── README.rst
├── wc-toolv2
│   └── __init__.py
└── tests
    ├── __init__.py
```

create main.py

```
touch main.py
```

add basic code to the main file

```python
import typer

def main(
	print('Hello world')
)

if __name__ == "__main__":
	typer.run(main)

```

The app usage will be the following:

```python
Usage: main.py [OPTIONS] [FILENAME]
```

So we will have one OPTIONAL argument and several OPTIONAL options

As per typer documentation(https://typer.tiangolo.com/tutorial/arguments/), we will manage the filename argument as follow:

```python
from typing import Optional
import typer

from typing_extensions import Annotated

def main(
	filename: Annotated[Optional[str], typer.Argument(show_default=False)] = None,
)

```

- Wrap the function parameter with Annotated
- Add additional metadata to tell typer that it is an argument: typer.Argument()
- Add a default value of None
- In this case I also added show_default=False to not show default values in the --help option

Now we move to the second part of the usage: Optional options

The app has the following options:
- `-c`: print the byte counts
- `-m`: print the character counts
- `-l`: print the newline counts
- `-w`: print the word counts

So again following the documentation we will add the code to the main function:

```python
c: Annotated[bool, typer.Option("-c", help="count text file bytes", show_default=False)] = False,

l: Annotated[bool, typer.Option("-l",help="count text file lines", show_default=False)] = False,

w: Annotated[bool, typer.Option("-w",help="count text file words", show_default=False)] = False,

m: Annotated[bool, typer.Option("-m",help="count text file chars", show_default=False)] = False,
```

- In this case I defined the options as boolean and default it to False
- Add typer.Option to tell typer that we are talking about options
- By default the options would be followed by "--" so I added an option short name to be able to use the app with only "-"


With the app this way in order to run it you need to run it like a python file

```bash
python3 main.py text.txt
```

So I decided to create a package

added the following to pyproject.toml

```toml
[tool.poetry.scripts]
wctoolv2 = "wctoolv2.main:app"
```

and in the main.py file changed the code to

```python
app = typer.Typer()
# Added @app.command() to the main function
@app.command()
def main(...rest of the code

```

And that way, inside the shell, wctoolv2 is avaliable and I can use the app like this
```bash
wctoolv2 /path/to/file/text.txt
7144 58164 334997 /path/to/file/text.txt
```

or
```
cat /path/to/file/text.txt wctoolv2
