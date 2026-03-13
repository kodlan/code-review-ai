"""CLI entry point for review-ai."""

from pathlib import Path

import typer

from code_review_ai.git_utils import GitError, find_styleguide, get_diff

app = typer.Typer(
    name="review-ai",
    help="AI-powered code review CLI that reviews Git diffs.",
)


@app.command()
def review(
    repo_path: str = typer.Option(".", help="Path to the git repository"),
    styleguide: str | None = typer.Option(None, help="Path to styleguide.md"),
    model: str = typer.Option("gpt-4o-mini", help="OpenAI model to use"),
    diff_target: str | None = typer.Option(None, help="Git diff target (e.g. HEAD~1, main)"),
    output: str | None = typer.Option(None, help="Write output to file instead of stdout"),
    verbose: bool = typer.Option(False, help="Show debug info"),
) -> None:
    """Review the current Git diff using an LLM."""
    try:
        diff = get_diff(Path(repo_path), diff_target=diff_target)
    except GitError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

    if not diff.strip():
        typer.echo("No changes detected in the diff.")
        raise typer.Exit(code=0)

    try:
        styleguide_content = find_styleguide(Path(repo_path), explicit_path=styleguide)
    except GitError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

    if verbose:
        typer.echo(f"Diff length: {len(diff)} characters")
        typer.echo(f"Styleguide: {'found' if styleguide_content else 'not found'}")
        typer.echo("---")
        typer.echo(diff)

    typer.echo("Review processing not yet implemented.")


if __name__ == "__main__":
    app()
