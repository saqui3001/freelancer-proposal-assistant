
from dataclasses import dataclass
from typing import List

from app.matching.profile_matcher import RequirementMatch
from app.requirements.priority import RequirementPriority


@dataclass
class FitAssessment:
    total_requirements: int
    supported_requirements: int
    unsupported_requirements: int
    score: float
    level: str
    critical_gaps: List[str]
    preferred_gaps: List[str]
    unclassified_gaps: List[str]


PRIORITY_WEIGHTS = {
    RequirementPriority.REQUIRED: 3,
    RequirementPriority.PREFERRED: 1,
    RequirementPriority.UNKNOWN: 1,
}


def assess_job_fit(
    requirement_matches: List[RequirementMatch],
) -> FitAssessment:
    """Calculate weighted job fit and report gaps by requirement priority."""

    total = len(requirement_matches)

    if total == 0:
        return FitAssessment(
            total_requirements=0,
            supported_requirements=0,
            unsupported_requirements=0,
            score=0.0,
            level="no requirements",
            critical_gaps=[],
            preferred_gaps=[],
            unclassified_gaps=[],
        )

    supported = sum(
        1
        for match in requirement_matches
        if match.status == "supported"
    )
    unsupported = total - supported

    total_weight = sum(
        PRIORITY_WEIGHTS[match.priority]
        for match in requirement_matches
    )
    supported_weight = sum(
        PRIORITY_WEIGHTS[match.priority]
        for match in requirement_matches
        if match.status == "supported"
    )

    score = (supported_weight / total_weight) * 100

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
        if (
            match.status == "unsupported"
            and match.priority == RequirementPriority.REQUIRED
        )
    ]

    preferred_gaps = [
        match.requirement
        for match in requirement_matches
        if (
            match.status == "unsupported"
            and match.priority == RequirementPriority.PREFERRED
        )
    ]

    unclassified_gaps = [
        match.requirement
        for match in requirement_matches
        if (
            match.status == "unsupported"
            and match.priority == RequirementPriority.UNKNOWN
        )
    ]

    return FitAssessment(
        total_requirements=total,
        supported_requirements=supported,
        unsupported_requirements=unsupported,
        score=round(score, 2),
        level=level,
        critical_gaps=critical_gaps,
        preferred_gaps=preferred_gaps,
        unclassified_gaps=unclassified_gaps,
    )
