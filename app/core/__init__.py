"""
Core module: Configuration, Structured Logging, and Exceptions
"""
from app.core.config import get_settings, Settings
from app.core.logger import get_logger, setup_logging
from app.core.exceptions import (
    BaseAppException,
    CandidateNotFoundError,
    InvalidJobSpecificationError,
    ResumeParsingError,
    RateLimitExceededError,
    UpstreamServiceError,
    AgentRecursionLimitError,
)

__all__ = [
    "get_settings",
    "Settings",
    "get_logger",
    "setup_logging",
    "BaseAppException",
    "CandidateNotFoundError",
    "InvalidJobSpecificationError",
    "ResumeParsingError",
    "RateLimitExceededError",
    "UpstreamServiceError",
    "AgentRecursionLimitError",
]

