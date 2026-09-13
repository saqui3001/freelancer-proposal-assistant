from anthropic import Anthropic
from app.ai.base import AIProvider
from app.config import Settings

class AnthropicProvider(AIProvider):
    def __init__(self, settings: Settings):
        self.settings = settings
        if not settings.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is not configured. Add it to your .env file.")
        self.client = Anthropic(api_key=settings.anthropic_api_key)

    def generate(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=self.settings.anthropic_model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return "\n".join(
            block.text for block in response.content if block.type == "text"
        )
