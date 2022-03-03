from bs4 import BeautifulSoup
from BaseClasses.BaseScraper import WebScraper
from pathlib import Path

import logging
import json
import os


logger = logging.getLogger()


class HTMLParser(WebScraper):
    def __init__(self, file: str) -> None:
        """
        Create an HTMLParser Object

        After instantiating an Object, call scrape_page() followed by build_page()
        and finally write_to_html()

        Args:
            file (str): Filename of the corresponding HTML File to pe parsed
        """
        super().__init__()

        self.file = file
        self.new_soup = BeautifulSoup("<!DOCTYPE html>", 'html.parser')

        with open("config.json", "r") as f:
            self.config = json.load(f)

        if not os.path.exists(Path.cwd().joinpath(f"{self.config['HTML_input_path']}/{self.file}")):
            logger.error(f"File '{self.file}' not found!")
            raise FileNotFoundError(f"File '{self.file}' not found!")

        logger.debug(f"Build HTMLParser with file '{file}'")

    def scrape_page(self) -> None:
        """
            Parse HTML into Soup Object
        """

        with open(Path.cwd().joinpath(f"{self.config['HTML_input_path']}/{self.file}"), "rb") as f:
            self.page = f.read()

        self.soup = BeautifulSoup(self.page, 'html.parser')

    def build_page(self) -> None:
        """
            Build a new Soup Object that only contains the necessary tags
        """

        tag = self.soup.find("style")
        self.new_soup.append(tag)

        with open("tag_id_list.json", "r") as f:
            tag_id_list = json.load(f)

        logger.debug(f"Loaded tags from file 'tag_id_list.json'")

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
                logger.debug(f"Tag with id '{id}' not found")

    def write_to_html(self) -> None:
        """
            Write HTML to specified output directory
        """
        with open(Path.cwd().joinpath(f"{self.config['HTML_output_path']}/{self.file}"), "w", encoding="utf-8") as f:
            f.write(str(self.new_soup))

        print("File saved successfully!")
        logger.info("File saved successfully!")

    def scrape_all(self) -> None:
        pass

    def get_page_content(self) -> bytes:
        pass

    def write_to_json(self) -> None:
        pass
