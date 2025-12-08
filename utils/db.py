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
        print(f"Saved: {title} (Breaking: {is_breaking})")
        return cursor.lastrowid
    except mysql.connector.errors.IntegrityError:
        print(f"Already exists : {title}")
        return None
    except Exception as e:
        print(f"Error saving {title}: {e}")
        return None
