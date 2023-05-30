import argparse
import logging
from blogbuilder.process import BlogBuilder


def get_parser():
    _parser = argparse.ArgumentParser()
    return _parser


def run():
    fmt = "%(asctime)s-%(name)s %(filename)s[%(lineno)d] - %(levelname)s: %(message)s"
    logging.basicConfig(level=logging.WARNING, format=fmt)
    builder = BlogBuilder()
    builder.build_all()


if __name__ == "__main__":
    run()
