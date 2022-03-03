from ScraperClasses.WeatherScraperClass import WeatherScraper
from ScraperClasses.HTMLParserClass import HTMLParser
from pathlib import Path
import json
import os

APP_FOLDER = Path(__file__).parent
os.chdir(APP_FOLDER)

with open("config.json", "r") as f:
    config = json.load(f)


def main() -> None:
    """ws = WeatherScraper(
        "https://weather.com/de-DE/wetter/heute/l/60b2003898aa2f2d8a5fff837187aa7adf9e4dbed6ff36aa45ccab7d618a2add")

    if ws.scrape_page():
        ws.scrape_all()
        ws.write_to_json()"""
    # TODO: Logger einbauen
    file_list = list(
        Path(APP_FOLDER / config["HTML_input_path"]).glob("*.html"))

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
