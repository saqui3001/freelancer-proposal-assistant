
from app.jobs.models import JobPost
from app.requirements.priority import RequirementPriority
from app.requirements.requirement_extractor import extract_requirements


def test_extract_requirements_and_default_priority():
    job = JobPost(
        platform="upwork",
        title="Senior Python Django Developer for E-commerce Platform",
        description=(
            "We need an experienced developer to improve our Django "
            "e-commerce application using Python, PostgreSQL and AWS. "
            "Docker experience is preferred."
        ),
        skills=["Python", "Django"],
    )

    requirements = extract_requirements(job)

    requirement_names = [requirement.name for requirement in requirements]

    assert requirement_names == [
        "Python",
        "Django",
        "AWS",
        "PostgreSQL",
        "Docker",
        "E-commerce",
    ]

    assert all(
        requirement.priority == RequirementPriority.UNKNOWN
        for requirement in requirements
    )