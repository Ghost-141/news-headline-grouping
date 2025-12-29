import datetime
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from utils.db import get_unsent_breaking_news, update_queue_sent_status
from utils.send_message import send_whatsapp

device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer(
    "models/embedding_gemma", local_files_only=True, trust_remote_code=True
).to(device=device)


def get_embeddings(text_list):
    """Generate embeddings for text list"""
    embeddings = model.encode(
        text_list,
        show_progress_bar=False,
        prompt="task: sentence similarity | document: ",
    )
    return np.array(embeddings, dtype="float32")


def send_breaking_news():
    """Send breaking news with similarity-based deduplication"""
    breaking_news_list = get_unsent_breaking_news()

    if not breaking_news_list:
        print("No unsent breaking news found.")
        return

    print(f"Found {len(breaking_news_list)} unsent breaking news.")

    # Generate embeddings
    titles = [item["title"] for item in breaking_news_list]
    embeddings = get_embeddings(titles)

    # Compute similarity
    norm_embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    similarities = np.dot(norm_embeddings, norm_embeddings.T)

    # Group similar news
    grouped = []
    used = set()

    for i in range(len(breaking_news_list)):
        if i in used:
            continue
        group = [breaking_news_list[i]]
        used.add(i)

        for j in range(i + 1, len(breaking_news_list)):
            if j not in used and similarities[i][j] > 0.90:
                group.append(breaking_news_list[j])
                used.add(j)

        grouped.append(group)

    print(f"Grouped into {len(grouped)} unique news items.")

    # Send messages
    all_queue_ids = []

    for group in grouped:
        news = group[0]  # Send only the first one from each group
        news_data = {
            "title": news["title"],
            "source": news["source"],
            "link": news["link"],
            "publish_time": datetime.datetime.now().strftime("%I:%M:%S %p"),
        }

        if send_whatsapp(news_data):
            all_queue_ids.extend([item["id"] for item in group])
            print(f"✅ Sent: {news['title'][:40]}...")
            if len(group) > 1:
                print(f" (Grouped with {len(group)-1} similar news)")
                for similar in group[1:]:
                    print(f"  -{similar['title'][:60]}")
        else:
            print(f"❌ Failed to send: {news['title'][:50]}...")

    # Update sent status
    if all_queue_ids:
        if update_queue_sent_status(all_queue_ids):
            print(f"✅ Updated {len(all_queue_ids)} items as sent.")
        else:
            print(f"❌ Failed to update sent status.")
