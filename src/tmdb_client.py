import requests
class TMDBClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_info(self,title: str, year : int) -> dict:
        pass

    def get_tmdb_id(self, title: str, year: int) -> int:
        response = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={self.api_key}&query={title}&year={year}")
        results = response.json()["results"]
        if results:
            return results[0]["id"]
        return None

    def get_movie_request(self,tmdb_id: int) -> dict:
        pass

