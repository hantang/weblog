from pathlib import Path
import shutil
import logging

from weblog.process import SiteSkeleton
from weblog.process import BlogBuilder


def build():
    logging.info("build blog")
    builder = BlogBuilder()
    builder.build_all()


def clean(path="."):
    deploy_path = Path(path, SiteSkeleton.deploy)
    if deploy_path.exists():
        logging.info(f"remove deploy path={deploy_path}")
        shutil.rmtree(deploy_path)
    