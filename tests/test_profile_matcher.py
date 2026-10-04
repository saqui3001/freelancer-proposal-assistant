from app.jobs.models import JobPost
from app.profile.profile_loader import load_profile
from app.matching.profile_matcher import match_profile_to_job


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

print("Requirement analysis:")
for match in result.requirement_matches:
    evidence_type = match.evidence_type or "no evidence"
    print(
        f" - {match.requirement}: "
        f"{match.status} [{evidence_type}]"
    )

print()
print("Matched skills:", len(result.matched_skills))
print("Relevant experience:", len(result.relevant_experience))
print("Relevant projects:", len(result.relevant_projects))
print("Relevant portfolio:", len(result.relevant_portfolio))