from abc import ABC, abstractmethod


class WebScraper(ABC):
    @abstractmethod
    def scrape_page(self) -> bool:
        pass

    @abstractmethod
    def scrape_all(self) -> None:
        pass

    @abstractmethod
    def get_page_content(self) -> bytes:
        pass

    @abstractmethod
    def write_to_json(self) -> None:
        pass
