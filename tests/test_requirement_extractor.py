from app.jobs.models import JobPost
from app.requirements.priority import RequirementPriority
from app.requirements.requirement_extractor import extract_requirements


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
    ],
)

requirements = extract_requirements(job)

print("Extracted requirements:")

for requirement in requirements:
    print(
        f" - {requirement.name}: "
        f"{requirement.priority.value}"
    )

print()
print("Total requirements:", len(requirements))

assert len(requirements) == 6
assert all(
    requirement.priority == RequirementPriority.UNKNOWN
    for requirement in requirements
)