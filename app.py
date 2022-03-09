from ScraperClasses.HTMLParserClass import HTMLParser
from ScraperClasses.WebSpider import WebSpider
from pathlib import Path

import config
import os


def main() -> None:
    # Get List of HTML files in 'HTMLs' directory
    file_list = list(
        Path(config.APP_FOLDER / config._config["HTML_input_path"]).glob("*.html"))

    config.logger.info(f"Found {len(file_list)} HTML files")

    index = 1

    for file in file_list:
        # Create an HTMLParser for every file found
        html_parser = HTMLParser(os.path.basename(file))

        config.logger.info("Parsing File " + str(index) +
                           "/" + str(len(file_list)))

        index += 1

        # Chain the 3 methods necessary to build and write the output HTML
        chain(html_parser.scrape_page,
              html_parser.build_page,
              html_parser.write_to_html
              )

    #ws = WebSpider("https://www.w3schools.com/python/", domain="same")
    # ws.get_html()


def chain(*args) -> None:
    """
        Chain functions together to be called in order
    """
    for arg in args:
        arg()


if __name__ == "__main__":
    main()
