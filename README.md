# Natural Language to Code Generator

A lightweight CLI that converts natural-language task descriptions into clean,
executable Python scripts using Groq-hosted language models.

## Features

- Strict system prompting for code-only model responses.
- Removes accidental Markdown code fences before saving output.
- Prints generated code and saves it under `generated_scripts/`.
- Includes a batch harness covering eight common Python tasks.

## Setup

```powershell
git clone https://github.com/Jeevanp69/nl2code-generator.git
cd nl2code-generator
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```dotenv
GROQ_API_KEY=your_groq_api_key
```

Optionally set `GROQ_MODEL` to a model available to your Groq account. Without
it, the generator selects a supported model from the account's available model
list.

## Usage

Generate one script:

```powershell
python generate.py "Check if a number is prime and return a boolean" -o is_prime.py
```

Generate all eight example scripts:

```powershell
python test_tasks.py
```

Generated files are written to `generated_scripts/`.

## Security

Keep `.env` private and never commit API keys. Rotate a key immediately if it
has been exposed.