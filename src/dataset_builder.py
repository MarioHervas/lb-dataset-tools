from src.zip_extractor import ZipExtractor, LetterboxdData
from src.tmdb_client import TMDBClient
import pandas as pd
from pathlib import Path
class DatasetConstructor:
    def __init__(self, user_data: list[LetterboxdData],tmdb_client:TMDBClient):
        self.user_data = user_data
        self.tmdb_client = tmdb_client
    def build(self, output_path: Path) -> None:
        output_path = Path(output_path) #TODO - Look into not making two times Path conversion but await incase script throws string
        output_path.mkdir(parents=True, exist_ok = True)
        movies = self._build_movies()
        interactions = self._build_interactions()

        movies.to_csv(output_path / "movies.csv", index = False)
        interactions.to_csv(output_path / "interactions.csv", index = False)
    def _build_movies(self) -> pd.DataFrame:
        all_movies = pd.concat(
            [user.ratings[["Name","Year","Letterboxd URI"]] for user in self.user_data], ignore_index = True).drop_duplicates(subset=["Name","Year"]
        )
        rows = []
        for movie in all_movies.iterrows():
            tmdb_id = self.tmdb_client.get_tmdb_id(movie["Name"],movie["Year"])
            details = self.tmdb_client.get_movie_request(tmdb_id)
            details["tmdb_id"] = tmdb_id
            details["name"] = movie["Name"]
            details["letterboxd_uri"] = movie["Letterboxd URI"]
            rows.append(details)

        return pd.DataFrame(rows)
    def _build_interactions(self) -> pd.DataFrame:
        frames = []
        for user in self.user_data:
            df = user.ratings[["Name","Year","Rating","Date"]].copy()
            df["username"]=user.username
            frames.append(df)
        return pd.concat(frames,ignore_index=True)
