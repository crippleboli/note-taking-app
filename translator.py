import os
import sys

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def llm_generate(prompt: str) -> str:
    """Translate the supplied text into English with DeepSeek."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Add it to the project .env file."
        )

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional translator. Translate the user's "
                    "text into English and return only the translation."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    )
    translation = response.choices[0].message.content
    if translation is None:
        raise RuntimeError("The translation response did not contain any text.")
    return translation


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <text to translate>", file=sys.stderr)
        sys.exit(2)

    input_text = " ".join(sys.argv[1:])
    print(llm_generate(input_text))
