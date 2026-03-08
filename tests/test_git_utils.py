"""Tests for git_utils module."""

import subprocess
from pathlib import Path

import pytest

from code_review_ai.git_utils import GitError, get_diff, validate_repo


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
