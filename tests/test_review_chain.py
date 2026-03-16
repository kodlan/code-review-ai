"""Tests for prompt templates and review chain."""

from code_review_ai.prompts import build_prompt


def test_build_prompt_without_styleguide():
    prompt = build_prompt(styleguide=None)
    messages = prompt.format_messages(diff="some diff")
    system_msg = messages[0].content
    assert "expert Python code reviewer" in system_msg
    assert "style guide" not in system_msg


def test_build_prompt_with_styleguide():
    prompt = build_prompt(styleguide="- Always use type hints")
    messages = prompt.format_messages(diff="some diff")
    system_msg = messages[0].content
    assert "Always use type hints" in system_msg
    assert "style guide" in system_msg


def test_prompt_contains_diff():
    prompt = build_prompt()
    messages = prompt.format_messages(diff="+print('hello')")
    human_msg = messages[1].content
    assert "+print('hello')" in human_msg
