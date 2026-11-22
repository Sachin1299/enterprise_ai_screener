import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, model_validator


class StrictnessLevel(str, Enum):
    """
    Recruiter evaluation strictness profile.
    """
    STRICT = "strict"        # Candidate must satisfy 100% of must-have skills and meet/exceed min YOE.
    BALANCED = "balanced"    # Evaluates composite weighted score; strong competencies can balance small gaps.
    LENIENT = "lenient"      # Focuses on transferable skills and growth potential.


class RubricWeights(BaseModel):
    """
    Configurable scoring weights for screening evaluation.
    Must sum up to 1.0 (with slight floating point tolerance).
    """
    skills: float = Field(default=0.50, ge=0.0, le=1.0, description="Weight for technical skill alignment")
    experience: float = Field(default=0.30, ge=0.0, le=1.0, description="Weight for years of experience & seniority")
    domain_education: float = Field(default=0.20, ge=0.0, le=1.0, description="Weight for domain/education relevance")

    @model_validator(mode="after")
    def validate_weights_sum(self) -> "RubricWeights":
        total = self.skills + self.experience + self.domain_education
        if not (0.99 <= total <= 1.01):
            raise ValueError(f"Rubric weights must sum to 1.0 (got {total:.2f})")
        return self


class JobSpecification(BaseModel):
    """
    Canonical job requirement schema.
    All incoming job representations (form, text, PDF, URL) are normalized into this format.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(..., description="Target Job Title (e.g. Senior Backend Engineer)")
    department: Optional[str] = Field(default=None, description="Department or business unit")
    min_experience_years: float = Field(default=0.0, ge=0.0, description="Minimum mandatory professional experience")
    must_have_skills: List[str] = Field(default_factory=list, description="Non-negotiable mandatory skills")
    good_to_have_skills: List[str] = Field(default_factory=list, description="Preferred/bonus skills")
    strictness_level: StrictnessLevel = Field(default=StrictnessLevel.BALANCED)
    custom_rubric: Optional[str] = Field(
        default=None,
        description="Custom recruiter criteria (e.g. 'Must have production Kafka experience, not just coursework')"
    )
    scoring_weights: RubricWeights = Field(default_factory=RubricWeights)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class JobInputMode(str, Enum):
    STRUCTURED = "structured"
    RAW_TEXT = "raw_text"
    URL = "url"
    FILE = "file"


class JobIngestRequest(BaseModel):
    """
    API payload for ingesting a Job Requirement in any of the 3 supported modes.
    """
    input_mode: JobInputMode = Field(default=JobInputMode.RAW_TEXT)
    raw_text: Optional[str] = Field(default=None, description="Raw job description text or markdown")
    url: Optional[str] = Field(default=None, description="Public job posting URL (e.g. LinkedIn, Greenhouse)")
    structured_spec: Optional[JobSpecification] = Field(default=None, description="Direct structured job specification")
