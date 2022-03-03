from bs4 import BeautifulSoup
from BaseClasses.BaseScraper import WebScraper

import datetime
import requests
import json


class WeatherScraper(WebScraper):
    def __init__(self, url: str) -> None:
        super().__init__()
        self.url = url
        self._cache = {}

    def scrape_page(self) -> bool:
        """
            Send HTTP Request to url and receive HTML

            Returns True if successful
        """
        try:
            self.page = requests.get(self.url)

            self.soup = BeautifulSoup(self.page.content, 'html.parser')

            return True
        except:
            return False

    def scrape_all(self) -> None:
        """
            Chain every fetch together to fill self._cache
        """
        self.get_location()
        self.get_temperature()
        self.get_condition()

    def get_page_content(self) -> bytes:
        return self.page.content

    def get_location(self) -> str:
        if "Location" in self._cache:
            return self._cache["Location"]

        result = self.soup.find("h1", attrs={
            'class': 'CurrentConditions--location--kyTeL'}).text

        self._cache["Location"] = result

        return result

    def get_temperature(self) -> str:
        if "Temperature" in self._cache:
            return self._cache["Temperature"]

        result = self.soup.find("span", attrs={
            'class': 'CurrentConditions--tempValue--3a50n', 'data-testid': 'TemperatureValue'}).text

        self._cache["Temperature"] = result

        return result

    def get_condition(self) -> str:
        if "Condition" in self._cache:
            return self._cache["Condition"]

        result = self.soup.find("div", attrs={
            'class': 'CurrentConditions--phraseValue--2Z18W', 'data-testid': 'wxPhrase'}).text

        self._cache["Condition"] = result

        return result

    def write_to_json(self) -> None:
        """
            Write JSON Object from data in self._cache
        """

        timestamp = datetime.datetime.now()
        timestamp = f"{timestamp.day}-{timestamp.month}-{timestamp.year} {timestamp.hour}-{timestamp.minute}"

        with open(f"Scraped_Files/{self.get_location()} {timestamp}.json", "w", encoding="utf-8") as file:
            json.dump(self._cache, file)
