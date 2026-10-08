import argparse
import os
import re
import sys
from datetime import datetime, timezone

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

SYSTEM_PROMPT = """You are an expert Python code generator.
Follow these rules strictly:
1. Return ONLY valid, executable Python code.
2. Do NOT output any markdown backticks, explanations, preamble, or conversational text.
3. Include clear docstrings and comments where appropriate.
4. Do NOT wrap the response in ```python or ``` fences.
"""

MODEL_PREFERENCES = (
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "llama-4-scout-17b-16e-instruct",
    "qwen/qwen3-32b",
)

def clean_code(raw_text: str) -> str:
    """Strips markdown code blocks, backticks, and extraneous blank edges."""
    text = raw_text.strip()
    # Remove triple-backtick markdown blocks if the LLM includes them
    text = re.sub(r"^```(?:python)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()

def resolve_model(client: Groq, requested_model: str | None = None) -> str:
    """Use an explicit model or choose one currently available to the API key."""
    if requested_model:
        return requested_model

    available_models = {model.id for model in client.models.list().data}
    for candidate in MODEL_PREFERENCES:
        if candidate in available_models:
            return candidate

    raise RuntimeError(
        "No supported Groq text model is available for this API key. "
        "Set GROQ_MODEL in .env to a model listed in the Groq console."
    )

def generate_code(prompt: str, model: str | None = None) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY is not set in your .env file.", file=sys.stderr)
        sys.exit(1)

    client = Groq(api_key=api_key)
    model = resolve_model(client, model or os.getenv("GROQ_MODEL"))
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )
    raw_content = response.choices[0].message.content
    return clean_code(raw_content)

def save_code(code: str, output_path: str | None = None) -> str:
    output_dir = "generated_scripts"
    os.makedirs(output_dir, exist_ok=True)

    if not output_path:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"generated_{timestamp}.py")
    else:
        if not output_path.endswith(".py"):
            output_path += ".py"
        output_path = os.path.join(output_dir, os.path.basename(output_path))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(code + "\n")
    return output_path

def main():
    parser = argparse.ArgumentParser(description="Natural Language to Python Code Generator")
    parser.add_argument("task", nargs="?", help="Plain-English description of the Python task")
    parser.add_argument("-o", "--output", help="Custom output filename (e.g., check_prime.py)", default=None)
    args = parser.parse_args()

    task = args.task
    if not task:
        task = input("\nEnter task description: ").strip()

    if not task:
        print("Task description cannot be empty.")
        return

    print("\n[+] Generating code via Groq...")
    code = generate_code(task)

    print("\n" + "=" * 50)
    print("--- GENERATED PYTHON CODE ---")
    print("=" * 50)
    print(code)
    print("=" * 50)

    saved_file = save_code(code, args.output)
    print(f"\n[✓] Code successfully saved to: {saved_file}\n")

if __name__ == "__main__":
    main()