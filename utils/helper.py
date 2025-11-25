import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer
import random
import ollama
import logging
from prompts.prompt_v2 import prompt

logger = logging.getLogger(__name__)


MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
LOCAL_DIR = "./models/all-mpnet-base-v2"


def read_file(file_path):
    """
    Read news data from JSON file and extract titles.

    Args:
        file_path (str): Path to the JSON file containing news data

    Returns:
        tuple: (news_data, titles) - Complete news data and list of titles
    """
    with open(file_path, "r", encoding="utf8") as f:
        news_data = json.load(f)

    titles = [item["title"] for item in news_data]

    return news_data, titles


def get_model():
    """
    Ensures the model is available locally, then loads it.
    """
    if not os.path.exists(LOCAL_DIR) or not os.listdir(LOCAL_DIR):
        logger.info("Downloading {MODEL_NAME} model from HF...")
        model = SentenceTransformer(MODEL_NAME)
        model.save(LOCAL_DIR)
    else:
        logger.info(f"Loading {MODEL_NAME} model from local directory...")
        model = SentenceTransformer(LOCAL_DIR)
        # logger.info("✔ Model loaded successfully!")
    return model


def get_embedding(titles):
    """
    Generate embeddings for news titles using sentence transformer model.

    Args:
        titles (list): List of news titles

    Returns:
        np.ndarray: Normalized embeddings for the titles
    """
    model = get_model()
    embeddings = model.encode(titles, normalize_embeddings=True).astype("float32")
    return embeddings


def find_similarity_pair(embeddings, news_data):
    """
    Find similar news pairs based on embedding similarity and group them together.

    Args:
        embeddings (np.ndarray): News title embeddings
        news_data (list): Complete news data with metadata

    Returns:
        tuple: (has_similarity, final_news) - Boolean indicating similarity found and processed news list
    """
    # Find similar pairs directly
    similarity_threshold = 0.8
    similar_pairs = []

    for i in range(len(embeddings)):
        for j in range(i + 1, len(embeddings)):
            similarity_score = np.dot(embeddings[i], embeddings[j])
            if similarity_score > similarity_threshold:
                similar_pairs.append((i, j, similarity_score))

    if similar_pairs:
        # Group similar articles together
        used_indices = set()
        final_news = []

        # Add similar pairs first
        for i, j, sim in sorted(similar_pairs, key=lambda x: x[2], reverse=True):
            if i not in used_indices:
                final_news.append(news_data[i])
                used_indices.add(i)
            if j not in used_indices:
                final_news.append(news_data[j])
                used_indices.add(j)

        # Add remaining articles
        for i, article in enumerate(news_data):
            if i not in used_indices:
                final_news.append(article)

        final_news = final_news[:10]
        logger.info("Found similar news - grouping together...")
        return True, final_news
    else:
        final_news = news_data.copy()
        random.shuffle(final_news)
        logger.info("No similar news found")
        return False, final_news


def group_data(similarity: bool, final_news: list):
    """
    Group similar news articles using Ollama LLM and return structured JSON output.

    Args:
        similarity (bool): Whether similar articles were found
        final_news (list): List of news articles to group

    Returns:
        str: JSON formatted response from Ollama with grouped similar and unique articles
    """
    from prompts.prompt_v1 import json_template

    simple_news = [{"id": item["id"], "title": item["title"]} for item in final_news]
    news_text = json.dumps(simple_news, ensure_ascii=False, indent=2)

    full_prompt = prompt.format(json_template=json_template, news_text=news_text)

    if similarity:
        response = ollama.generate(model="llama3.2:3b", prompt=full_prompt)
        logger.info("Genearing Response from Ollama")
        return response["response"]

    else:
        return news_text
