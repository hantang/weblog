import logging
from pathlib import Path
from textwrap import dedent
import pendulum
import toml
import shutil

from process import SiteSkeleton

def _demo_post(now):
    post = f"""
    ---
    title: "My First Post"
    author:
    date: "{now}"
    draft: false
    summary: "Tis is a demo post."
    comment: ""
    ---

    ## Part1

    something here...

    ## Part2

    more words...
    
    """
    return dedent(post)


def _demo_about(now):
    text = f"""
    ---
    title: "about"
    date: "{now}"
    draft: false
    ---

    ## About
    """
    return dedent(text)


def _demo_index(now, title, description=""):
    text = f"""
    ---
    title: "{title}"
    date: "{now}"
    draft: false
    description: "{description}"
    ---
    """
    return dedent(text)


def nvl(val, default_val):
    return val if val else default_val


def _read_input():
    title = input(
        "Site title:\n",
    )
    initials = input("Site initials:\n")
    description = input("Site description:\n")
    # theme = input("Use Default theme:\n")
    author = input("Author name:\n")
    return title, initials, description, author


def init(path):
    """
    # project dir skeleton
    blog-site/
        - config.toml
        - content/
            - index.md
            - about.md
            - posts/
                - first-post.md
            - ...
        - themes/
        - deploy/
    """
    path = Path(path)
    if path.exists():
        if path.is_file():
            logging.error(f"Error, path={path} is a file and exits")
            return False
        else:
            for sub in path.iterdir():
                logging.error(f"Error, path={path} is a dir and not empty")
                return False
    else:
        logging.info(f"Make site dir = {path}")
        path.mkdir()

    logging.info("Read basic info")
    title, initials, description, author = _read_input()
    title = nvl(title, "My Awesome Blog").strip()
    initials = nvl(initials, title).strip()
    description = nvl(description, "A weblog Site").strip()
    author = nvl(author, "Someone").strip()
    now = pendulum.now("UTC").format("YYYY-MM-DD HH:mm:ss")

    logging.info("Create configurations")
    # update config
    config_template = SiteSkeleton.config_template
    config_local = Path(path, SiteSkeleton.config)
    # _config = loadf_config(config_template, encoding="utf-8")
    raw_config = toml.load(config_template)
    raw_config["title"] = title
    raw_config["site"]["initials"] = initials
    raw_config["site"]["description"] = description
    raw_config["author"]["name"] = author
    with open(config_local, "w") as fw:
        toml.dump(raw_config, fw)

    logging.info("Create content and posts")
    content_dir = SiteSkeleton.content
    posts_dir = SiteSkeleton.content_posts
    files = [
        {
            "name": "index.md",
            "text": _demo_index(now, title, description),
            "dir": content_dir,
        },
        {"name": "about.md", "text": _demo_about(now), "dir": content_dir},
        {"name": "first-post.md", "text": _demo_post(now), "dir": posts_dir},
    ]
    for entry in files:
        edir = Path(entry["dir"])
        efile = Path(edir, entry["name"])
        if not edir.exists():
            edir.mkdir()
        with open(efile) as f:
            f.write(entry["text"])

    logging.info("Copy builtin theme")
    theme_name = raw_config["theme"]
    themes_local = Path(path, SiteSkeleton.themes)
    theme_template = Path(SiteSkeleton.themes, theme_name)
    if not themes_local.exists():
        themes_local.mkdir()

    shutil.copytree(theme_template, Path(themes_local, theme_name))
    logging.info("Finished")
