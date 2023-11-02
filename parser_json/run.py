import typer
from typing_extensions import Annotated

from parser_json.main import main

app = typer.Typer()


@app.command()
def process_json(filename: Annotated[str, typer.Argument()]):
    if filename:
        result = main(filename)
        print(result)


if __name__ == "__main__":
    app()
