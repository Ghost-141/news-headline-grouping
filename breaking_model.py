import json
import ollama
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

PROMPT_TEMPLATE = """
You are an expert news classifier.

From this news item, determine if it is **breaking/urgent news**. Include: accidents, crimes, political events, protests, deaths, arrests, fires, emergencies, or trending/hyped events.

Return a JSON object with the same fields, but only if it is breaking news. If the news is not breaking, return null.

JSON format (return exactly this, nothing else):
{{
  "id": <original_id>,
  "title": "<original_title>",
  "publish_time": "<original_publish_time>",
  "source": "<original_source>"
}}

News Item:
{news_item}

Return JSON object or null:
"""


def classify_breaking_news(
    input_file: str, output_file: str, model: str = "llama3.2:3b"
):
    logger.info(f"📰 Reading from {input_file}...")
    with open(input_file, "r", encoding="utf8") as f:
        news_data = json.load(f)

    results = []
    for idx, item in enumerate(news_data, 1):
        logger.info(f"🔄 Processing {idx}/{len(news_data)}: ID {item['id']}")

        # Prepare prompt for this single news item
        prompt = PROMPT_TEMPLATE.format(news_item=json.dumps(item, ensure_ascii=False))

        response = ollama.generate(model=model, prompt=prompt)

        response_text = response.get("response", "").strip()

        # Parse JSON safely
        import re

        match = re.search(r"(\{.*\}|null)", response_text, re.DOTALL)
        if match:
            try:
                parsed = json.loads(match.group(1))
                if parsed:  # Only include if breaking news (not null)
                    results.append(parsed)
            except json.JSONDecodeError:
                logger.warning(
                    f"⚠️ Failed to parse JSON for ID {item['id']}: {response_text}"
                )
        else:
            logger.warning(f"⚠️ No JSON object returned for ID {item['id']}")

    logger.info(f"💾 Saving {len(results)} breaking news items to {output_file}...")
    with open(output_file, "w", encoding="utf8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    logger.info("✅ Completed!")


if __name__ == "__main__":
    classify_breaking_news("news_2025-12-08_12:30:36.json", "breaking_news.json")
