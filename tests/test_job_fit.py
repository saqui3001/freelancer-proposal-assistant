from app.matching.profile_matcher import RequirementMatch
from app.assessment.job_fit import assess_job_fit


matches = [
    RequirementMatch(
        requirement="Python",
        status="supported",
        evidence_type="skill",
    ),
    RequirementMatch(
        requirement="Django",
        status="supported",
        evidence_type="skill",
    ),
    RequirementMatch(
        requirement="AWS",
        status="supported",
        evidence_type="skill",
    ),
    RequirementMatch(
        requirement="PostgreSQL",
        status="unsupported",
    ),
    RequirementMatch(
        requirement="E-commerce",
        status="supported",
        evidence_type="project",
    ),
    RequirementMatch(
        requirement="Docker",
        status="unsupported",
    ),
]

assessment = assess_job_fit(matches)

print("Job fit assessment:")
print("Total requirements:", assessment.total_requirements)
print("Supported:", assessment.supported_requirements)
print("Unsupported:", assessment.unsupported_requirements)
print("Score:", assessment.score)
print("Level:", assessment.level)
print("Critical gaps:", assessment.critical_gaps)