import logging
import re

import mistune
from mistune import HTMLRenderer
from mistune.toc import add_toc_hook, render_toc_ul
from mistune.util import escape as escape_text, safe_entity, striptags
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

from blogbuilder.utils.fileutil import get_img_pattern


def heading_id(token, index):
    return str(token.get("text", "toc_" + str(index + 1)))


def render_html_toc(toc_items, title=None, collapse=False):
    if not title:
        title = "Table of Contents"
    content = render_toc_ul(toc_items)

    html = '<details class="toc"'
    if not collapse:
        html += " open"
    html += ">\n<summary>" + title + "</summary>\n"
    return html + content + "</details>\n"


class MyRenderer(HTMLRenderer):
    def __init__(self, escape=True, use_local_img=True, use_figure=True):
        super(MyRenderer, self).__init__(escape)
        self.image_urls = []
        self.link_urls = []
        self.use_local_img = use_local_img
        self.use_figure = use_figure
        self.img_pattern_md, _, self.img_pattern_md_idx = get_img_pattern("markdown")
        self.img_pattern_html, _, (self.img_pattern_html_idx_full,
                                   self.img_pattern_html_idx) = get_img_pattern("html")

    def block_code(self, code, info=None):
        # https://mistune.lepture.com/en/latest/guide.html#customize-renderer
        if info:
            info = safe_entity(info.strip())
            try:
                lexer = get_lexer_by_name(info, stripall=True)
                formatter = HtmlFormatter()  # linenos='table'/'inline, filename=info
                lang = info.split(None, 1)[0]
                text = highlight(code, lexer, formatter)
                out = text.replace("<pre>", "<pre><code>").replace("</pre>", "</code></pre>")
                out = out.replace('class="highlight"', 'class="highlight language-{}"'.format(lang))
                return out
            except:
                logging.warning(f"error html.HtmlFormatter(), info={info}")
        return super().block_code(code, info)

    def block_html(self, html: str) -> str:
        """block_text, block_html, text, inline_html"""
        out = super().block_html(html)
        imgs, new_out = self._img_html(out)
        if imgs and len(imgs) > 0:
            logging.error("block_html, image_urls={},  imgs = {}".format(self.image_urls, imgs))
            for entry in imgs:
                self.image_urls.append(entry[:2] + ["html"])
        return new_out

    def image(self, text: str, url: str, title=None, *args) -> str:
        """todo support
            ![text](img.png){ width=60%,height:30px }
        """
        src = self.safe_url(url)
        alt = escape_text(striptags(text))

        src2 = self._img_src(src)
        self.image_urls.append([src, src2, "markdown"])
        src_url = src2 if self.use_local_img else src
        title2 = safe_entity(title) if title else ""
        s = '<img src="{}" alt="{}" title="" />'.format(src_url, alt, title2)
        if self.use_figure and title:
            s = f"<figure>\n{s}\n<figcaption>{title2}</figcaption>\n</figure>"
        return s

    def _img_html(self, html, replace=True):
        out = re.findall(self.img_pattern_html, html)
        new_html = html
        if replace:
            new_html = re.sub(self.img_pattern_html, r'\2\7\9', html)

        if out and len(out) > 0:
            out = [[o[self.img_pattern_html_idx_full],
                     o[self.img_pattern_html_idx]] for o in out]
        return out, new_html

    def _img_src(self, img_url):
        out = re.match(self.img_pattern_md, img_url)
        if out is None:
            return img_url
        else:
            return out.groups()[self.img_pattern_md_idx]


class MarkdownParser:
    def __init__(self, min_level=1, max_level=3):
        # plugins: https://mistune.lepture.com/en/latest/plugins.html
        plugins = [
            "strikethrough",
            "footnotes",
            "table",
            "task_lists",
            "superscript",
            "subscript",
            "math",
        ]

        self.parser = mistune.create_markdown(renderer=MyRenderer(False), plugins=plugins)
        add_toc_hook(self.parser, min_level, max_level, heading_id=heading_id)

    def parse(self, s: str):
        return self.parser(s)

    def parse_toc(self, s: str):
        html, state = self.parser.parse(s)
        toc_items = state.env["toc_items"]
        toc_html = render_html_toc(toc_items)
        return html, toc_html

    def __call__(self, s: str, toc=False):
        if s is None:
            s = "\n"
        if toc:
            return self.parse_toc(s)
        return self.parse(s)

    def get_images_map(self):
        return self.parser.renderer.image_urls
