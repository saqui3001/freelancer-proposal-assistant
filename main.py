from app.ai.factory import AIProviderFactory
from app.config import get_settings

def main() -> None:
    settings = get_settings()
    print("Freelancer Proposal Assistant")
    print("Phase 1 - AI Provider Framework")
    print("-" * 40)
    print(f"Selected provider: {settings.ai_provider}")

    if settings.ai_provider.lower() == "anthropic":
        print(f"Selected model: {settings.anthropic_model}")
    else:
        print(f"Selected model: {settings.openai_model}")

    try:
        provider = AIProviderFactory.create(settings)
        response = provider.generate(
            "Reply with exactly: AI Provider Framework connection successful."
        )
        print("\nAPI response:")
        print(response)
    except Exception as exc:
        print("\nERROR:")
        print(type(exc).__name__)
        print(str(exc))

if __name__ == "__main__":
    main()
