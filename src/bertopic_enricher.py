from sentence_transformers import SentenceTransformer
from bertopic import BERTopic
from src.movie_store import MovieStore
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from bertopic.vectorizers import ClassTfidfTransformer
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
        topics, _ = topic_model.fit_transform(docs)

        # DEBUG — pegar aquí
        from sentence_transformers import SentenceTransformer
        import numpy as np
        from sklearn.metrics.pairwise import cosine_similarity

        sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = sentence_model.encode(docs[:100], show_progress_bar=False)
        sample = embeddings[:50]
        sim_matrix = cosine_similarity(sample)
        np.fill_diagonal(sim_matrix, 0)
        print(f"Similitud coseno media: {sim_matrix.mean():.3f}")
        print(f"Similitud coseno máxima: {sim_matrix.max():.3f}")
        print(f"Similitud coseno mínima: {sim_matrix.min():.3f}")
        # FIN DEBUG

        from collections import Counter
        print(Counter(topics))

        from collections import defaultdict
        topic_movies = defaultdict(list)
        for i, title in enumerate(titles):
            topic_movies[topics[i]].append(title)

        for topic_id in sorted(topic_movies.keys()):
            words = [word for word, _ in topic_model.get_topic(topic_id)]
            keywords = "|".join(words[:5])
            sample = topic_movies[topic_id][:5]
            print(f"\nTópico {topic_id} [{keywords}]:")
            for movie in sample:
                print(f"  - {movie}")

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

    def _build_model(self) -> BERTopic:
        sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
        umap_model = UMAP(n_neighbors=15, n_components=5, random_state=42)
        cluster_model = KMeans(n_clusters=20, random_state=42)
        vectorizer = CountVectorizer(stop_words="english")

        return BERTopic(
            embedding_model=sentence_model,
            umap_model=umap_model,
            hdbscan_model=cluster_model,
            vectorizer_model=vectorizer,
        )

    def _update_store(self, titles: list[str], topics: list[int], topic_model: BERTopic):
        for i, title in enumerate(titles):
            topic_id = topics[i]
            if topic_id == -1:
                themes = ""
            else:
                words = [word for word, _ in topic_model.get_topic(topic_id)]
                themes = "|".join(words[:5])
            self.movie_store.update_themes(title, themes)
