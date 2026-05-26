import os
import google.generativeai as genai
from dotenv import load_dotenv
from app.prompts.templates import RAG_PROMPT_TEMPLATE
from app.utils.logger import logger

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class LLMService:
    @staticmethod
    def generate_response(context: str, history: str, question: str) -> str:
        prompt = RAG_PROMPT_TEMPLATE.format(
            retrieved_context=context,
            history=history,
            user_question=question
        )
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.2, # Grounded responses
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"LLM generation failed: {str(e)}")
            raise e