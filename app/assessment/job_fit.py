from dataclasses import dataclass
from typing import List

from app.matching.profile_matcher import RequirementMatch


@dataclass
class FitAssessment:
    total_requirements: int
    supported_requirements: int
    unsupported_requirements: int
    score: float
    level: str
    critical_gaps: List[str]


def assess_job_fit(
    requirement_matches: List[RequirementMatch],
) -> FitAssessment:
    """
    Calculate an initial job-fit assessment from requirement matches.

    This first version treats all requirements equally.
    Requirement priority will be introduced in a later iteration.
    """

    total = len(requirement_matches)

    if total == 0:
        return FitAssessment(
            total_requirements=0,
            supported_requirements=0,
            unsupported_requirements=0,
            score=0.0,
            level="no requirements",
            critical_gaps=[],
        )

    supported = sum(
        1
        for match in requirement_matches
        if match.status == "supported"
    )

    unsupported = total - supported

    score = (supported / total) * 100

    if score >= 80:
        level = "strong match"
    elif score >= 60:
        level = "good match"
    elif score >= 40:
        level = "partial match"
    else:
        level = "weak match"

    critical_gaps = [
        match.requirement
        for match in requirement_matches
        if match.status == "unsupported"
    ]

    return FitAssessment(
        total_requirements=total,
        supported_requirements=supported,
        unsupported_requirements=unsupported,
        score=round(score, 2),
        level=level,
        critical_gaps=critical_gaps,
    )