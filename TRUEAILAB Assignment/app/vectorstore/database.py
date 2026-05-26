import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from app.services.embedding_service import EmbeddingService
from app.utils.logger import logger

class VectorStore:
    def __init__(self, docs_path: str = "docs.json"):
        self.chunks = []
        self.embeddings = []
        self.load_and_index_documents(docs_path)

    def load_and_index_documents(self, docs_path: str):
        try:
            with open(docs_path, "r") as f:
                documents = json.load(f)
            
            chunk_id = 0
            for doc in documents:
                # Naive word-based chunker mimicking token chunking limits
                words = doc["content"].split()
                chunk_size = 100  # Words per chunk
                
                for i in range(0, len(words), chunk_size):
                    chunk_text = " ".join(words[i:i + chunk_size])
                    logger.info(f"Indexing chunk {chunk_id} for document: {doc['title']}")
                    
                    embedding = EmbeddingService.get_embedding(chunk_text)
                    
                    self.chunks.append({
                        "id": chunk_id,
                        "title": doc["title"],
                        "content": chunk_text,
                        "source": docs_path
                    })
                    self.embeddings.append(embedding)
                    chunk_id += 1
            
            self.embeddings = np.array(self.embeddings)
            logger.info("Successfully completed indexing.")
        except Exception as e:
            logger.error(f"Failed to initialize Vector Store: {str(e)}")

    def similarity_search(self, query_vector: list[float], k: int = 3, threshold: float = 0.70) -> list[dict]:
        if len(self.embeddings) == 0:
            return []
        
        query_arr = np.array([query_vector])
        scores = cosine_similarity(query_arr, self.embeddings)[0]
        
        ranked_indices = np.argsort(scores)[::-1]
        results = []
        
        for idx in ranked_indices:
            score = float(scores[idx])
            logger.info(f"Chunk ID {self.chunks[idx]['id']} Similarity Score: {score:.4f}")
            if score >= threshold:
                results.append({
                    "chunk": self.chunks[idx],
                    "score": score
                })
            if len(results) == k:
                break
                
        return results

# Initialize a global instance of VectorStore
vector_store = None

def init_vector_store():
    global vector_store
    if vector_store is None:
        vector_store = VectorStore()
    return vector_store