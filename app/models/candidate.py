import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class PageCitation(BaseModel):
    """
    Verifiable evidence citation extracted from candidate resume.
    Ensures zero hallucination by anchoring claims to exact page numbers and quotes.
    """
    page_number: int = Field(..., ge=1, description="Page number in the original PDF resume")
    exact_quote: str = Field(..., description="Exact textual excerpt from the candidate resume")
    context_snippet: Optional[str] = Field(default=None, description="Surrounding contextual sentence")


class SkillMatchStatus(str, Enum):
    FOUND = "found"
    PARTIAL = "partial"
    MISSING = "missing"


class SkillMatch(BaseModel):
    """
    Evaluation breakdown for an individual skill.
    """
    skill_name: str
    status: SkillMatchStatus
    years_detected: Optional[float] = None
    citations: List[PageCitation] = Field(default_factory=list)
    reasoning: str = Field(..., description="Explainable justification for the status")


class CandidateMetadata(BaseModel):
    """
    Ingested candidate profile metadata.
    """
    candidate_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    candidate_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    total_experience_years: Optional[float] = None
    total_pages: int = Field(default=1, ge=1)
    raw_file_path: str
    skills_detected: List[str] = Field(default_factory=list)
    ingested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class RecommendedAction(str, Enum):
    INVITE = "invite"                 # Candidate meets threshold -> schedule initial interview
    REJECT = "reject"                 # Critical must-haves missing -> send respectful rejection
    MANUAL_REVIEW = "manual_review"   # Borderline or ambiguous -> recruiter human review


class ScreeningResult(BaseModel):
    """
    Complete audit-ready candidate screening assessment.
    """
    screening_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    candidate_id: str
    candidate_name: Optional[str] = None
    job_id: str
    job_title: str
    overall_match_score: float = Field(..., ge=0.0, le=100.0, description="Composite score (0 to 100)")
    experience_match: bool = Field(..., description="Whether candidate satisfies minimum required YOE")
    skill_matches: List[SkillMatch] = Field(default_factory=list)
    missing_critical_skills: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    concerns: List[str] = Field(default_factory=list)
    recommended_action: RecommendedAction
    action_justification: str
    citations_summary: List[PageCitation] = Field(default_factory=list)
    screened_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
