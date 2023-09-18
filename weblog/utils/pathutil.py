"""file or dir: is_hidden, suffix, filename check and split"""
from pathlib import PurePath


def is_hidden_file(path: str) -> bool:
    return path and path.startswith(".")


def obtain_file_suffix(path: str) -> str:
    # todo
    assert path is not None
    # PurePath(filename).suffix.lower()
    return path.split(".")[-1].lower()


def obtain_file_stem(path: str) -> str:
    return path.split("/")[-1].split(".")[0]


def is_index_filename(filename, stem=False):
    name = filename
    if stem:
        name = obtain_file_stem(filename)
    return name in ["index", "_index"]


def concat_path(*args, to_str=False):
    path = PurePath(*args)
    if to_str:
        path = str(path)
    return path


def split_paths(path, parent):
    child_parts = PurePath(path).parts
    start = 0
    if path.startswith(parent):
        start = len(PurePath(parent).parts)
    return child_parts[start:]
