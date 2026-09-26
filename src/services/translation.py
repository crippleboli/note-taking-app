import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import APIError, OpenAI


PROMPT_PATH = Path(__file__).resolve().parents[2] / "prompts" / "translate_prompt.md"


class TranslationError(RuntimeError):
    """Raised when a translation cannot be produced or validated."""


class TranslationConfigurationError(TranslationError):
    """Raised when translation service configuration is missing."""


def _load_prompts():
    try:
        prompt_file = PROMPT_PATH.read_text(encoding="utf-8")
    except OSError as error:
        raise TranslationError("The translation prompt file could not be loaded.") from error

    system_marker = "## System Prompt\n"
    user_marker = "\n## User Prompt\n"
    system_start = prompt_file.find(system_marker)
    user_start = prompt_file.find(user_marker)
    if system_start != 0 or user_start < len(system_marker):
        raise TranslationError("The translation prompt file has an invalid format.")

    system_prompt = prompt_file[len(system_marker):user_start].strip()
    user_template = prompt_file[user_start + len(user_marker):].strip()
    if not system_prompt or not user_template:
        raise TranslationError("The translation prompt file is incomplete.")
    return system_prompt, user_template


def translate_note(title: str, content: str, target_language: str) -> dict[str, str]:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise TranslationConfigurationError(
            "OPENAI_API_KEY is not set. Add it to the project .env file."
        )

    system_prompt, user_template = _load_prompts()
    user_prompt = (
        user_template
        .replace("{{target_language}}", target_language)
        .replace(
            "{{note_json}}",
            json.dumps({"title": title, "content": content}, ensure_ascii=False),
        )
    )

    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
        )
    except APIError as error:
        raise TranslationError("The translation provider request failed.") from error

    if not response.choices:
        raise TranslationError("The translation response did not contain any choices.")
    result_text = response.choices[0].message.content
    if not result_text:
        raise TranslationError("The translation response did not contain any text.")
    try:
        result = json.loads(result_text)
    except json.JSONDecodeError as error:
        raise TranslationError("The translation response was not valid JSON.") from error

    if (
        not isinstance(result, dict)
        or set(result) != {"title", "content"}
        or not isinstance(result["title"], str)
        or not isinstance(result["content"], str)
    ):
        raise TranslationError(
            'The translation response must contain string "title" and "content" fields.'
        )
    return result
