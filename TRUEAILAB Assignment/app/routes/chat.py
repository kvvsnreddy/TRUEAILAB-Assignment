from fastapi import APIRouter, HTTPException, status
from app.models.schemas import ChatRequest, ChatResponse
from app.vectorstore.database import init_vector_store
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.utils.logger import logger

router = APIRouter(prefix="/api")

# Session management for local short term chat history
# Stores up to last 5 message turns per session ID
chat_histories: dict[str, list[dict]] = {}

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest):
    try:
        store = init_vector_store()
        
        # 1. Generate query embedding
        query_embedding = EmbeddingService.get_embedding(payload.message)
        
        # 2. Similarity Search
        search_results = store.similarity_search(query_embedding, k=3, threshold=0.70)
        
        # 3. Grounding evaluation
        if not search_results:
            return ChatResponse(
                reply="I could not find enough information in the knowledge base to answer this question.",
                tokensUsed=0,
                retrievedChunks=0
            )
            
        # 4. Compile context
        context_str = "\n\n".join([f"Source: {res['chunk']['title']}\nContent: {res['chunk']['content']}" for res in search_results])
        
        # 5. Extract Session History
        if payload.sessionId not in chat_histories:
            chat_histories[payload.sessionId] = []
            
        history_list = chat_histories[payload.sessionId][-5:] # Last 5 items max
        history_str = "\n".join([f"{h['role'].capitalize()}: {h['text']}" for h in history_list])
        
        # 6. Call LLM
        reply = LLMService.generate_response(context=context_str, history=history_str, question=payload.message)
        
        # 7. Update conversation logs
        chat_histories[payload.sessionId].append({"role": "user", "text": payload.message})
        chat_histories[payload.sessionId].append({"role": "assistant", "text": reply})
        
        return ChatResponse(
            reply=reply,
            tokensUsed=len(reply.split()) + len(context_str.split()), # Rough estimation proxy
            retrievedChunks=len(search_results)
        )
        
    except Exception as e:
        logger.error(f"Global server route error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error: {str(e)}"
        )