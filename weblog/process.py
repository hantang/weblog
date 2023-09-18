"""自定义静态博客实现"""
import logging
import os
import shutil
from pathlib import Path

from weblog.config import BlogConfig
from weblog.content import BlogContent
from weblog.theme import BlogTheme
from weblog.utils.dateutil import get_datetime, get_deltatime, get_time_now
from weblog.utils.dirutil import get_keep_dirs, get_keep_files, walk
from weblog.utils.pathutil import is_index_filename, obtain_file_stem, split_paths


# todo
class SiteSkeleton:
    # 基本的目录结构
    BASEDIR = os.path.dirname(os.path.abspath(__file__))
    content = "content/"
    content_posts = f"{content}posts/"
    deploy = "deploy/"
    # themes = "../themes/"
    themes = "themes/"
    config = "config.toml"
    config_template = f"config/{config}"


class TextTypes:
    def __int__(self):
        self._types = {
            "Markdown": ["md", "markdown"],
            "reStructuredText": ["rst", "rest"],
            "text": ["txt", "text"]
        }
        self._markdown = self._types["Markdown"]

    @property
    def markdown(self):
        # return self._markdown
        return ["md", "markdown"]  # todo error


class BlogBuilder:
    """从读取到生成的整个流程"""

    def __init__(self) -> None:
        self.config_file = SiteSkeleton.config
        self.content_dir = SiteSkeleton.content
        self.deploy_dir = SiteSkeleton.deploy

        self.config = BlogConfig(self.config_file)
        self.theme_name = self.config.theme
        self.theme_dir = SiteSkeleton.themes + self.theme_name
        self.text_types = TextTypes()
        logging.debug("==>> init theme = {}".format(self.theme_dir))

    def get_theme(self):
        # todo
        assert os.path.exists(self.theme_dir)

    def get_contents(self):
        """读取content中markdown文件
        max_depth: 限制3级目录下的md需要是index/_index/同目录名文件
        满足条件：(index/_index特殊)
            content/xx.md
            content/topic/xx.md
            content/topic/xx/{xx, index, _index}.md
        """
        content_dir = self.content_dir
        remained_dir = self.config.remained_dir
        max_depth = self.config.max_depth
        menu_dirs = self.config.menu_dirs
        logging.debug(f"==>> content_dir = {content_dir}")

        candidate_dirs = get_keep_dirs(menu_dirs)
        candidate_files = get_keep_files(self.text_types.markdown, None)
        content_list = []
        walker = walk(content_dir,
                      max_depth=max_depth,
                      limit_dirs=candidate_dirs,
                      limit_files=candidate_files)

        for dirpath, dirnames, filenames in walker:
            subdirs = split_paths(dirpath, content_dir)
            assert 0 <= len(subdirs) < max_depth

            if len(subdirs) == max_depth - 1:
                # 仅保留 xx/{xx, index, _index}.md
                all_names = {obtain_file_stem(name): name for name in filenames}  # 去除后缀，得到文件名
                keep_names = [name for name in all_names.keys() if name == subdirs[-1]] + \
                             [name for name in all_names.keys() if is_index_filename(name)]
                if len(keep_names) > 0:
                    filenames = [all_names[keep_names[0]]]
                else:
                    filenames = []
                logging.debug("subdirs = {}, filenames = {}".format(subdirs, filenames))

            for filename in filenames:
                if len(subdirs) == 0 and obtain_file_stem(filename) in remained_dir:
                    logging.warning(f"!!! error filename = {filename}, conflict to remained dir")
                    continue
                content = BlogContent(dirpath, filename, subdirs, max_depth)
                content_list.append(content)

        logging.info("==> total content_list = {}".format(len(content_list)))
        return content_list

    def get_htmls(self, content_list):
        # params = self.config.params
        self.get_theme()

        template = BlogTheme(self.content_dir, self.theme_dir, self.deploy_dir, self.config, content_list)

        template.generate()
        template.generate_404()
        template.process_resources()

    def clean(self):  # todo overwrite
        if Path(self.deploy_dir).exists():
            logging.info(f"clean deploy_dir = {self.deploy_dir}")
            shutil.rmtree(self.deploy_dir)

    def build_all(self):
        start = get_time_now()

        self.clean()
        content_list = self.get_contents()
        self.get_htmls(content_list)

        end = get_time_now()
        logging.info("=" * 20 + " FIN " + "=" * 20)
        logging.info(f"total content file = {len(content_list)}")
        logging.info(f"run time: {get_datetime(start, date=False)} -> {get_datetime(end, date=False)}")
        logging.info(f"total time = {get_deltatime(start, end)}")
