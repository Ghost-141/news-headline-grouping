import mysql.connector

conn = mysql.connector.connect(
    host="localhost", user="root", password="", database="news_automation"
)
cursor = conn.cursor(dictionary=True)  # type: ignore


def save_to_db(source, title, summary, category, link, publish_time, is_breaking=0):
    try:
        sql = """
        INSERT INTO news 
        (source, title, summary, category, link, publish_time, is_breaking, sent_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 0)
        """
        cursor.execute(
            sql, (source, title, summary, category, link, publish_time, is_breaking)
        )
        conn.commit()
        print(f"Saved: {title} (Breaking: {True if is_breaking else False})")
        return cursor.lastrowid
    except mysql.connector.errors.IntegrityError:
        print(f"Already exists : {title}")
        return None
    except Exception as e:
        print(f"Error saving {title}: {e}")
        return None


def get_pending_breaking_news():
    """Fetch breaking news with sent_status = 0"""
    try:
        sql = "SELECT id, title, link, source FROM news WHERE is_breaking = 1 AND sent_status = 0"
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching breaking news: {e}")
        return []


def update_sent_status(news_id):
    """Update sent_status to 1 for given news_id"""
    try:
        sql = "UPDATE news SET sent_status = 1 WHERE id = %s"
        cursor.execute(sql, (news_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating sent status for ID {news_id}: {e}")
        return False
