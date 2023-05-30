import mistune
from mistune.directives import RSTDirective, TableOfContents


class MyRenderer(mistune.HTMLRenderer):
    def codespan(self, text):
        if text.startswith('$') and text.endswith('$'):
            return '<span class="math">' + mistune.escape(text) + '</span>'
        return '<code>' + mistune.escape(text) + '</code>'


class MarkdownParser:
    def __init__(self):
        # plugins: https://mistune.lepture.com/en/latest/plugins.html
        plugins = ["strikethrough", "footnotes", "table",
                    "task_lists", "superscript", "subscript", "math"] + \
                    [RSTDirective([TableOfContents()])]

        self.parser = mistune.create_markdown(escape=False, plugins=plugins)

    def parse(self, s: str):
        return self.parser(s)

    def __call__(self, s: str):
        if s is None:
            s = '\n'
        return self.parse(s)
