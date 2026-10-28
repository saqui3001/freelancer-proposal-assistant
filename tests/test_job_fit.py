
from app.assessment.job_fit import assess_job_fit
from app.matching.profile_matcher import RequirementMatch
from app.requirements.priority import RequirementPriority


def create_match(
    requirement: str,
    status: str,
    priority: RequirementPriority = RequirementPriority.UNKNOWN,
) -> RequirementMatch:
    return RequirementMatch(
        requirement=requirement,
        priority=priority,
        status=status,
    )


def test_assess_job_fit_uses_weighted_score():
    matches = [
        create_match("Python", "supported", RequirementPriority.REQUIRED),
        create_match("Django", "supported", RequirementPriority.REQUIRED),
        create_match("PostgreSQL", "unsupported", RequirementPriority.REQUIRED),
        create_match("Docker", "unsupported", RequirementPriority.PREFERRED),
    ]

    assessment = assess_job_fit(matches)

    assert assessment.total_requirements == 4
    assert assessment.supported_requirements == 2
    assert assessment.unsupported_requirements == 2
    assert assessment.score == 60.0


def test_assess_job_fit_separates_gaps_by_priority():
    matches = [
        create_match("Python", "supported", RequirementPriority.REQUIRED),
        create_match("PostgreSQL", "unsupported", RequirementPriority.REQUIRED),
        create_match("Docker", "unsupported", RequirementPriority.PREFERRED),
        create_match("Kubernetes", "unsupported", RequirementPriority.UNKNOWN),
    ]

    assessment = assess_job_fit(matches)

    assert assessment.critical_gaps == ["PostgreSQL"]
    assert assessment.preferred_gaps == ["Docker"]
    assert assessment.unclassified_gaps == ["Kubernetes"]


def test_assess_job_fit_with_no_requirements():
    assessment = assess_job_fit([])

    assert assessment.total_requirements == 0
    assert assessment.supported_requirements == 0
    assert assessment.unsupported_requirements == 0
    assert assessment.score == 0.0
    assert assessment.level == "no requirements"
    assert assessment.critical_gaps == []
    assert assessment.preferred_gaps == []
    assert assessment.unclassified_gaps == []


def test_assess_job_fit_with_all_requirements_supported():
    matches = [
        create_match("Python", "supported", RequirementPriority.REQUIRED),
        create_match("Docker", "supported", RequirementPriority.PREFERRED),
    ]

    assessment = assess_job_fit(matches)

    assert assessment.score == 100.0
    assert assessment.level == "strong match"
    assert assessment.critical_gaps == []
    assert assessment.preferred_gaps == []
    assert assessment.unclassified_gaps == []


def test_missing_required_requirement_is_reported_as_critical():
    matches = [
        create_match("Python", "supported", RequirementPriority.REQUIRED),
        create_match("Django", "supported", RequirementPriority.REQUIRED),
        create_match("PostgreSQL", "unsupported", RequirementPriority.REQUIRED),
        create_match("Docker", "supported", RequirementPriority.PREFERRED),
        create_match("AWS", "supported", RequirementPriority.PREFERRED),
    ]

    assessment = assess_job_fit(matches)

    assert assessment.score == 72.73
    assert assessment.critical_gaps == ["PostgreSQL"]
