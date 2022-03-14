from pathlib import Path
from bs4 import BeautifulSoup

import urllib.request
import config
import json
import os

logger = config.logger


class WebSpider():
    def __init__(self, url: str, domain: str, source_name: str) -> None:
        """
        Create an HTMLParser Object

        After instantiating an Object, call scrape_page() followed by build_page()
        and finally write_to_html()

        Args:
            file (str): Filename of the corresponding HTML File to pe parsed
        """

        self.url = url
        self.domain = domain
        self.source_name = source_name

        with open("config.json", "r") as f:
            self.config = json.load(f)

        """if not os.path.exists(Path.cwd() / self.config['HTML_input_path'] / self.file):
            logger.error(f"File '{self.file}' not found!")
            raise FileNotFoundError(f"File '{self.file}' not found!")"""

        # logger.debug(f"Build HTMLParser with file '{file}'")

    def get_html(self) -> None:
        """
            Parse HTML into Soup Object

            Loads the content of the file specified in 'self.file'
        """

        """res = urllib.request.urlopen(self.url)

        css_res = urllib.request.urlopen(
            "https://www.w3schools.com/lib/w3schools30.css")
        c = css_res.read()

        _res = res.read()

        with open(Path.cwd() / self.config['HTML_input_path'] / "test.html", "w", encoding="utf-8") as f:
            r = str(_res, "utf-8")
            r = r.replace("<!DOCTYPE html>",
                          "<!DOCTYPE html><style>" + str(c, "utf-8") + "</style>")

            f.write(r)

        soup = BeautifulSoup(_res, 'html.parser')
        t = soup.find("div", attrs={"id": "sidenav"})
        tags = t.find_all("a")

        for tag in tags:
            res = urllib.request.urlopen(self.url + tag["href"])

            _res = res.read()

            with open(Path.cwd() / self.config['HTML_input_path'] / tag["href"].replace(".asp", ".html"), "w", encoding="utf-8") as f:
                r = str(_res, "utf-8")
                r = r.replace("<!DOCTYPE html>",
                              "<!DOCTYPE html><style>" + str(c, "utf-8") + "</style>")

                f.write(r)"""

        """session = HTMLSession()
        response = session.get(self.url)

        response.html.render()
        r = response.html.html

        with open(Path.cwd() / self.config['HTML_input_path'] / "test.html", "w", encoding="utf-8") as f:
            soup = BeautifulSoup(r, 'html.parser')
            soup.append("<style>background-color:black</style>")
            f.write(str(soup))"""

    def write_to_html(self) -> None:
        """
            Write HTML to specified output directory
        """

        with open("link_location_list.json", "r") as f:
            link_location = json.load(f)

        res = urllib.request.urlopen(self.url)

        css_res = urllib.request.urlopen(link_location[self.source_name][2])

        c = css_res.read()

        _res = res.read()

        with open(Path.cwd() / self.config['HTML_input_path'] / "test.html", "w", encoding="utf-8") as f:
            r = str(_res, "utf-8")
            r = r.replace("<!DOCTYPE html>",
                          "<!DOCTYPE html><style>" + str(c, "utf-8") + "</style>")

            f.write(r)

        soup = BeautifulSoup(_res, 'html.parser')
        t = soup.find("div", attrs={
                      link_location[self.source_name][0]: link_location[self.source_name][1]})
        tags = t.find_all("a")

        for tag in tags:
            if (not tag["href"].startswith("/")) and (not self.domain.endswith("/")):
                continue

            if tag["href"].startswith("/w/"):
                continue

            if "#" in tag["href"]:
                continue

            res = urllib.request.urlopen(self.domain + tag["href"])

            _res = res.read()

            with open(Path.cwd() / self.config['HTML_input_path'] / (os.path.basename(tag["href"]) + ".html"), "w", encoding="utf-8") as f:
                r = str(_res, "utf-8")
                r = r.replace("<!DOCTYPE html>",
                              "<!DOCTYPE html><style>" + str(c, "utf-8") + "</style>")

                f.write(r)
