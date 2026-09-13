from openai import OpenAI
from app.ai.base import AIProvider
from app.config import Settings

class OpenAIProvider(AIProvider):
    def __init__(self, settings: Settings):
        self.settings = settings
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is not configured. Add it to your .env file.")
        self.client = OpenAI(api_key=settings.openai_api_key)

    def generate(self, prompt: str) -> str:
        response = self.client.responses.create(
            model=self.settings.openai_model,
            input=prompt,
        )
        return response.output_text
