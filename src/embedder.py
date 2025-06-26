from sentence_transformers import SentenceTransformer
import numpy as np
import json
from pathlib import Path

def embed_questions(faq_list, model_name="all-MiniLM-L6-v2"):
    """
    Generate embeddings for a list of FAQ questions.
    
    Args:
        faq_list: List of dicts with at least the "question" key.
        model_name: Pretrained SentenceTransformer model to use.
        
    Returns:
        embeddings: np.ndarray of shape (num_questions, embedding_dim)
    """
    model = SentenceTransformer(model_name)
    questions = [faq["question"] for faq in faq_list]
    embeddings = model.encode(questions, show_progress_bar=True)
    return embeddings

def save_embeddings(embeddings, save_path="data/faq_embeddings.npy"):
    np.save(save_path, embeddings)
    print(f"Saved embeddings to {save_path}")

def load_embeddings(path="data/faq_embeddings.npy"):
    path = Path(path)
    if path.exists():
        return np.load(path)
    else:
        raise FileNotFoundError(f"Embedding file not found: {path}")

if __name__ == "__main__":
    from src.data_loader import load_faq_data

    faqs = load_faq_data("data/faqs.json")
    embeddings = embed_questions(faqs)
    save_embeddings(embeddings)
