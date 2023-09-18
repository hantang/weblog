import logging
from pathlib import Path
from textwrap import dedent
import pendulum
import toml
import shutil

from weblog.process import SiteSkeleton
from weblog.utils.configutil import loadf_config

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
    return dedent(post).lstrip()


def _demo_about(now):
    text = f"""
    ---
    title: "about"
    date: "{now}"
    draft: false
    ---

    ## About
    """
    return dedent(text).lstrip()


def _demo_index(now, title, description=""):
    text = f"""
    ---
    title: "{title}"
    date: "{now}"
    draft: false
    description: "{description}"
    ---
    """
    return dedent(text).lstrip()


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
    base_url = input("Site url:\n")
    return title, initials, description, author, base_url


def init(path, query, encoding="utf-8"):
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
    site_path = Path(path)
    if site_path.exists():
        if site_path.is_file():
            logging.error(f"Error, site path={site_path} is a file and exits")
            return False
        else:
            for sub in site_path.iterdir():
                logging.error(f"Error, site path={site_path} is a dir and not empty")
                return False
    else:
        logging.info(f"Make site dir = {site_path}")
        site_path.mkdir()

    logging.info("Read basic info")
    if query:
        title, initials, description, author, base_url = _read_input()
    else:
        title, initials, description, author, base_url = None, None, None, None, None
    title = nvl(title, "My Awesome Blog").strip()
    initials = nvl(initials, title).strip()
    description = nvl(description, "A weblog Site").strip()
    author = nvl(author, "Someone").strip()
    base_url = nvl(base_url, "").strip()
    now = pendulum.now("UTC").format("YYYY-MM-DD HH:mm:ss")

    logging.info(f"""settings:
        title={title}
        initials={initials}
        description={description}
        author={author}
        """)

    logging.info("Create configurations")
    # update config
    BASEDIR = SiteSkeleton.BASEDIR
    config_template = Path(BASEDIR, SiteSkeleton.config_template)
    config_local = Path(site_path, SiteSkeleton.config)
    raw_config = loadf_config(config_template, encoding=encoding)

    raw_config['url'] = base_url
    raw_config["title"] = title
    raw_config["site"]["initials"] = initials
    raw_config["site"]["description"] = description
    raw_config["author"]["name"] = author

    logging.info(f"config_local = {config_local}")
    with open(config_local, "w", encoding=encoding) as fw:
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
        data_dir = Path(site_path, entry["dir"])
        data_file = Path(data_dir, entry["name"])
        # logging.info(f"mkdir={edir}, file={efile}")
        if not data_dir.exists():
            data_dir.mkdir()
        with open(data_file, "w", encoding=encoding) as f:
            f.write(entry["text"])

    logging.info("Copy builtin theme")
    theme_name = raw_config["theme"]
    themes_local = Path(site_path, SiteSkeleton.themes)
    theme_template = Path(BASEDIR, SiteSkeleton.themes, theme_name)
    if not themes_local.exists():
        themes_local.mkdir()

    shutil.copytree(theme_template, Path(themes_local, theme_name))
    logging.info("Finished")
