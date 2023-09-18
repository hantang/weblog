from jinja2 import Environment, FileSystemLoader


class TemplateUtil:
    def __init__(self, files_path):
        self.env = Environment(loader=FileSystemLoader(files_path),
                               trim_blocks=True, lstrip_blocks=True)

    def render(self, layout_name, params):
        tpl_index = self.env.get_template(layout_name)
        out = tpl_index.render(**params)
        return out

    def __call__(self, layout_name, params):
        return self.render(layout_name, params)
