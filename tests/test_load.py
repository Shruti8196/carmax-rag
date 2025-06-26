from src.data_loader import load_faq_data

faq_list = load_faq_data("data/faqs.json")
for faq in faq_list[:3]:
    print(f"Q: {faq['question']}")
    print(f"A: {faq['answer']}")
    print(f"Topic: {faq['topic']}\n")