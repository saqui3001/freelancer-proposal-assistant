from dataclasses import dataclass
from typing import List

from app.jobs.models import JobPost
from app.requirements.priority import RequirementPriority


@dataclass
class ExtractedRequirement:
    name: str
    priority: RequirementPriority = RequirementPriority.UNKNOWN


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


def extract_requirements(job: JobPost) -> List[ExtractedRequirement]:
    """
    Extract known requirements from a job's explicit skills,
    title, and description.

    Priority remains UNKNOWN unless it is explicitly available
    from the job data. This version deliberately does not guess
    whether a requirement is mandatory or preferred.
    """

    searchable_text = " ".join(
        [
            job.title,
            job.description,
            *job.skills,
        ]
    )

    requirements: List[ExtractedRequirement] = []
    requirement_names = set()

    # Explicit job skills are requirements, but their priority
    # is unknown unless the JobPost model provides that information.
    for skill in job.skills:
        if not skill:
            continue

        normalized_skill = normalize(skill)

        if normalized_skill in requirement_names:
            continue

        requirements.append(
            ExtractedRequirement(
                name=skill,
                priority=RequirementPriority.UNKNOWN,
            )
        )

        requirement_names.add(normalized_skill)

    # Detect additional known requirements from the job text.
    for requirement in KNOWN_REQUIREMENTS:
        normalized_requirement = normalize(requirement)

        if normalized_requirement in requirement_names:
            continue

        if requirement_in_text(requirement, searchable_text):
            requirements.append(
                ExtractedRequirement(
                    name=requirement,
                    priority=RequirementPriority.UNKNOWN,
                )
            )

            requirement_names.add(normalized_requirement)

    return requirements