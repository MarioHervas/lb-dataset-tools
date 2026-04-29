

from src.movie_store import MovieStore


class BertopicEnricher:

    def __init__(self, movie_store: MovieStore):
        self.movie_store = movie_store

    def enrich(self) -> None :
        pass

    def _extract_overviews(self) -> tuple[list[str],list[str]]:
        titles = []
        docs = []
        for title, data in self.movie_store.store.items():
            overview = data.get("overview", "").strip()
            if overview:
                titles.append(title)
                docs.append(overview)
        return titles, docs
