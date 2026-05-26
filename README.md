# Production-Grade GenAI Assistant with RAG

This is a complete implementation of a Retrieval-Augmented Generation chatbot engineered via FastAPI and Gemini AI.

## RAG Architecture Workflow
1. **Document Ingestion**: On boot up, documents are loaded out of `docs.json`, text-chunked, embedded via Gemini's `embedding-001` model, and indexed in-memory.
2. **Retrieval Engine**: When querying, user messages are processed into embeddings. Sklearn's mathematical libraries calculate the cosine similarity metric across all vectors.
3. **Thresholding & Guardrails**: If matching vectors hit values $< 0.70$, a safe grounding response is returned natively without generating LLM calls.
4. **Context Provision & Execution**: Valid matches build a structured injection system tracking standard dynamic user request prompts bundled with active short-term memory history records.

## Local Configuration and Deployment

Install requirements:
   bash
   pip install -r requirements.txt
Setup your system parameters inside an active environmental variable file:

Bash
cp .env.example .env
Run the deployment instance locally:

Bash
uvicorn app.main:app --reload --port 8000
