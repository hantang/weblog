import logging

import pendulum

from .utils.configutil import loadf_config


class BlogConfig:
    keys = [
        "url",
        "title",
        "theme",
        "menu",
        "site",
        "author",
        "taxonomies",
        "page",
        "info"
    ]

    def __init__(self, config_file, encoding="utf-8") -> None:
        # todo 合法的key
        logging.debug(f"==>> read from = {config_file}")
        self._config = loadf_config(config_file, encoding)
        self._check()
        self._menu = self._config["menu"]
        self._title = self._config["title"]
        self._theme = self._config["theme"]
        self._author = self._config["author"]

        self._params = self._proc_params()
        self._meta_params = self._proc_meta()
        self._menu2 = self._proc_menu()

        self._remained_dir = ["assets", "static", "drafts", "archives", "page"]
        self._max_depth = 3

    def _proc_menu(self):
        menu = []
        for entry in self._menu:
            menu.append({
                "topic": entry["url"].strip().strip("/"),
                "url": entry["url"].strip(),
                "name": entry["name"].strip(),
                "weight": int(entry["weight"]),
            })
        return menu

    def _proc_params(self):
        return {
            key: self._config[key] for key in ["url", "title", "author", "menu", "site", "page", "info"]
        }

    def _proc_meta(self):
        # inherit_keys = ["author", "layout", "date", "page", "paginate"]
        meta_params = {}
        if self._config["author"].get("name"):
            meta_params["author"] = self._config["author"].get("name")
        if self._config["page"]:
            meta_params["page"] = self._config["page"]
        if self._config["site"]["paginate"]:
            meta_params["paginate"] = self._config["site"]["paginate"]
        if self._config["info"]["since"]:
            meta_params["date"] = pendulum.parse(self._config["info"]["since"])
        meta_params["layout"] = "page"
        return meta_params

    def _check(self):
        if self._config:
            menus = self._config["menu"]
            # name, url都必须唯一
            names = [m["name"] for m in menus]
            urls = [m["url"] for m in menus]
            assert len(names) == len(set(names)), len(urls) == len(set(urls))

    @property
    def remained_dir(self):
        return self._remained_dir

    @property
    def max_depth(self):
        return self._max_depth

    @property
    def menu_dirs(self):
        menu = [entry['topic'] for entry in self._menu2]
        assert len(menu) == len(set(menu))
        assert len(set(self._remained_dir) & set(menu)) == 0
        return menu

    @property
    def menu(self):
        return self._menu2

    @property
    def menu_topics(self):
        menu = [(entry['topic'], entry['weight']) for entry in self._menu2]
        menu = sorted(menu, key=lambda x: (x[1], x[0]))
        return [entry[0] for entry in menu]

    @property
    def theme(self):
        return self._theme

    @property
    def author_name(self):
        return self._author["name"]

    @property
    def params(self):
        return self._params

    @property
    def meta_params(self):
        return self._meta_params