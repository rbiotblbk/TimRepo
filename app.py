from ScraperClasses.WeatherScraperClass import WeatherScraper
from ScraperClasses.HTMLParserClass import HTMLParser
from pathlib import Path
from logging.config import fileConfig
import logging
import json
import os

APP_FOLDER = Path(__file__).parent
os.chdir(APP_FOLDER)

with open("config.json", "r") as f:
    config = json.load(f)

fileConfig(config["logger_config"], disable_existing_loggers=False)

logger = logging.getLogger()


def main() -> None:
    file_list = list(
        Path(APP_FOLDER / config["HTML_input_path"]).glob("*.html"))

    logger.info(f"Found {len(file_list)} HTML files")

    for file in file_list:
        html_parser = HTMLParser(os.path.basename(file))

        chain(html_parser.scrape_page,
              html_parser.build_page,
              html_parser.write_to_html
              )


def chain(*args) -> None:
    for arg in args:
        arg()


if __name__ == "__main__":
    main()
