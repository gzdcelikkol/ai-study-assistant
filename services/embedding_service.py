# metinlerin vektöre çevrilmesi

from sentence_transformers import SentenceTransformer
from core.config import embedding_model_name

model = SentenceTransformer(EMBEDDING_MODEL_NAME)

def get_embedding(text: str) -> list[float]:
    return model.encode(text).tolist()

def get_embeddings_batch(texts: list[str]) -> list[list[float]]:
    # Toplu dönüştürme tek tek yapmaktan çok daha hızlıdır
    return model.encode(texts).tolist()
