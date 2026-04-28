import os
from pathlib import Path
from pathlib import Path
from dotenv import load_dotenv
import os

from src.zip_extractor import ZipExtractor
from src.preprocessor import preprocess
from src.tmdb_client import TMDBClient
from src.nanogenre_scraper import NanogenreScraper
from src.movie_store import MovieStore
from src.dataset_builder import DatasetConstructor
from dotenv import load_dotenv
import requests

from src.zip_extractor import ZipExtractor
from src.preprocessor import preprocess
from src.tmdb_client import TMDBClient
from src.nanogenre_scraper import NanogenreScraper
from src.dataset_builder import DatasetConstructor


load_dotenv()

extractor = ZipExtractor()
data = []
data.append(extractor.extract(Path("zips/letterboxd-mariohervas-2026-03-04-17-51-utc.zip")))
data.append(extractor.extract(Path("zips/letterboxd-withloveclau-2026-02-28-12-46-utc.zip")))

for d in data:
    preprocess(d)

client = TMDBClient(api_key=os.getenv("TMDB_API_KEY"))
scraper = NanogenreScraper()
store = MovieStore("movie_store.json")

dataset = DatasetConstructor(data, client, scraper, store)
dataset.build("testdata")


