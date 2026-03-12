"""Tests for git_utils module."""

import subprocess
from pathlib import Path

import pytest

from code_review_ai.git_utils import GitError, find_styleguide, get_diff, validate_repo


def test_validate_repo_success(tmp_git_repo: Path):
    validate_repo(tmp_git_repo)  # Should not raise


def test_validate_repo_not_a_repo(tmp_path: Path):
    with pytest.raises(GitError):
        validate_repo(tmp_path)


def test_get_diff_unstaged(tmp_git_repo: Path):
    diff = get_diff(tmp_git_repo)
    assert "+print('hello world')" in diff


def test_get_diff_staged(tmp_git_repo: Path):
    subprocess.run(
        ["git", "add", "."], cwd=tmp_git_repo, check=True, capture_output=True,
    )
    diff = get_diff(tmp_git_repo)
    assert "+print('hello world')" in diff


def test_get_diff_with_target(tmp_git_repo: Path):
    diff = get_diff(tmp_git_repo, diff_target="HEAD")
    assert "+print('hello world')" in diff


def test_get_diff_empty(tmp_git_repo: Path):
    subprocess.run(
        ["git", "checkout", "--", "."],
        cwd=tmp_git_repo, check=True, capture_output=True,
    )
    diff = get_diff(tmp_git_repo)
    assert diff.strip() == ""


def test_find_styleguide_auto_detect(tmp_git_repo: Path):
    (tmp_git_repo / "styleguide.md").write_text("# Rules\n- Use type hints\n")
    result = find_styleguide(tmp_git_repo)
    assert "Use type hints" in result


def test_find_styleguide_not_found(tmp_git_repo: Path):
    result = find_styleguide(tmp_git_repo)
    assert result is None


def test_find_styleguide_explicit(tmp_git_repo: Path):
    sg = tmp_git_repo / "custom-style.md"
    sg.write_text("# Custom\n")
    result = find_styleguide(tmp_git_repo, explicit_path=str(sg))
    assert "Custom" in result


def test_find_styleguide_explicit_missing(tmp_git_repo: Path):
    with pytest.raises(GitError, match="Styleguide not found"):
        find_styleguide(tmp_git_repo, explicit_path="/nonexistent/style.md")
