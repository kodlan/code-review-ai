"""Pydantic models for structured review output."""

from enum import Enum

from pydantic import BaseModel, Field


class Severity(str, Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


class ReviewComment(BaseModel):
    category: str = Field(
        description="One of: bug, edge_case, readability, testing, maintainability",
    )
    severity: Severity = Field(
        description="How severe this issue is",
    )
    file_path: str = Field(
        description="The file path this comment refers to",
    )
    line_hint: str | None = Field(
        default=None,
        description="A snippet or line reference from the diff",
    )
    comment: str = Field(
        description="The review comment explaining the issue",
    )
    suggestion: str | None = Field(
        default=None,
        description="A concrete code suggestion to fix the issue, if applicable",
    )


class ReviewResult(BaseModel):
    summary: str = Field(
        description="A 1-3 sentence overall summary of the diff quality",
    )
    comments: list[ReviewComment] = Field(
        default_factory=list,
        description="List of specific review comments",
    )
    verdict: str = Field(
        description="One of: approve, request_changes, comment_only",
    )
