import os
from pathlib import Path

from dotenv import load_dotenv
import requests

from src.zip_extractor import ZipExtractor
from src.preprocessor import preprocces
from src.tmdb_client import TMDBClient
from src.nanogenre_scraper import NanogenreScraper

load_dotenv()
api_key = os.getenv("TMDB_API_KEY")
print(api_key)

from src.tmdb_client import TMDBClient

scraper = NanogenreScraper()
nano = scraper.scrape("https://boxd.it/hYC8/")
print(nano)
response = requests.get("https://boxd.it/hYC8/")
print(f"{response.url}nanogenres")

#
# client = TMDBClient(api_key)
# print(client.get_tmdb_id("Mulholland Drive",2001))
# print(client.get_info("Mulholland Drive",2001))
#
# extractor = ZipExtractor()
# data = extractor.extract(Path("zips/letterboxd-mariohervas-2026-03-04-17-51-utc.zip"))
# print(data.ratings)
# preprocces(data)
# print(data.ratings)
