from app.jobs.models import JobPost
from app.profile.profile_loader import load_profile
from app.matching.profile_matcher import match_profile_to_job
from app.requirements.priority import RequirementPriority


def test_profile_matcher_identifies_supported_and_unsupported_requirements():
    job = JobPost(
        platform="upwork",
        title="Senior Python Django Developer for E-commerce Platform",
        description=(
            "We need an experienced developer to improve our Django "
            "e-commerce application using Python, PostgreSQL and AWS. "
            "Docker experience is preferred."
        ),
        skills=[
            "Python",
            "Django",
            "PostgreSQL",
            "AWS",
            "E-commerce",
        ],
    )

    profile = load_profile()
    result = match_profile_to_job(job, profile)

    matches_by_name = {
        match.requirement: match
        for match in result.requirement_matches
    }

    # Verify that the expected requirements were extracted.
    assert set(matches_by_name) == {
        "Python",
        "Django",
        "PostgreSQL",
        "AWS",
        "E-commerce",
        "Docker",
    }

    # Verify supported requirements.
    assert matches_by_name["Python"].status == "supported"
    assert matches_by_name["Python"].evidence_type == "skill"

    assert matches_by_name["Django"].status == "supported"
    assert matches_by_name["Django"].evidence_type == "skill"

    assert matches_by_name["AWS"].status == "supported"
    assert matches_by_name["AWS"].evidence_type == "skill"

    assert matches_by_name["E-commerce"].status == "supported"
    assert matches_by_name["E-commerce"].evidence_type == "project"

    # Verify unsupported requirements.
    assert matches_by_name["PostgreSQL"].status == "unsupported"
    assert matches_by_name["PostgreSQL"].evidence_type is None

    assert matches_by_name["Docker"].status == "unsupported"
    assert matches_by_name["Docker"].evidence_type is None

    # Verify that priority is preserved by the matcher.
    assert all(
        match.priority == RequirementPriority.UNKNOWN
        for match in result.requirement_matches
    )

    # Verify the categorized evidence collections.
    assert len(result.matched_skills) == 3
    assert len(result.relevant_projects) == 1
    assert len(result.relevant_experience) == 0
    assert len(result.relevant_portfolio) == 0