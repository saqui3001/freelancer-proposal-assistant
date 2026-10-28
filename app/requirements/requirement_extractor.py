import re
from dataclasses import dataclass
from typing import List

from app.jobs.models import JobPost
from app.requirements.priority import RequirementPriority


@dataclass
class ExtractedRequirement:
    name: str
    priority: RequirementPriority = RequirementPriority.UNKNOWN


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


REQUIRED_PATTERNS = [
    r"\brequired\b",
    r"\bmust[- ]have\b",
    r"\bessential\b",
    r"\bmandatory\b",
]

PREFERRED_PATTERNS = [
    r"\bpreferred\b",
    r"\bnice[- ]to[- ]have\b",
    r"\bwould be a plus\b",
    r"\bis a plus\b",
    r"\bare a plus\b",
    r"\bbonus\b",
]


def normalize(value: str) -> str:
    """Normalize text for deterministic comparison."""
    return value.strip().lower()


def requirement_in_text(requirement: str, text: str) -> bool:
    """Match a requirement without matching it inside another word."""
    pattern = rf"(?<!\w){re.escape(requirement)}(?!\w)"
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def _sentences(text: str) -> List[str]:
    """Split text into simple sentence-like segments."""
    return [
        segment.strip()
        for segment in re.split(r"[.!?\n;]+", text)
        if segment.strip()
    ]


def _priority_in_segment(
    requirement: str,
    segment: str,
) -> RequirementPriority:
    """Detect priority only when wording relates to this requirement."""
    if not requirement_in_text(requirement, segment):
        return RequirementPriority.UNKNOWN

    has_required = any(
        re.search(pattern, segment, flags=re.IGNORECASE)
        for pattern in REQUIRED_PATTERNS
    )
    has_preferred = any(
        re.search(pattern, segment, flags=re.IGNORECASE)
        for pattern in PREFERRED_PATTERNS
    )

    if has_required and has_preferred:
        return RequirementPriority.UNKNOWN
    if has_required:
        return RequirementPriority.REQUIRED
    if has_preferred:
        return RequirementPriority.PREFERRED

    return RequirementPriority.UNKNOWN


def _detect_priority(
    requirement: str,
    text: str,
) -> RequirementPriority:
    """Resolve priority from all segments that mention a requirement."""
    detected_priorities = []

    for segment in _sentences(text):
        priority = _priority_in_segment(requirement, segment)

        if priority != RequirementPriority.UNKNOWN:
            detected_priorities.append(priority)

    # No explicit priority evidence.
    if not detected_priorities:
        return RequirementPriority.UNKNOWN

    # Conflicting explicit evidence.
    unique_priorities = set(detected_priorities)

    if len(unique_priorities) > 1:
        return RequirementPriority.UNKNOWN

    return detected_priorities[0]


def extract_requirements(job: JobPost) -> List[ExtractedRequirement]:
    """
    Extract explicit and recognized requirements from a job post.

    Priority is assigned only when explicit wording is associated
    with the individual requirement. Ambiguous and conflicting cases
    remain UNKNOWN.
    """
    searchable_text = " ".join(
        [job.description, *job.skills]
    )

    requirements: List[ExtractedRequirement] = []
    requirement_names = set()

    # Preserve explicit skill order and deduplicate case-insensitively.
    for skill in job.skills:
        if not skill or not skill.strip():
            continue

        normalized_skill = normalize(skill)

        if normalized_skill in requirement_names:
            continue

        requirements.append(
            ExtractedRequirement(
                name=skill.strip(),
                priority=_detect_priority(skill.strip(), searchable_text),
            )
        )
        requirement_names.add(normalized_skill)

    # Add recognized requirements that were not listed explicitly.
    for requirement in KNOWN_REQUIREMENTS:
        normalized_requirement = normalize(requirement)

        if normalized_requirement in requirement_names:
            continue

        if requirement_in_text(requirement, searchable_text):
            requirements.append(
                ExtractedRequirement(
                    name=requirement,
                    priority=_detect_priority(
                        requirement,
                        searchable_text,
                    ),
                )
            )
            requirement_names.add(normalized_requirement)

    return requirements
