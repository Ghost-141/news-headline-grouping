#!/usr/bin/env python3
"""
Database migration script to add created_at column
Run this once to update your existing database schema
"""

import mysql.connector
from datetime import datetime

def migrate_database():
    try:
        conn = mysql.connector.connect(
            host="localhost", 
            user="root", 
            password="", 
            database="news_update"
        )
        cursor = conn.cursor()
        
        # Check if created_at column exists
        cursor.execute("SHOW COLUMNS FROM news LIKE 'created_at'")
        if cursor.fetchone():
            print("✅ created_at column already exists")
            return
            
        # Add created_at column
        cursor.execute("ALTER TABLE news ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP")
        
        # Update existing records
        cursor.execute("UPDATE news SET created_at = NOW() WHERE created_at IS NULL")
        
        conn.commit()
        print("✅ Database migration completed successfully")
        print(f"✅ Added created_at column and set existing records to {current_date}")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    migrate_database()