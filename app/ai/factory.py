from app.ai.anthropic_provider import AnthropicProvider
from app.ai.base import AIProvider
from app.ai.openai_provider import OpenAIProvider
from app.config import Settings

class AIProviderFactory:
    @staticmethod
    def create(settings: Settings) -> AIProvider:
        provider_name = settings.ai_provider.lower().strip()
        if provider_name == "anthropic":
            return AnthropicProvider(settings)
        if provider_name == "openai":
            return OpenAIProvider(settings)
        raise ValueError(
            f"Unsupported AI provider: {provider_name!r}. "
            "Currently supported: anthropic, openai"
        )
