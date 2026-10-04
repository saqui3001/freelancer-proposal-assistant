from dataclasses import dataclass, field
from typing import Any, Dict, List

from app.jobs.models import JobPost
from app.requirements.requirement_extractor import extract_requirements


@dataclass
class RequirementMatch:
    requirement: str
    status: str
    evidence_type: str | None = None
    evidence: Any = None


@dataclass
class MatchingResult:
    requirement_matches: List[RequirementMatch] = field(default_factory=list)
    matched_skills: List[Dict[str, Any]] = field(default_factory=list)
    relevant_experience: List[Dict[str, Any]] = field(default_factory=list)
    relevant_projects: List[Dict[str, Any]] = field(default_factory=list)
    relevant_portfolio: List[Dict[str, Any]] = field(default_factory=list)


def normalize(value: str) -> str:
    """Normalize text for deterministic comparison."""
    return value.strip().lower()


def contains_requirement(text: str, requirement: str) -> bool:
    """Return True when the normalized requirement appears in text."""
    return normalize(requirement) in normalize(text)


def find_requirement_evidence(
    requirement: str,
    profile: Dict[str, Any],
) -> RequirementMatch:
    """
    Search the verified profile for evidence supporting one job requirement.

    Evidence is checked in this order:
    1. Skills
    2. Experience
    3. Projects
    4. Portfolio

    No evidence is inferred when no direct profile match exists.
    """

    normalized_requirement = normalize(requirement)

    # 1. Skills
    for skill in profile.get("skills", []):
        skill_name = skill.get("name", "")

        if (
            skill_name
            and normalize(skill_name) == normalized_requirement
        ):
            return RequirementMatch(
                requirement=requirement,
                status="supported",
                evidence_type="skill",
                evidence=skill,
            )

    # 2. Experience
    for experience in profile.get("experience", []):
        searchable_values = [
            experience.get("role", ""),
            experience.get("description", ""),
            *experience.get("technologies", []),
        ]

        if any(
            value and contains_requirement(value, requirement)
            for value in searchable_values
        ):
            return RequirementMatch(
                requirement=requirement,
                status="supported",
                evidence_type="experience",
                evidence=experience,
            )

    # 3. Projects
    for project in profile.get("projects", []):
        searchable_values = [
            project.get("name", ""),
            project.get("description", ""),
            project.get("role", ""),
            *project.get("technologies", []),
        ]

        if any(
            value and contains_requirement(value, requirement)
            for value in searchable_values
        ):
            return RequirementMatch(
                requirement=requirement,
                status="supported",
                evidence_type="project",
                evidence=project,
            )

    # 4. Portfolio
    for item in profile.get("portfolio", []):
        searchable_values = [
            item.get("name", ""),
            item.get("description", ""),
            *item.get("technologies", []),
            *item.get("categories", []),
        ]

        if any(
            value and contains_requirement(value, requirement)
            for value in searchable_values
        ):
            return RequirementMatch(
                requirement=requirement,
                status="supported",
                evidence_type="portfolio",
                evidence=item,
            )

    # No verified evidence
    return RequirementMatch(
        requirement=requirement,
        status="unsupported",
    )


def match_profile_to_job(
    job: JobPost,
    profile: Dict[str, Any],
) -> MatchingResult:
    """
    Match all detected job requirements against verified profile evidence.
    """

    result = MatchingResult()

    # Extract requirements from explicit skills, title, and description.
    requirements = extract_requirements(job)

    for requirement in requirements:
        match = find_requirement_evidence(
            requirement=requirement,
            profile=profile,
        )

        result.requirement_matches.append(match)

        if match.status != "supported":
            continue

        if match.evidence_type == "skill":
            if match.evidence not in result.matched_skills:
                result.matched_skills.append(match.evidence)

        elif match.evidence_type == "experience":
            if match.evidence not in result.relevant_experience:
                result.relevant_experience.append(match.evidence)

        elif match.evidence_type == "project":
            if match.evidence not in result.relevant_projects:
                result.relevant_projects.append(match.evidence)

        elif match.evidence_type == "portfolio":
            if match.evidence not in result.relevant_portfolio:
                result.relevant_portfolio.append(match.evidence)

    return result