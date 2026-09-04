# vektör veritabanı
import chromadb
from core.config import chroma_path

chroma_client = chromadb.PersistentClient(path=chroma_path)
collection = chroma_client.get_or_create_collection(name="study_notes")


def save_chunks_to_db(filename: str, chunks: list[str], embeddings: list[list[float]]):
    ids = []
    metadatas = []

    for i in range(len(chunks)):
        ids.append(f"{filename}_chunk_{i}")
        metadatas.append({"source": filename, "chunk_index": i})

    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas
    )


def search_relevant_chunks(query_embedding: list[float], top_k: int = 3) -> list[str]:
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results["documents"][0] if results["documents"] else []