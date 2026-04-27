import requests
from bs4 import BeautifulSoup
import cloudscraper

class NanogenreScraper:

    def __init__(self):
        self.scraper = cloudscraper.create_scraper()

    def scrape(self, letterboxd_uri: str) -> list[str]:
        return self._get_nanogenres(url=self._get_url(letterboxd_uri))

    def _get_url(self, letterboxd_uri: str) -> str:
        response = requests.get(letterboxd_uri)
        return f"{response.url}nanogenres"

    def _get_nanogenres(self, url: str) -> list[str]:
        response = self.scraper.get(url, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        nanogenres = []
        for a in soup.select('a[href*="/films/nanogenre/"]'):
            label = a.select_one("span.label")
            if label:
                text = label.get_text(strip=True)
                if text and text not in nanogenres:
                    nanogenres.append(text)

        return nanogenres[:10]