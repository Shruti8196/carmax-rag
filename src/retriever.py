import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pathlib import Path
from src.data_loader import load_faq_data
from src.embedder import embed_questions

class FAQRetriever:
    def __init__(self, faq_path="data/faqs.json", embedding_path="data/faq_embeddings.npy", model_name="all-MiniLM-L6-v2"):
        self.faqs = load_faq_data(faq_path)
        self.embeddings = np.load(embedding_path)
        self.model = SentenceTransformer(model_name)
        self.index = self._build_faiss_index(self.embeddings)

    def _build_faiss_index(self, embeddings):
        dim = embeddings.shape[1]
        index = faiss.IndexFlatIP(dim)  # Inner Product for cosine similarity (vectors should be normalized)
        faiss.normalize_L2(embeddings)
        index.add(embeddings)
        return index

    def retrieve(self, query, top_k=5):
        query_vec = self.model.encode([query])
        faiss.normalize_L2(query_vec)
        distances, indices = self.index.search(query_vec, top_k)
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            faq = self.faqs[idx]
            faq["score"] = float(dist)
            results.append(faq)
        return results

if __name__ == "__main__":
    retriever = FAQRetriever()
    query = "Can you give me some information about Skye?"
    results = retriever.retrieve(query)
    for r in results:
        print(f"Score: {r['score']:.4f} | Q: {r['question']} | A: {r['answer']}\n")
