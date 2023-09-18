__version__ = "0.0.2"
__name__ = "weblog"

import argparse
import logging
from .process import BlogBuilder


def get_parser():
    _parser = argparse.ArgumentParser()
    return _parser


def run():
    fmt = "%(asctime)s-%(name)s %(filename)s[%(lineno)d] - %(levelname)s: %(message)s"
    logging.basicConfig(level=logging.INFO, format=fmt)
    builder = BlogBuilder()
    builder.build_all()


def main():
    run()
