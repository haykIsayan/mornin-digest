
def build_prompt(topics: list[str]) -> str:
    if not topics:
        raise ValueError("Topics list cannot be empty")

    topics_str = ", ".join(topics)

#     prompt = f"""Search the web for the latest news articles on these topics: {topics_str}.

# For each topic find 2-3 recent articles. 
# Return ONLY a raw JSON object — no explanation, no markdown, no code fences.
# Use exactly this structure:

# {{
#   "articles": [
#     {{
#       "topic": "the topic this article relates to",
#       "title": "article title",
#       "summary": "2-3 sentence summary of the article",
#       "source": "publication name e.g. BBC, Reuters",
#       "url": "full article URL",
#       "published_date": "YYYY-MM-DD format, e.g. 2026-05-27"
#     }}
#   ]
# }}"""

    prompt = f"""Search the web for the latest news articles on these topics: {topics_str}.

For each topic find 2-3 recent articles.

CRITICAL INSTRUCTIONS:
- Your ENTIRE response must be a single valid JSON object
- Do NOT include any text before or after the JSON
- Do NOT include markdown code fences
- Do NOT narrate your search process

Use exactly this structure:

{{
  "articles": [
    {{
      "topic": "the topic this article relates to",
      "title": "article title",
      "summary": "2-3 sentence summary of the article",
      "source": "publication name e.g. BBC, Reuters",
      "url": "full article URL",
      "published_date": "YYYY-MM-DD format, e.g. 2026-05-27"
    }}
  ]
}}"""
    return prompt