"""toml/yaml configuration files or strings check and load"""
import logging
from pathlib import Path

import toml
import yaml

from weblog.utils.pathutil import obtain_file_suffix

YAML_FORMAT = "YAML"
TOML_FORMAT = "TOML"
YAML_SUFFIX = ["yaml", "yml"]
TOML_SUFFIX = ["toml"]
YAML_SEP = "-" * 3
TOML_SEP = "=" * 3


def loadf_config(filename: str, encoding: str = "utf-8") -> dict:
    data = {}
    filepath = Path(filename)
    if not filepath.exists():
        logging.error(f"??? config {filename} NOT EXISTS")
        return data

    filetype = check_config_type(filename)
    logging.debug(f"==>> {filename} type = `{filetype}`")

    with open(filepath, encoding=encoding) as f:
        if filetype == YAML_SUFFIX:
            data = yaml.safe_load(f)
        elif filetype == TOML_SUFFIX:
            data = toml.load(f)
    return data


def loads_config(text: str, filetype: str) -> dict:
    data = {}
    text = text.strip()
    logging.debug("==>> config string, text len = {}".format(len(text)))
    if len(text) > 0:
        if filetype == YAML_FORMAT:
            data = yaml.safe_load(text)
        elif filetype == TOML_FORMAT:
            data = toml.loads(text)
    return data


def check_config_type(filename: str) -> str:
    suffix = obtain_file_suffix(filename)
    logging.debug(f"==>> check config type, suffix = `{suffix}`")
    if suffix in YAML_SUFFIX:
        return YAML_FORMAT
    elif suffix in TOML_SUFFIX:
        return TOML_SUFFIX
    return None


def check_config_sep(line_sep: str) -> bool:
    return line_sep in [TOML_SEP, YAML_SEP]


def obtain_config_type(line_sep: str) -> str:
    logging.debug(f"==>> check line sep type = `{line_sep}`")
    if line_sep == YAML_SEP:
        return YAML_FORMAT
    elif line_sep == TOML_SEP:
        return TOML_FORMAT
    return None
