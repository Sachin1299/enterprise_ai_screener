from typing import Any, Dict, Optional
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.core.logger import get_logger

logger = get_logger("app.core.exceptions")


class BaseAppException(Exception):
    """
    Base domain exception for all application-specific errors.
    Carries HTTP status code, machine-readable error code, and context payload.
    """
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: str = "INTERNAL_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}


class CandidateNotFoundError(BaseAppException):
    def __init__(self, candidate_id: str):
        super().__init__(
            message=f"Candidate with ID '{candidate_id}' not found.",
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="CANDIDATE_NOT_FOUND",
            details={"candidate_id": candidate_id},
        )


class InvalidJobSpecificationError(BaseAppException):
    def __init__(self, reason: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"Invalid job specification: {reason}",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="INVALID_JOB_SPECIFICATION",
            details=details,
        )


class ResumeParsingError(BaseAppException):
    def __init__(self, file_name: str, reason: str):
        super().__init__(
            message=f"Failed to parse resume '{file_name}': {reason}",
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="RESUME_PARSING_FAILED",
            details={"file_name": file_name, "reason": reason},
        )


class RateLimitExceededError(BaseAppException):
    def __init__(self, provider: str = "Google Gemini", retry_after_seconds: int = 60):
        super().__init__(
            message=f"Upstream {provider} API rate limit exceeded (HTTP 429).",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="RATE_LIMIT_EXCEEDED",
            details={"provider": provider, "retry_after_seconds": retry_after_seconds},
        )


class UpstreamServiceError(BaseAppException):
    def __init__(self, service_name: str, message: str, status_code: int = status.HTTP_502_BAD_GATEWAY):
        super().__init__(
            message=f"Error communicating with {service_name}: {message}",
            status_code=status_code,
            error_code="UPSTREAM_SERVICE_ERROR",
            details={"service_name": service_name},
        )


class AgentRecursionLimitError(BaseAppException):
    def __init__(self, max_depth: int = 10):
        super().__init__(
            message=f"Agent exceeded maximum reasoning steps ({max_depth}). Circuit breaker tripped.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="AGENT_RECURSION_LIMIT_EXCEEDED",
            details={"max_depth": max_depth},
        )


def register_exception_handlers(app: FastAPI) -> None:
    """
    Registers standardized error handlers with the FastAPI application.
    Ensures every error response follows a strict, consistent JSON contract.
    """
    @app.exception_handler(BaseAppException)
    async def app_exception_handler(request: Request, exc: BaseAppException) -> JSONResponse:
        logger.warning(
            f"Handled application exception: {exc.error_code} - {exc.message}",
            extra={"path": request.url.path, "error_code": exc.error_code, "status_code": exc.status_code}
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.error_code,
                    "message": exc.message,
                    "details": exc.details,
                }
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        logger.warning(
            f"Request validation failure on {request.url.path}",
            extra={"path": request.url.path, "errors": exc.errors()}
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": {
                    "code": "REQUEST_VALIDATION_ERROR",
                    "message": "Invalid request payload or query parameters.",
                    "details": {"validation_errors": exc.errors()},
                }
            }
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.error(
            f"Unhandled server error on {request.url.path}: {str(exc)}",
            exc_info=True,
            extra={"path": request.url.path}
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected server error occurred. Please contact system administrator.",
                    "details": {},
                }
            }
        )

