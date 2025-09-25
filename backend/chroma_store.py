import chromadb
from chromadb.config import Settings
import uuid

class ChromaStore:
    def __init__(self, collection_name: str = "rag_collection"):
        self.client = chromadb.Client(Settings(anonymized_telemetry=False))
        self.collection = self.client.get_or_create_collection(collection_name)
    
    def add_texts(self, texts: list, embeddings: list, metadata: list = None):
        ids = [str(uuid.uuid4()) for _ in texts]
        if not metadata:
            metadata = [{}] * len(texts)
        
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadata,
            ids=ids
        )
    
    def search(self, query_embedding: list, top_k: int = 5):
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        formatted_results = []
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                'text': results['documents'][0][i],
                'score': 1 - results['distances'][0][i],  # Convert distance to similarity
                'metadata': results['metadatas'][0][i]
            })
        return formatted_results