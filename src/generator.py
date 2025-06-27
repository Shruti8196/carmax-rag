import os
import openai
from openai import OpenAI
from src.retriever import FAQRetriever

openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
def build_context(faqs):
    return "\n\n".join([f"Q: {f['question']}\nA: {f['answer']}" for f in faqs])

def generate_answer(query, faqs, model="gpt-4o-mini", temperature=0.2):
    context = build_context(faqs)
    
    system_prompt = (
        "You are Skye, a friendly and accurate AI assistant for CarMax. "
        "Use the provided FAQs as source of truth. "
        "If you’re unsure or the answer isn't in the FAQs, say 'I’m not sure'."
    )
    
    user_prompt = (
        f"Context:\n{context}\n\n"
        f"User question: {query}\n"
        f"Answer as Skye:"
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temperature
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    retriever = FAQRetriever()
    query = "How do I know if a car has a safety recall"
    faqs = retriever.retrieve(query)
    answer = generate_answer(query, faqs)
    print("\n🤖 Skye says:\n")
    print(answer)
