def build_proposal_prompt(
    job_title: str,
    job_description: str,
) -> str:
    return f"""
You are an expert freelancer proposal writer.

Write a professional proposal for the following freelance job.

JOB TITLE:
{job_title}

JOB DESCRIPTION:
{job_description}

Requirements:
- Show that you understand the client's requirements.
- Focus on relevant skills and experience.
- Be professional and concise.
- Do not invent experience, skills, qualifications, or project details.
- Do not use generic filler.
- Write only the proposal text.
""".strip()