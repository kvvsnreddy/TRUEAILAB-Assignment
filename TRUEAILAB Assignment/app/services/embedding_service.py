import os
import google.generativeai as genai
from dotenv import load_dotenv
from app.utils.logger import logger

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class EmbeddingService:
    @staticmethod
    def get_embedding(text: str) -> list[float]:
        try:
            response = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="retrieval_document"
            )
            return response['embedding']
        except Exception as e:
            logger.error(f"Embedding generation failed: {str(e)}")
            raise e