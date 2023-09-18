import sys

sys.path.insert(0, "./")

# import argparse
import logging
import click
import platform

from weblog import __version__, project_name
from weblog.commands import initutil, moreutil

DESC = """
weblog:
    A python static blog generator.
"""


def get_version():
    return "%(prog)s, version %(version)s; {}={}; Python={}".format(
        project_name, __version__, platform.python_version()
    )


@click.group()
@click.version_option(__version__, message=get_version())
def cli():
    fmt = "%(asctime)s-%(name)s %(filename)s[%(lineno)d] - %(levelname)s: %(message)s"
    logging.basicConfig(level=logging.INFO, format=fmt)
    DESC


@cli.command()
@click.option("--path", type=str, default="blog-site")
@click.option("--query", is_flag=True)
# @click.option('--conf', type=str, default="")
# @click.option('--theme', type=str, default="")
def init(path, query):
    initutil.init(path, query)


@cli.command()
def build():
    moreutil.build()


@cli.command()
@click.option("--port", type=int, default=8000)
def serve(port):
    pass  # todo


@cli.command()
# @click.option('--out', type=str, default="out")
def clean():
    moreutil.clean()


if __name__ == "__main__":
    cli()
