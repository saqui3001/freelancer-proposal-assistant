
from app.jobs.models import JobPost
from app.requirements.priority import RequirementPriority
from app.requirements.requirement_extractor import extract_requirements


def get_priorities(job: JobPost) -> dict[str, RequirementPriority]:
    return {
        requirement.name: requirement.priority
        for requirement in extract_requirements(job)
    }


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

    assert [requirement.name for requirement in requirements] == [
        "Python",
        "Django",
        "AWS",
        "PostgreSQL",
        "Docker",
        "E-commerce",
    ]

    priorities = {
        requirement.name: requirement.priority
        for requirement in requirements
    }

    assert priorities["Docker"] == RequirementPriority.PREFERRED
    assert priorities["Python"] == RequirementPriority.UNKNOWN
    assert priorities["Django"] == RequirementPriority.UNKNOWN
    assert priorities["AWS"] == RequirementPriority.UNKNOWN
    assert priorities["PostgreSQL"] == RequirementPriority.UNKNOWN
    assert priorities["E-commerce"] == RequirementPriority.UNKNOWN


def test_detects_explicitly_required_requirements():
    job = JobPost(
        platform="upwork",
        title="Python Developer",
        description=(
            "Python is required. Must have Django experience. "
            "AWS knowledge is essential."
        ),
        skills=[],
    )

    priorities = get_priorities(job)

    assert priorities["Python"] == RequirementPriority.REQUIRED
    assert priorities["Django"] == RequirementPriority.REQUIRED
    assert priorities["AWS"] == RequirementPriority.REQUIRED


def test_detects_explicitly_preferred_requirements():
    job = JobPost(
        platform="upwork",
        title="Backend Developer",
        description=(
            "Docker experience is preferred. "
            "Kubernetes knowledge would be a plus."
        ),
        skills=[],
    )

    priorities = get_priorities(job)

    assert priorities["Docker"] == RequirementPriority.PREFERRED
    assert priorities["Kubernetes"] == RequirementPriority.PREFERRED


def test_priority_is_assigned_to_the_correct_requirement():
    job = JobPost(
        platform="upwork",
        title="Python and Docker Developer",
        description=(
            "Python is required. Docker experience is a plus."
        ),
        skills=[],
    )

    priorities = get_priorities(job)

    assert priorities["Python"] == RequirementPriority.REQUIRED
    assert priorities["Docker"] == RequirementPriority.PREFERRED


def test_conflicting_priority_evidence_remains_unknown():
    job = JobPost(
        platform="upwork",
        title="Python Developer",
        description=(
            "Python is required. Python experience is preferred."
        ),
        skills=[],
    )

    priorities = get_priorities(job)

    assert priorities["Python"] == RequirementPriority.UNKNOWN


def test_git_does_not_match_github_as_the_same_requirement():
    job = JobPost(
        platform="upwork",
        title="GitHub integration developer",
        description="Experience with GitHub is required.",
        skills=[],
    )

    priorities = get_priorities(job)

    assert priorities["GitHub"] == RequirementPriority.REQUIRED
    assert "Git" not in priorities
