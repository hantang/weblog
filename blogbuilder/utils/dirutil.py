"""dir traverse"""
import logging
import os
from typing import List

from .pathutil import is_hidden_file, obtain_file_suffix

flag_include = "^"
flag_type = "*"
flag_type_include = flag_include + flag_type


def get_keep_dirs(dirs: List) -> List:
    limit_dirs = []
    if dirs:
        assert len([v for v in dirs if flag_include in v]) == 0
        limit_dirs = [flag_include + v for v in dirs if len(v) > 0]
    return limit_dirs


def get_keep_files(types: List, files: List) -> List:
    limit_files = []
    if types:
        assert len([v for v in types if flag_include in v or flag_type in v]) == 0
        limit_files = [flag_type_include + v for v in types if len(v) > 0]
    elif files:
        limit_files = [flag_include + v for v in types if len(v) > 0]
    return limit_files


def walk(top, max_depth=2, limit_dirs=None, limit_files=None, limit_hidden=True):
    """
    遍历目录，限制递归深度
    > ref: https://github.com/python/cpython/blob/3.11/Lib/os.py#L345

    过滤或限制目录或文件名，不要使用特殊字符比如^*, ^保留文件（不排除），*（类型）
    * 目录：limit_dirs(仅top目录生效)
        * 所有目录 []
        * 仅排除某些目录 [draft, demo] (排除draft和demo)
        * 仅保留某些目录 [^post, ^test](保留，不排除post和test)
    * 文件：
        * 所有文件
        * 排除有些类型但保留特定文件 [*type(排除),  ^filename]
        * 保留有些类型但排除特定文件 [^*type(不排除), filename]
    * 隐藏文件或目录过滤
    """

    if limit_dirs:
        keep_dirs = [d.split(flag_include)[-1] for d in limit_dirs if d.startswith(flag_include)]
        ignore_dirs = [d for d in limit_dirs if not d.startswith(flag_include)]
    else:
        keep_dirs = []
        ignore_dirs = []

    if limit_files:
        ignore_types = [f.lstrip(flag_type) for f in limit_files if f.startswith(flag_type)]
        keep_files = [f.lstrip(flag_include) for f in limit_files
                      if f.startswith(flag_include) and not f.startswith(flag_type_include)]

        keep_types = [f.lstrip(flag_type_include) for f in limit_files if f.startswith(flag_type_include)]
        ignore_files = [f for f in limit_files if not (f[0] in flag_type_include)]
    else:
        keep_files = []
        keep_types = []
        ignore_files = []
        ignore_types = []

    assert len(keep_dirs) == 0 or len(ignore_dirs) == 0
    assert (len(keep_types + ignore_types + keep_files + ignore_files) == 0
            or len(ignore_types) > 0 and len(keep_files) >= 0 and len(keep_types + ignore_files) == 0
            or len(keep_types) > 0 and len(ignore_files) >= 0 and len(ignore_types + keep_files) == 0)

    logging.debug(f"dir: keep_dirs={keep_dirs}, ignore_dirs={ignore_dirs}")
    logging.debug(f"files1: keep_types={keep_types}, ignore_files={ignore_files}")
    logging.debug(f"files2: ignore_types={ignore_types}, keep_files={keep_files}")

    return _walk(top, True, None, False,
                 max_depth, max_depth, keep_dirs, ignore_dirs,
                 keep_files, keep_types, ignore_files, ignore_types, limit_hidden)


def _walk(top, topdown, onerror, followlinks,
          max_depth, total_depth, keep_dirs, ignore_dirs,
          keep_files, keep_types, ignore_files, ignore_types, limit_hidden):
    dirs, nondirs = [], []
    if max_depth < 0:
        return top, dirs, nondirs

    dirs_all, nondirs_all = [], []
    scandir_it = os.scandir(top)
    with scandir_it:
        while True:
            try:
                entry = next(scandir_it)
            except StopIteration:
                break
            name = entry.name
            is_dir = entry.is_dir()
            if is_dir:
                dirs_all.append(name)
            else:
                nondirs_all.append(name)

            # hidden files or dirs filter
            if limit_hidden and is_hidden_file(name):
                continue

            if flag_include in name or flag_type in name:
                logging.warning(f"bad dir/file name = {name}")

            if is_dir:
                if max_depth == total_depth:
                    # 顶级目录过滤
                    if keep_dirs:
                        if name in keep_dirs:
                            logging.debug("Add keep dir = {}".format(name))
                            dirs.append(name)
                    elif ignore_dirs:
                        if name not in ignore_dirs:
                            logging.debug("Add not ignore dir = {}".format(name))
                            dirs.append(name)
                    else:
                        logging.debug("Add all dir = {}".format(name))
                        dirs.append(name)
                else:
                    dirs.append(name)

                # TODO followlinks and entry.is_symlink()
            else:
                filetype = obtain_file_suffix(name)
                if len(keep_types + ignore_types) == 0:
                    nondirs.append(name)
                elif len(keep_types) > 0:
                    if filetype in keep_types and name not in ignore_files:
                        nondirs.append(name)
                elif len(ignore_types) > 0:
                    if filetype not in ignore_types or name in keep_files:
                        nondirs.append(name)
    logging.debug(f"top-dir={top}, dirs={dirs}, non-dirs={nondirs}")
    logging.debug(f"  all-dirs={dirs_all}, filtered=({len(dirs_all) - len(dirs)})")
    logging.debug(f"  all-non-dirs={nondirs_all}, filtered=({len(nondirs_all) - len(nondirs)})")
    yield top, dirs, nondirs

    # only topdown recursion
    for dirname in dirs:
        new_path = os.path.join(top, dirname)
        if followlinks or not os.path.islink(new_path):
            yield from _walk(new_path, topdown, onerror, followlinks,
                             max_depth - 1, total_depth, keep_dirs, ignore_dirs,
                             keep_files, keep_types, ignore_files, ignore_types, limit_hidden)
