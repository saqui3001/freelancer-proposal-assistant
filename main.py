from app.ai.factory import AIProviderFactory
from app.config import get_settings
from app.prompts.proposal_prompt import build_proposal_prompt


def main() -> None:
    settings = get_settings()

    print("Freelancer Proposal Assistant")
    print("Phase 1B - Proposal Prompt Test")
    print("-" * 40)
    print(f"Selected provider: {settings.ai_provider}")

    if settings.ai_provider.lower() == "anthropic":
        print(f"Selected model: {settings.anthropic_model}")
    else:
        print(f"Selected model: {settings.openai_model}")

    # Sample job used only to test the proposal-generation pipeline.
    job_title = "Python Django Developer Needed for E-commerce Website"

    job_description = """
We are looking for an experienced Python/Django developer to help
improve an existing e-commerce website. The developer should have
experience with Django, REST APIs, databases, and integrating
third-party services. Experience with AWS is a plus.
""".strip()

    prompt = build_proposal_prompt(
        job_title=job_title,
        job_description=job_description,
    )

    print("\nSending proposal request to AI provider...")

    try:
        provider = AIProviderFactory.create(settings)
        proposal = provider.generate(prompt)

        print("\nGenerated proposal:")
        print("-" * 40)
        print(proposal)
        print("-" * 40)

    except Exception as exc:
        print("\nERROR:")
        print(type(exc).__name__)
        print(str(exc))


if __name__ == "__main__":
    main()