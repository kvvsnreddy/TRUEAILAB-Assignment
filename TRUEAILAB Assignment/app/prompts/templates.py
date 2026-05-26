RAG_PROMPT_TEMPLATE = """You are a helpful assistant.

Use ONLY the provided context to answer the question. If you do not know the answer or if it's not found in the context, explicitly state that you cannot find enough information.

Context:
{retrieved_context}

Conversation History:
{history}

Question:
{user_question}

Answer:"""