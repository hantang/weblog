"""
markdown文件内容解析
"""
import logging
import os
import re
from pathlib import PurePath

from .utils.dateutil import get_date_part, get_datetime
from .utils.fileutil import divide_textfile
from .utils.mdutil import MarkdownParser
from .utils.pathutil import concat_path, is_index_filename, obtain_file_stem, obtain_file_suffix


class BlogMeta:
    keys = [
        "title",
        "author",
        "layout",
        "date",
        "lastmod",
        "draft",
        "slug",
        "cover",
        "categories",
        "tags",
        "series",
        "keywords",
        "page",
        "summary",
        "comment",
    ]
    inherit_keys = [
        "author", "layout", "date", "paginate", "page"
    ]

    def __init__(self, meta_data):
        self.meta_data = meta_data if meta_data else {}
        self._title = None
        self._datetime = None
        self._layout = None
        self._author = None
        self._summary = None
        self._paginate = None
        self._get()

    @property
    def title(self):
        return self._title

    @property
    def datetime(self):
        return get_datetime(self._datetime)

    @property
    def date(self):
        return "/".join(self._datetime_parts)

    @property
    def date_year_month(self):
        return "-".join(self._datetime_parts[:2])

    @property
    def date_year(self):
        return self._datetime_parts[0]

    @property
    def layout(self):
        return self._layout

    @property
    def author(self):
        return self._author

    @property
    def summary(self):
        return self._summary

    @property
    def paginate(self):
        return 0 if self._paginate is None else self._paginate

    def _get(self):
        self._title = self.meta_data.get("title", "")
        self._datetime = str(self.meta_data.get("date", "1970-01-01"))
        self._layout = self.meta_data.get("layout")
        self._author = self.meta_data.get("author")
        self._summary = self.meta_data.get("summary")
        self._paginate = self.meta_data.get("paginate")
        self._datetime_parts = get_date_part(self._datetime)

    def update_meta(self, new_meta, overwrite=False):
        """本地>上级目录>根目录配置"""
        for k, v in new_meta.items():
            if k not in BlogMeta.inherit_keys:
                continue
            if k == "page":  # todo
                if k in self.meta_data:
                    for k2, v2 in new_meta[k].items():
                        if overwrite and k2 not in self.meta_data[k]:
                            self.meta_data[k][k2] = v2
                else:
                    self.meta_data[k] = v.copy()
            else:
                if overwrite or k not in self.meta_data:
                    self.meta_data[k] = v
        self._get()

    def get_meta(self):
        return self.meta_data


class BlogBody:
    def __init__(self, body_raw) -> None:
        self.parser_markdown = MarkdownParser()
        self.raw = body_raw
        self.text = "".join(body_raw)

        self._html = ""
        self._html_toc = ""
        self._images = []

    def render(self, toc):
        if toc:
            logging.debug("==>> post with toc")
            raw_html_text, raw_html_toc = self.parser_markdown(self.text, toc)
        else:
            raw_html_text = self.parser_markdown(self.text)
            raw_html_toc = None
        self._html = raw_html_text
        self._html_toc = raw_html_toc

        img = self.parser_markdown.get_images_map()
        self._images = set([i[0] for i in img])
        if len(img) > 0:
            logging.debug("==>> parser_markdown = {}".format(img))

    @property
    def html(self):
        return self._html

    @property
    def toc(self):
        return self._html_toc

    @property
    def images(self):
        logging.debug("==>> images = {}".format(", ".join(self._images)))
        return self._images


class BlogContent:
    """解析markdown文件: front matter + 正文内容
    index.md -> /index.html (/<topic>/<slug>/index.html)
    about.md -> /about/index.html (/about/<slug>/index.html)
    topic1/post1.md -> /topic1/post1/index.html
    topic2/project1/project1.md -> /topic2/project1/index.html
    """

    def __init__(self, dirpath, filename, subdirs=None, max_depth=-1, toc=False) -> None:
        self.dirpath = dirpath
        self.subdirs = subdirs

        name = obtain_file_stem(filename)
        self.topic = ""
        if len(subdirs) > 0:
            self.topic = subdirs[0]
        elif len(subdirs) == 0 and not (is_index_filename(name)):
            self.topic = name

        self.slug = ""
        if len(subdirs) == 2:
            self.slug = subdirs[1]
        elif len(subdirs) == 1 and not (is_index_filename(name)):
            self.slug = name
        self.slug = re.sub(r"[\s_.]+", "-", self.slug)

        self.toc = toc
        self.charset = "utf-8"
        self.filepath = concat_path(dirpath, filename)
        self.filename = filename
        self.filetype = obtain_file_suffix(filename)  # dict
        logging.debug(f"==> content: filepath={self.filepath}, subdirs={subdirs}, topic={self.topic}, slug={self.slug}")

        self.meta, self.body = self._parse_file()

        self.url_base = "{}/{}".format(self.topic, self.slug).strip("/")
        self.url_name = "index.html"
        # self.url_full = "{}/{}".format(self.url_base, self.url_name).lstrip("/")
        self.url_prev = None
        self.url_next = None
        self.url_topic = self.topic.strip("/")

    def update_meta(self, new_meta, overwrite=False):
        self.meta.update_meta(new_meta, overwrite)

    def get_meta(self):
        return self.meta.get_meta()

    def set_urls(self, url_prev, url_next):
        self.url_prev = url_prev.strip("/") if url_prev else None
        self.url_next = url_next.strip("/") if url_next else None

    def get_layout(self, default="page"):
        # todo
        logging.debug(f"==>> {self.filepath}, layout={self.meta.layout}, default={default}")
        return default

    def get_info(self):
        info = {
            "datetime": self.meta.datetime,
            "date": self.meta.date,
            "date_year_month": self.meta.date_year_month,
            "date_year": self.meta.date_year,
            "author": self.meta.author,
            "title": self.meta.title,
            "summary": self.meta.summary,
            "url_base": self.url_base,
        }
        logging.debug("==>>  content info = {}".format(info))
        return info

    def render(self, layout=None, toc=False):
        self.body.render(toc)

    def get_output(self):
        return self.body.html

    def get_toc(self):
        return self.body.toc

    def get_images(self):
        dirpath = self.dirpath
        images_path = [
            PurePath(dirpath, img_path) for img_path in self.body.images
        ]
        return images_path

    def _parse_file(self) -> tuple[BlogMeta, BlogBody]:
        """
        1. 元数据信息解析, 得到url
        2. 正文内容解析，得到图片路径
        """
        if os.path.exists(self.filepath):
            (meta_raw, meta_type, meta_data), body_raw = divide_textfile(self.filepath, self.charset)
        else:
            logging.warning(f"!!! content path({self.filepath}) not exits")
            meta_data = {}
            body_raw = ""
        meta = BlogMeta(meta_data)
        body = BlogBody(body_raw)
        return meta, body
