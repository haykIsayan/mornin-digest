import json
from .prompt_builder import build_prompt
from .prompt_runner import run_prompt

class ArticlesFetcher:
    def fetch_articles(self, topics: list[str]) -> dict:
        prompt = build_prompt(topics)
        raw_text = run_prompt(prompt)
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            raise Exception(
                f"Prompt resulted in an invalid JSON. Raw response was: {raw_text[:300]}"
            )