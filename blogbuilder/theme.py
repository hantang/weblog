"""generate html files with jinja2 templates"""
import logging
import os
import shutil
from pathlib import Path, PurePath
from typing import List

from .config import BlogConfig
from .content import BlogContent
from .utils.tplutil import TemplateUtil


class ThemeSkeleton:
    layouts = "layouts"
    assets = "assets"
    static = "static"
    css = "css"
    js = "js"
    fonts = "fonts"

    layout_index = "index"
    layout_post = "post"
    layout_page = "page"
    layout_404 = "404"
    suffix = "html"
    favicon_name = "favicon.ico"


class BlogTheme:
    """渲染得到html"""

    def __init__(self, content_dir, theme_dir, deploy_dir, config: BlogConfig,
                 content_list: List[BlogContent], charset="utf-8") -> None:
        self.theme_dir = theme_dir
        self.content_dir = content_dir
        self.deploy_dir = deploy_dir

        self.config = config
        self.params = config.params
        self.meta_params = config.meta_params
        self.content_list = content_list
        self.charset = charset

        self.template = TemplateUtil(PurePath(theme_dir, ThemeSkeleton.layouts))
        logging.debug(f"params = {self.params}")
        logging.debug(f"meta_params = {self.meta_params}")

    def generate(self):
        topic_dict = self._group_contents()
        topic_list = self.config.menu_topics

        for topic in topic_list:
            entry = topic_dict[topic]
            page_index: BlogContent = entry["index"]
            page_contents: List[BlogContent] = entry["contents"]

            if page_index is None:
                # topic虚假的页面，仅用于展示post-list
                page_index = BlogContent(dirpath="{}/{}".format(self.content_dir, topic),
                                         filename="index.md", subdirs=[topic] if len(topic) > 0 else [])
            page_index.update_meta(self.meta_params)

            if topic == "":
                # 首页
                self._render(page_index, layout=ThemeSkeleton.layout_index)
            else:
                # 非首页：topic + posts
                inherit_params = page_index.get_meta()
                for page in page_contents:
                    page.update_meta(inherit_params)
                # 排序
                new_page_contents = self._sort_contents(page_contents)
                pages = [content.get_info() for content in new_page_contents]
                self._render(page_index, layout=ThemeSkeleton.layout_page, pages=pages)
                for content in new_page_contents:
                    self._render(content, layout=ThemeSkeleton.layout_post)

    def generate_404(self):
        self._render_404()

    def process_resources(self):
        # todo sitemap.xml, rss feed: index.html

        # static/favicon.ico
        favicons = [
            Path(self.content_dir, ThemeSkeleton.static, ThemeSkeleton.favicon_name),
            Path(self.theme_dir, ThemeSkeleton.static, ThemeSkeleton.favicon_name)
        ]
        favicon = favicons[0]
        if not favicon.exists():
            favicon = favicons[1]

        if favicon.exists():
            save_path = Path(self.deploy_dir, ThemeSkeleton.static)
            if not save_path.exists():
                save_path.mkdir()
            logging.debug(f"copy {favicon} files to target={save_path}")
            shutil.copyfile(favicon, Path(save_path, ThemeSkeleton.favicon_name))

        # assets/{css, js}
        assets_path = Path(self.theme_dir, ThemeSkeleton.assets)
        for suffix in [ThemeSkeleton.css, ThemeSkeleton.js, ThemeSkeleton.fonts]:
            sub_assets_path = Path(assets_path, suffix)
            if sub_assets_path.exists():
                logging.info(f"copy fonts = {sub_assets_path}")
                if suffix == ThemeSkeleton.fonts:

                    assets_files = sub_assets_path.glob("*.ttf")
                else:
                    assets_files = sub_assets_path.glob(f"*.{suffix}")
                if len(list(assets_files)) > 0:
                    save_path = Path(self.deploy_dir, ThemeSkeleton.assets, suffix)
                    # if not save_path.exists():
                    #     save_path.mkdir()
                    logging.debug(f"copy {suffix} files to target={save_path}")
                    shutil.copytree(sub_assets_path, save_path)

    def _group_contents(self):
        """group contents by topics(url)"""
        content_list: List[BlogContent] = self.content_list
        menu_list = self.config.menu

        topic_dict = {}
        for entry in menu_list:
            name, topic = entry["name"], entry["topic"]
            topic_dict[topic] = {
                "name": name,
                "index": None,
                "contents": [],
            }

        logging.debug("topic_dict = {}".format(topic_dict.keys()))
        for content in content_list:
            topic = content.topic
            slug = content.slug
            if topic not in topic_dict:
                logging.debug("not used content, topic = {}/{}".format(topic, content.filepath))
                continue

            if slug == "":
                topic_dict[topic]["index"] = content
            else:
                topic_dict[topic]["contents"].append(content)

        return topic_dict

    def _sort_contents(self, contents: List[BlogContent]):
        def sort_key(content):
            x = content.get_info()
            return x["datetime"], x["author"], x["url_base"]

        new_contents = sorted(contents, key=sort_key)
        for i, c in enumerate(new_contents):
            prev_url = None if i == 0 else new_contents[i - 1].get_info()["url_base"]
            next_url = None if i == len(new_contents) - 1 else new_contents[i + 1].get_info()["url_base"]
            c.set_urls(prev_url, next_url)
        return new_contents

    def _render(self, page_data: BlogContent, layout=ThemeSkeleton.layout_page, **kwargs):
        page_layout = page_data.get_layout(layout)
        if page_layout == ThemeSkeleton.layout_index:
            self._render_index(page_data)
        elif page_layout == ThemeSkeleton.layout_page:
            self._render_page(page_data, **kwargs)
        elif page_layout == ThemeSkeleton.layout_post:
            self._render_post(page_data)

        self._save_image(page_data)

    def _render_index(self, post_index: BlogContent, **kwargs):
        """
        首页：
        """
        layout = ThemeSkeleton.layout_index
        layout_name = ".".join([layout, ThemeSkeleton.suffix])
        params = self.params.copy()
        params["post_content"] = post_index.get_output()

        logging.info("==>> params since {}".format(params['info']['since']))
        out = self.template(layout_name, params)
        save_dir = post_index.url_base
        self._save(out, save_dir)

    def _render_post(self, post_content: BlogContent):
        """
        文章内容 TODO prev/next
        """
        layout = ThemeSkeleton.layout_post
        layout_name = ".".join([layout, ThemeSkeleton.suffix])
        params = self.params.copy()

        params["post_title"] = post_content.meta.title
        params["post_content"] = post_content.get_output()
        params["post_prev"] = post_content.url_prev
        params["post_next"] = post_content.url_next
        info = post_content.get_info()
        params["post_datetime"] = info["datetime"]
        params["post_author"] = info["author"]

        out = self.template(layout_name, params)
        save_dir = post_content.url_base
        self._save(out, save_dir)

    def _render_page(self, page_index: BlogContent, pages: List[BlogContent] = None):
        """
        两个部分：topic/index.md中内容 + topic/xxx 文章列表(标题+日期)
        """
        layout = ThemeSkeleton.layout_page
        layout_name = ".".join([layout, ThemeSkeleton.suffix])
        params = self.params.copy()

        params["post_content"] = ""
        if page_index:
            params["post_content"] = page_index.get_output()  # markdown -> html

        if pages is None: pages = []
        pages_list = []
        for page in pages[::-1]:
            pages_list.append({
                "title": page["title"],
                "date_year_month": page["date_year_month"],
                "url": page["url_base"].strip("/").split("/")[-1],
                "summary": page["summary"],
                "author": page["author"],
            })

        pages_by_ym = {}
        for entry in pages_list:
            ym = entry["date_year_month"]
            if ym not in pages_by_ym:
                pages_by_ym[ym] = [entry]
            else:
                pages_by_ym[ym].append(entry)
        ym_keys = sorted(pages_by_ym.keys(), reverse=True)
        pages_by_ym2 = [{"year_month": ym, "posts": pages_by_ym[ym]} for ym in ym_keys]

        params["post_list"] = pages_list  # generate post list
        params["post_list_grouped"] = pages_by_ym2
        logging.info("post_list_grouped = {}".format(ym_keys))

        out = self.template(layout_name, params)
        save_dir = page_index.url_base
        self._save(out, save_dir)

    def _render_404(self):
        """
        """
        layout = ThemeSkeleton.layout_404
        layout_name = ".".join([layout, ThemeSkeleton.suffix])
        params = self.params.copy()

        out = self.template(layout_name, params)
        self._save(out, save_dir=None, save_name=layout_name)

    def _save(self, output, save_dir=None, save_name=ThemeSkeleton.layout_index):
        if not save_name.endswith(".html"):
            save_name += ".html"

        save_path = Path(self.deploy_dir)
        if save_dir is not None and len(save_dir) > 0:
            save_path = Path(save_path, save_dir)
        if not save_path.exists():
            save_path.mkdir(parents=True)

        save_file = PurePath(save_path, save_name)
        with open(save_file, mode="w", encoding=self.charset) as fw:
            logging.info(f"save data(count={len(output)}) to target={save_file}")
            fw.write(output)

    def _save_image(self, page: BlogContent):
        save_dir = page.url_base
        save_path = PurePath(self.deploy_dir)
        if save_dir:
            save_path = PurePath(save_path, save_dir)
        images = page.get_images()
        for img_path in images:
            if os.path.exists(img_path):
                new_path = PurePath(save_path, PurePath(img_path).name)
                logging.debug(f"copy {img_path} to {new_path}")
                shutil.copyfile(img_path, new_path)
            else:
                logging.warning(f"{img_path} not exists")
