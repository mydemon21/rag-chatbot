import faiss
import numpy as np
import pickle
import os

class FAISSStore:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.texts = []
        self.metadata = []
        
    def add_texts(self, texts: list, embeddings: list, metadata: list = None):
        embeddings_array = np.array(embeddings).astype('float32')
        faiss.normalize_L2(embeddings_array)
        self.index.add(embeddings_array)
        self.texts.extend(texts)
        if metadata:
            self.metadata.extend(metadata)
        else:
            self.metadata.extend([{}] * len(texts))
    
    def search(self, query_embedding: list, top_k: int = 5):
        query_array = np.array([query_embedding]).astype('float32')
        faiss.normalize_L2(query_array)
        scores, indices = self.index.search(query_array, top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1:
                results.append({
                    'text': self.texts[idx],
                    'score': float(scores[0][i]),
                    'metadata': self.metadata[idx]
                })
        return results
    
    def save(self, path: str):
        faiss.write_index(self.index, f"{path}.index")
        with open(f"{path}.pkl", 'wb') as f:
            pickle.dump({'texts': self.texts, 'metadata': self.metadata}, f)
    
    def load(self, path: str):
        if os.path.exists(f"{path}.index"):
            self.index = faiss.read_index(f"{path}.index")
            with open(f"{path}.pkl", 'rb') as f:
                data = pickle.load(f)
                self.texts = data['texts']
                self.metadata = data['metadata']