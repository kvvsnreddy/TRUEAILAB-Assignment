from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    sessionId: str = Field(..., example="abc123")
    message: str = Field(..., example="How can I reset my password?")

class ChatResponse(BaseModel):
    reply: str
    tokensUsed: int
    retrievedChunks: int