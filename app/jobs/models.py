from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class JobPost:
    platform: str
    title: str
    description: str
    source_url: str = ""
    skills: List[str] = field(default_factory=list)
    budget: Optional[str] = None
    job_type: Optional[str] = None
    experience_level: Optional[str] = None