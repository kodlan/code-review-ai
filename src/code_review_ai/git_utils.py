"""Git subprocess utilities for reading diffs and repository info."""

import subprocess
from pathlib import Path


class GitError(Exception):
    """Raised when a git command fails."""


def _run_git(args: list[str], repo_path: Path) -> str:
    """Run a git command and return stdout."""
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise GitError(f"git {' '.join(args)} failed: {e.stderr.strip()}") from e
    except FileNotFoundError:
        raise GitError("git is not installed or not found on PATH") from None


def validate_repo(repo_path: Path) -> None:
    """Check that repo_path is a valid git repository."""
    if not repo_path.is_dir():
        raise GitError(f"Not a directory: {repo_path}")
    _run_git(["rev-parse", "--git-dir"], repo_path)


def get_diff(repo_path: Path, diff_target: str | None = None) -> str:
    """Get the git diff for the repository.

    If diff_target is provided, runs: git diff <target>
    Otherwise: tries staged diff first, falls back to unstaged diff.
    """
    repo_path = Path(repo_path).resolve()
    validate_repo(repo_path)

    if diff_target:
        return _run_git(["diff", diff_target], repo_path)

    # Try staged changes first
    diff = _run_git(["diff", "--cached"], repo_path)
    if diff.strip():
        return diff

    # Fall back to unstaged changes
    return _run_git(["diff"], repo_path)


def get_repo_root(repo_path: Path) -> Path:
    """Get the root directory of the git repository."""
    root = _run_git(["rev-parse", "--show-toplevel"], Path(repo_path).resolve())
    return Path(root.strip())


def find_styleguide(repo_path: Path, explicit_path: str | None = None) -> str | None:
    """Find and read the styleguide.

    If explicit_path is given, read that file (error if missing).
    Otherwise, look for styleguide.md in the repo root.
    Returns the file content as a string, or None if not found.
    """
    if explicit_path:
        p = Path(explicit_path)
        if not p.is_file():
            raise GitError(f"Styleguide not found: {explicit_path}")
        return p.read_text(encoding="utf-8")

    repo_root = get_repo_root(repo_path)
    styleguide_path = repo_root / "styleguide.md"
    if styleguide_path.is_file():
        return styleguide_path.read_text(encoding="utf-8")

    return None
