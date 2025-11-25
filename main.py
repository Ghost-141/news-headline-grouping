import logging
from utils.helper import read_file, get_embedding, find_similarity_pair, group_data

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """
    Main function to run the news classification pipeline.

    Process:
    1. Read news data from JSON file
    2. Generate embeddings for news titles
    3. Find similar news pairs and group them
    4. Use Ollama LLM to create structured output with similar and unique articles
    """
    try:
        # Read news data
        logger.info("📰 Reading news data...")
        news_data, titles = read_file("db_data.json")
        logger.info(f"✔ Loaded {len(news_data)} news articles")

        # Generate embeddings
        logger.info("🔤 Generating embeddings...")
        embeddings = get_embedding(titles)
        logger.info(f"✔ Generated embeddings with shape: {embeddings.shape}")

        # Find similar pairs and group articles
        logger.info("🔍 Finding similar news pairs...")
        has_similarity, final_news = find_similarity_pair(embeddings, news_data)

        # Group data using Ollama
        grouped_result = group_data(has_similarity, final_news)

        # Save results
        logger.info("💾 Saving results...")
        with open("grouped_news.json", "w", encoding="utf8") as f:
            f.write(grouped_result)

        logger.info("✅ News classification completed successfully!")
        logger.info(f"📄 Results saved to: grouped_news.json")

    except FileNotFoundError:
        logger.error(
            "❌ Error: db_data.json file not found. Please ensure the file exists."
        )
    except Exception as e:
        logger.error(f"❌ Error occurred: {str(e)}")


if __name__ == "__main__":
    main()
