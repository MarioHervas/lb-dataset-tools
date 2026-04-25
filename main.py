import os
from pathlib import Path

from dotenv import load_dotenv

from src.zip_extractor import ZipExtractor
from src.preprocessor import preprocces
from src.tmdb_client import TMDBClient

load_dotenv()
api_key = os.getenv("TMDB_API_KEY")
print(api_key)

from src.tmdb_client import TMDBClient

client = TMDBClient(api_key)
print(client.get_tmdb_id("L’Eclisse", 1962))

# extractor = ZipExtractor()
# data = extractor.extract(Path("zips/letterboxd-mariohervas-2026-03-04-17-51-utc.zip"))
#
# preprocces(data)
# print(f'movies: {data.ratings["Name"]} ratings:{data.ratings["Rating"]}')