# code-review-ai

A minimal AI-powered code review CLI that reviews local Git diffs and produces structured Markdown feedback. Supports repo-specific style guides via `styleguide.md`.

## Setup

Requires Python 3.11+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

## Usage

```bash
# Review changes in the current repo (staged, or unstaged as fallback)
uv run review-ai review

# Review against a specific target (branch, commit, etc.)
uv run review-ai review --diff-target main

# Review a different repository
uv run review-ai review --repo-path /path/to/repo

# Use a custom styleguide
uv run review-ai review --styleguide ./my-style.md

# Show debug info (diff contents, styleguide status)
uv run review-ai review --verbose
```

## Tests

```bash
uv run pytest -v
```
