"""Tests for Pydantic models."""

from code_review_ai.models import ReviewComment, ReviewResult, Severity


def test_review_result_minimal():
    result = ReviewResult(
        summary="Looks good overall.",
        comments=[],
        verdict="approve",
    )
    assert result.summary == "Looks good overall."
    assert result.comments == []
    assert result.verdict == "approve"


def test_review_result_with_comments():
    comment = ReviewComment(
        category="bug",
        severity=Severity.CRITICAL,
        file_path="main.py",
        line_hint="+    return x / y",
        comment="Division by zero if y is 0.",
        suggestion="Add a check: if y == 0: raise ValueError(...)",
    )
    result = ReviewResult(
        summary="Found a potential bug.",
        comments=[comment],
        verdict="request_changes",
    )
    assert len(result.comments) == 1
    assert result.comments[0].severity == Severity.CRITICAL
    assert result.comments[0].category == "bug"


def test_review_comment_optional_fields():
    comment = ReviewComment(
        category="readability",
        severity=Severity.INFO,
        file_path="utils.py",
        comment="Consider a more descriptive variable name.",
    )
    assert comment.line_hint is None
    assert comment.suggestion is None
