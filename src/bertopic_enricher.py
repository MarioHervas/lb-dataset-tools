from sentence_transformers import SentenceTransformer
from bertopic import BERTopic
from src.movie_store import MovieStore
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
class BertopicEnricher:

    def __init__(self, movie_store: MovieStore):
        self.movie_store = movie_store

    def enrich(self) -> None:
        titles, docs = self._extract_overviews()

        if len(docs) < 10:
            print("[BERTopic] No hay suficientes sinopsis para entrenar el modelo.")
            return

        print(f"[BERTopic] Entrenando sobre {len(docs)} sinopsis...")
        topic_model = self._build_model()
        topics, _   = topic_model.fit_transform(docs)

        self._update_store(titles, topics, topic_model)
        self.movie_store._save()

        n_topics = len(set(t for t in topics if t != -1))
        n_outliers = sum(1 for t in topics if t == -1)
        print(f"[BERTopic] Hecho. {n_topics} tópicos encontrados, {n_outliers} outliers.")

    def _extract_overviews(self) -> tuple[list[str],list[str]]:
        titles = []
        docs = []
        for title, data in self.movie_store.store.items():
            overview = data.get("overview", "").strip()
            if overview:
                titles.append(title)
                docs.append(overview)
        return titles, docs

    def _build_model(self)-> BERTopic:
        sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
        umap_model = UMAP(n_neighbors=10, n_components=5, random_state=42)
        hdbscan_model = HDBSCAN(min_cluster_size=5, prediction_data=True)
        vectorizer = CountVectorizer(stop_words="english")

        return BERTopic(
            embedding_model=sentence_model,
            umap_model=umap_model,
            hdbscan_model=hdbscan_model,
            vectorizer_model=vectorizer,
        )
    def _update_store(self, titles: list[str],topics: list[int], topic_model: BERTopic):
        for i, title in enumerate(titles):
            topic_id = topics[i]
            words = [word for word, _ in topic_model.get_topic(topic_id)]
            themes = "|".join(words[:5])
            print(f"{title} {themes} ")
