import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

class SimpleVectorStore:
    def __init__(self):
        self.embeddings = []
        self.texts = []
        self.metadata = []
    
    def add_texts(self, texts: list, embeddings: list, metadata: list = None):
        self.embeddings.extend(embeddings)
        self.texts.extend(texts)
        if metadata:
            self.metadata.extend(metadata)
        else:
            self.metadata.extend([{}] * len(texts))
    
    def search(self, query_embedding: list, top_k: int = 5):
        if not self.embeddings:
            return []
        
        similarities = cosine_similarity([query_embedding], self.embeddings)[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            results.append({
                'text': self.texts[idx],
                'score': float(similarities[idx]),
                'metadata': self.metadata[idx]
            })
        return results
    
    def save(self, path: str):
        data = {
            'embeddings': self.embeddings,
            'texts': self.texts,
            'metadata': self.metadata
        }
        with open(f"{path}.pkl", 'wb') as f:
            pickle.dump(data, f)
    
    def load(self, path: str):
        if os.path.exists(f"{path}.pkl"):
            with open(f"{path}.pkl", 'rb') as f:
                data = pickle.load(f)
                self.embeddings = data.get('embeddings', [])
                self.texts = data.get('texts', [])
                self.metadata = data.get('metadata', [])