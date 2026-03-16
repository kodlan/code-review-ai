"""Prompt templates for the review chain."""

from langchain_core.prompts import ChatPromptTemplate

REVIEW_SYSTEM_PROMPT = """\
You are an expert Python code reviewer. You review Git diffs and provide \
structured, actionable feedback.

Focus on these categories:
- **bug**: Likely bugs, logic errors, or incorrect behavior
- **edge_case**: Missing edge case handling, boundary conditions
- **readability**: Code clarity, naming, structure, Pythonic patterns
- **testing**: Missing tests, untested paths, test quality issues
- **maintainability**: Code that will be hard to change, coupling, duplication

Rules:
- Only comment on code that is added or changed in the diff (lines starting with +).
- Do not comment on deleted code unless the deletion itself introduces a bug.
- Be concise. Every comment must be actionable.
- If the diff looks good, say so with an empty comments list.
- Assign severity: critical (must fix), warning (should fix), info (nice to have).
{styleguide_section}"""

REVIEW_HUMAN_PROMPT = """\
Review the following Git diff:

```diff
{diff}
```"""


def build_prompt(styleguide: str | None = None) -> ChatPromptTemplate:
    """Build the review prompt, optionally including styleguide content."""
    if styleguide:
        styleguide_section = (
            "\n\nThe following project-specific style guide must also be applied:\n\n"
            f"```markdown\n{styleguide}\n```\n"
        )
    else:
        styleguide_section = ""

    return ChatPromptTemplate.from_messages([
        ("system", REVIEW_SYSTEM_PROMPT),
        ("human", REVIEW_HUMAN_PROMPT),
    ]).partial(styleguide_section=styleguide_section)
