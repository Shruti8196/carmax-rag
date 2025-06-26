import json
from pathlib import Path

def load_faq_data(file_path: str):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"{file_path} not found.")

    with open(file_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    cleaned = []
    for entry in raw_data:
        question = entry.get("question", "").strip()   # changed from "question" to "title"
        answer = entry.get("answer", "").strip()
        if question and answer:
            cleaned.append({
                "question": question,
                "answer": answer,
                "topic": entry.get("topic", "General"),
                "source": entry.get("source", "Unknown"),
                "created_at": entry.get("created_at", None)
            })
    return cleaned
