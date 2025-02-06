import faiss
import numpy as np

class FaissIndex:
    def __init__(self, embeddings_file: str, num_cells: int = 50):
        self.embeddings_file = embeddings_file
        self.num_cells = num_cells
        self.index = self._create_faiss_index()

    def _create_faiss_index(self):
        data = np.load(self.embeddings_file)
        embeddings = data["embeddings"]
        emb_dim = embeddings.shape[1]

        quantizer = faiss.IndexFlatL2(emb_dim)
        index = faiss.IndexIVFFlat(quantizer, emb_dim, self.num_cells)
        index.train(embeddings)
        index.add(embeddings)
        
        return index

    def search(self, query_embedding, top_k=5):
        D, I = self.index.search(query_embedding, top_k)
        return I
