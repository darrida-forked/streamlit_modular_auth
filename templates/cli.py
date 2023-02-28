import shutil
from pathlib import Path

import click
from rich import print


@click.group()
def cli():
    pass


@cli.command("app-template")
def app_template():
    source_dir = Path(__file__).resolve().parent / "template_app"
    target_dir = Path(".") / "starter_app"
    try:
        shutil.copytree(source_dir, target_dir)
    except FileExistsError:
        print("[bold yellow]Warning:[/bold yellow] A directory named 'apps' already exists.")


@cli.command("custom-app-template")
def custom_app_template():
    source_dir = Path(__file__).resolve().parent / "template_app_custom"
    target_dir = Path(".") / "custom_starter_app"
    try:
        shutil.copytree(source_dir, target_dir)
    except FileExistsError:
        print("[bold yellow]Warning:[/bold yellow] A directory named 'apps' already exists.")


def main():
    cli()


if __name__ == "__main__":
    main()
