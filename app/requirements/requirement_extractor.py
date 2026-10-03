from typing import List

from app.jobs.models import JobPost


# Known technical and professional requirements that the
# deterministic extractor can recognize.
KNOWN_REQUIREMENTS = [
    "Python",
    "Django",
    "PHP",
    "Laravel",
    "WordPress",
    "Flutter",
    "AWS",
    "Oracle Cloud",
    "Linux",
    "PostgreSQL",
    "MySQL",
    "Docker",
    "Kubernetes",
    "REST API",
    "GraphQL",
    "JavaScript",
    "TypeScript",
    "React",
    "Vue.js",
    "Node.js",
    "E-commerce",
    "Git",
    "GitHub",
]


def normalize(value: str) -> str:
    """Normalize text for deterministic comparison."""
    return value.strip().lower()


def requirement_in_text(
    requirement: str,
    text: str,
) -> bool:
    """Return True when a requirement appears in the supplied text."""
    return normalize(requirement) in normalize(text)


def extract_requirements(job: JobPost) -> List[str]:
    """
    Extract known requirements from a job's explicit skills,
    title, and description.

    Requirements are returned once and preserve the order in which
    they appear in the known requirement list.
    """

    searchable_text = " ".join(
        [
            job.title,
            job.description,
            *job.skills,
        ]
    )

    requirements: List[str] = []

    # Explicit job skills are always requirements.
    for skill in job.skills:
        if skill and skill not in requirements:
            requirements.append(skill)

    # Detect additional known requirements from the job text.
    for requirement in KNOWN_REQUIREMENTS:
        if requirement in requirements:
            continue

        if requirement_in_text(requirement, searchable_text):
            requirements.append(requirement)

    return requirements