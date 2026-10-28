
from app.assessment.job_fit import assess_job_fit
from app.matching.profile_matcher import RequirementMatch
from app.requirements.priority import RequirementPriority


def create_match(
    requirement: str,
    status: str,
) -> RequirementMatch:
    return RequirementMatch(
        requirement=requirement,
        priority=RequirementPriority.UNKNOWN,
        status=status,
    )


def test_assess_job_fit_with_supported_and_unsupported_requirements():
    matches = [
        create_match("Python", "supported"),
        create_match("Django", "supported"),
        create_match("AWS", "supported"),
        create_match("PostgreSQL", "unsupported"),
        create_match("E-commerce", "supported"),
        create_match("Docker", "unsupported"),
    ]

    assessment = assess_job_fit(matches)

    assert assessment.total_requirements == 6
    assert assessment.supported_requirements == 4
    assert assessment.unsupported_requirements == 2
    assert assessment.score == 66.67
    assert assessment.level == "good match"
    assert set(assessment.critical_gaps) == {"PostgreSQL", "Docker"}


def test_assess_job_fit_with_no_requirements():
    assessment = assess_job_fit([])

    assert assessment.total_requirements == 0
    assert assessment.supported_requirements == 0
    assert assessment.unsupported_requirements == 0
    assert assessment.score == 0.0
    assert assessment.level == "no requirements"
    assert assessment.critical_gaps == []


def test_assess_job_fit_with_all_requirements_supported():
    matches = [
        create_match("Python", "supported"),
        create_match("Django", "supported"),
    ]

    assessment = assess_job_fit(matches)

    assert assessment.total_requirements == 2
    assert assessment.supported_requirements == 2
    assert assessment.unsupported_requirements == 0
    assert assessment.score == 100.0
    assert assessment.level == "strong match"
    assert assessment.critical_gaps == []


def test_assess_job_fit_with_all_requirements_unsupported():
    matches = [
        create_match("PostgreSQL", "unsupported"),
        create_match("Docker", "unsupported"),
    ]

    assessment = assess_job_fit(matches)

    assert assessment.total_requirements == 2
    assert assessment.supported_requirements == 0
    assert assessment.unsupported_requirements == 2
    assert assessment.score == 0.0
    assert assessment.level == "weak match"
    assert set(assessment.critical_gaps) == {"PostgreSQL", "Docker"}