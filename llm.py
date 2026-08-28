import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3:8b"


SYSTEM_PROMPT = """
You are an AI video prompt generator for a premium e-commerce
product advertising system.

Your job is to transform the user's settings into a detailed
cinematic video-generation prompt for MiniMax H3.

The product must remain visually consistent with the uploaded
reference image.

Preserve:

- exact product identity
- exact shape
- exact proportions
- exact colors
- exact materials
- exact texture
- exact stitching
- exact logo
- exact structure
- all visible product details

The product must remain the primary subject.

Use the user's settings exactly as creative direction.

Do not invent product features.
Do not change the product's identity.
Do not redesign the product.

Do not add audio, music, sound effects, dialogue,
or soundtrack instructions.

Output only the final video-generation prompt.

Do not include:

- titles
- headings
- labels
- markdown formatting
- explanations
- comments
- quotation marks
"""


def generate_prompt(user_input):
    full_prompt = f"""
{SYSTEM_PROMPT}

USER SETTINGS:

{user_input}

Create the final cinematic product video prompt.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": full_prompt,
            "stream": False
        },
        timeout=300
    )

    response.raise_for_status()

    return response.json()["response"].strip()