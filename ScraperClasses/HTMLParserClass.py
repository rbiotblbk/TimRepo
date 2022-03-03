from bs4 import BeautifulSoup
from BaseClasses.BaseScraper import WebScraper
from pathlib import Path

import datetime
import json


class HTMLParser(WebScraper):
    def __init__(self, file: str) -> None:
        super().__init__()
        self.file = file
        self._cache = {}
        self.new_soup = BeautifulSoup("<!DOCTYPE html>", 'html.parser')

        with open("config.json", "r") as f:
            self.config = json.load(f)

    def scrape_page(self) -> None:
        """
            Parse HTML into Soup Object
        """

        # FIXME: Hardcoded HTMLs
        with open(Path.cwd().joinpath(f"{self.config['HTML_input_path']}/{self.file}"), "rb") as f:
            self.page = f.read()

        self.soup = BeautifulSoup(self.page, 'html.parser')

    def build_page(self) -> None:
        """
            Build a new Soup Object that only contains the necessary tags
        """

        tag = self.soup.find("style")
        self.new_soup.append(tag)

        # TODO: Change to JSON File
        tag_id_list = {"sidenav": ["append", None],
                       "main": ["append", "margin-left:220px;padding-top:0px"],
                       "mainLeaderboard": ["decompose", None],
                       "leftmenuinner": [None, " "],
                       "midcontentadcontainer": ["decompose", None]
                       }

        for id in tag_id_list:
            try:
                tag = self.soup.find("div", attrs={
                    'id': id})

                if not tag:
                    tag = self.new_soup.find("div", attrs={
                        'id': id})

                if tag_id_list[id][1]:
                    tag["style"] = tag_id_list[id][1]

                if tag_id_list[id][0] == "append":
                    self.new_soup.append(tag)
                elif tag_id_list[id][0] == "decompose":
                    tag.decompose()
            except:
                pass

    def write_to_html(self) -> None:
        """
            Write HTML to specified output directory
        """
        with open(Path.cwd().joinpath(f"{self.config['HTML_output_path']}/{self.file}"), "w", encoding="utf-8") as f:
            f.write(str(self.new_soup))

        print("File saved successfully!")

    def scrape_all(self) -> None:
        pass

    def get_page_content(self) -> bytes:
        return self.page.content

    def write_to_json(self) -> None:
        """
            Write JSON Object from data in self._cache
        """

        timestamp = datetime.datetime.now()
        timestamp = f"{timestamp.day}-{timestamp.month}-{timestamp.year} {timestamp.hour}-{timestamp.minute}"

        with open(f"Scraped_Files/{self.get_location()} {timestamp}.json", "w", encoding="utf-8") as file:
            json.dump(self._cache, file)
