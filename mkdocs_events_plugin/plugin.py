import mkdocs
import re
import os
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, Template, select_autoescape

DIR_PATH = Path(os.path.dirname(os.path.realpath(__file__)))
EVENTS_PAGE_PATTERN = re.compile(
    r"\{\{\s*events_content\s*\}\}", flags=re.IGNORECASE)

class EventsConfig(mkdocs.config.base.Config):
    events_dir = mkdocs.config.config_options.Type(str, default='events')

class EventsPlugin(mkdocs.plugins.BasePlugin[EventsConfig]):

    def __init__(self):
        self.events_dir = None
        self.jinja_template = None
        self.pages = []

    def on_config(self, mkdocs_config):
        self.events_dir = self.config.get("events_dir")

        # Setup jinja template
        search_paths = [DIR_PATH / "templates"]

        env = Environment(
            loader=FileSystemLoader(search_paths),
            autoescape=select_autoescape()
        )

        self.jinja_template = env.get_template("events.html")

    def on_serve(self, server, config, builder):
        return server


    def on_page_content(self, html, page, config, files):

        file_path = Path(page.file.src_path)

        if Path(self.events_dir) in file_path.parents:
                self.pages.append(page)

        return
    
    def on_page_markdown(self, markdown, page, config, files):
        return markdown

    def on_post_page(self, output, page, config):
        match = EVENTS_PAGE_PATTERN.search(output)

        if match:
            html = self.generate_html()
            result = EVENTS_PAGE_PATTERN.sub(
                html,
                output,
            )
            output = result

        return output

    def generate_html(self) -> str:
        template = self.jinja_template
        sorted_pages = sorted(self.pages, key=lambda page: datetime.strptime(page.meta["start_date"], '%d/%m/%Y'))
        return template.render(pages=sorted_pages, page_num=len(self.pages))


    