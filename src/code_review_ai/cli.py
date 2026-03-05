"""CLI entry point for review-ai."""

import typer

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
    typer.echo("review-ai: not yet implemented")


if __name__ == "__main__":
    app()
