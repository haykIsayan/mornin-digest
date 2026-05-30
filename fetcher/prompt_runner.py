
import anthropic
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def run_prompt(prompt: str) -> str:
    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            tools=[
                {
                    "type": "web_search_20250305",
                    "name": "web_search"
                }
            ],
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    except anthropic.AuthenticationError:
        raise Exception("Invalid API key. Check your ANTHROPIC_API_KEY in .env")
    except anthropic.RateLimitError:
        raise Exception("Rate limit hit. Too many requests — wait a moment and try again")
    except anthropic.APIConnectionError:
        raise Exception("Could not connect to Claude API. Check your internet connection")
    except anthropic.APIError as e:
        raise Exception(f"Claude API returned an error: {e.message}")

    raw_text = ""
    for block in response.content:
        if block.type == "text":
            raw_text = block.text

    if not raw_text:
        raise Exception("Claude responded but returned no text content")

    if not raw_text.endswith("}"):
        raise Exception(f"Prompt resulted in a cut off response. Raw response was: {raw_text[:300]}")
        
    return raw_text