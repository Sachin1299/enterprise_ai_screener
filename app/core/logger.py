import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any, Dict


class JSONFormatter(logging.Formatter):
    """
    Formatter that outputs JSON strings containing logs with contextual metadata.
    Enables centralized log aggregation (CloudWatch, Datadog, ELK) without custom regex parsing.
    """
    def format(self, record: logging.LogRecord) -> str:
        log_record: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "func": record.funcName,
            "line": record.lineno,
        }

        # Include custom extra attributes passed via logger.info("...", extra={...})
        standard_fields = {
            "name", "msg", "args", "levelname", "levelno", "pathname", "filename",
            "module", "exc_info", "exc_text", "stack_info", "lineno", "funcName",
            "created", "msecs", "relativeCreated", "thread", "threadName",
            "processName", "process", "message"
        }
        for key, value in record.__dict__.items():
            if key not in standard_fields and not key.startswith("_"):
                log_record[key] = value

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record)


class ColoredConsoleFormatter(logging.Formatter):
    """
    Human-readable colored formatter for local development in PowerShell / Bash.
    """
    COLORS = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Green
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[41m",  # Red background
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, self.RESET)
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        msg = super().format(record)
        return f"{self.RESET}[{timestamp}] {color}{record.levelname:<8}{self.RESET} [{record.name}] {msg}"


def setup_logging(log_level: str = "INFO", is_production: bool = False) -> None:
    """
    Configures root and application loggers.
    Uses JSON formatting in production and colored human-readable logs in local development.
    """
    level = getattr(logging, log_level.upper(), logging.INFO)
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Clear existing handlers to prevent duplicate lines
    root_logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    if is_production:
        handler.setFormatter(JSONFormatter())
    else:
        formatter = ColoredConsoleFormatter(
            fmt="%(message)s"
        )
        handler.setFormatter(formatter)

    root_logger.addHandler(handler)

    # Tone down noisy third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("chromadb").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Retrieves a named logger instance.
    """
    return logging.getLogger(name)
