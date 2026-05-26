from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes import chat
from app.vectorstore.database import init_vector_store

app = FastAPI(title="Production-Grade GenAI Assistant with RAG")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize vector db synchronously on bootup
@app.on_event("startup")
async def startup_event():
    init_vector_store()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

app.include_router(chat.router)

# Serve Frontend SPA
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")