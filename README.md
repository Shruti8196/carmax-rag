1. User Query Input
   A customer submits a question via the chatbot interface (e.g., "Can I return my car if I change my mind?").

2. Query Decomposition
   The input query is broken into focused subquestions to better understand and capture granular intent. eg. "What is the return policy?", "Are there any time limits for returns?"

3. FAQ Matching
   Each subquestion is semantically matched to the most relevant FAQ entries using vector similarity search. Embeddings are pre-computed and stored in a vector database.

4. Context Construction
   Retrieved FAQ answers are combined and appended to the original user query to form a rich context.

5. Answer Generation
   A language model (e.g., GPT-4 or Claude) generates a final response grounded in the retrieved context.

![image](https://github.com/user-attachments/assets/8d3f4d8f-3309-4f75-ae14-6c89e4fdc6b3)
