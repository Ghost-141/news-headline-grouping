import mysql.connector

conn = mysql.connector.connect(
    host="localhost", user="root", password="", database="news_update"
)
cursor = conn.cursor(dictionary=True)  # type: ignore


def save_to_db(source, title, link, publish_time):
    try:
        sql = """
        INSERT INTO news 
        (source, title, link, publish_time, is_breaking, pending, sent_status)
        VALUES (%s, %s, %s, %s, 0, 0, 0)
        """
        cursor.execute(sql, (source, title, link, publish_time))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.errors.IntegrityError:
        print(f"Already exists : {title}")
        return None
    except Exception as e:
        print(f"Error saving {title}: {e}")
        return None


def get_pending_breaking_news():
    """Fetch breaking news with pending and sent_status = 0"""
    try:
        sql = "SELECT id, title, link, source FROM news WHERE is_breaking = 1 AND sent_status = 0 AND DATE(created_at) = CURDATE()"
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


def save_breaking_news_to_queue(news_id, source, title, link, publish_time):
    """Save breaking news to queue table"""
    try:
        sql = """
        INSERT INTO breaking_news_queue 
        (news_id, source, title, link, publish_time)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (news_id, source, title, link, publish_time))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.errors.IntegrityError:
        print(f"Breaking news already in queue: {title}")
        return None
    except Exception as e:
        print(f"Error saving to queue {title}: {e}")
        return None


def get_unsent_breaking_news():
    """Fetch breaking news from queue that haven't been sent"""
    try:
        sql = """SELECT id, news_id, source, title, link, publish_time 
                 FROM breaking_news_queue 
                 WHERE sent_status = 0 AND DATE(created_at) = CURDATE()"""
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching breaking news queue: {e}")
        return []


def update_queue_sent_status(queue_ids):
    """Update sent_status for multiple queue IDs"""
    try:
        if not queue_ids:
            return True
        placeholders = ','.join(['%s'] * len(queue_ids))
        sql = f"UPDATE breaking_news_queue SET sent_status = 1 WHERE id IN ({placeholders})"
        cursor.execute(sql, tuple(queue_ids))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating queue sent status: {e}")
        return False
