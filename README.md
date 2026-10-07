# Natural Language to Code Generator (Week 1)

A fast, lightweight CLI coding agent that converts natural language task descriptions into clean, executable Python code using Groq and Meta's Llama 3.3 70B model.

## Features
- **Prompt Isolation:** Strict system prompt enforcing code-only returns.
- **Defensive Regex Sanitation:** Automatically strips accidental markdown backticks and fences.
- **Dual Output:** Streams code to terminal standard output and auto-saves to `.py` script files.
- **Comprehensive Coverage:** Verified against 8 core tasks across math, string manipulation, and nested collection operations.

## Setup
```bash
git clone <your-repo-link>
cd nl2code_generator
python -m venv venv
source venv/bin/activate  # Or .\venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt