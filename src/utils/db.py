import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

def test_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO meetings (title, start_time, attendees) VALUES ('Test Meeting', '2025-03-01 10:00:00', ARRAY['user@example.com']) RETURNING id;")
    meeting_id = cur.fetchone()[0]
    conn.commit()
    print(f"Inserted meeting with ID: {meeting_id}")
    cur.close()
    conn.close()

if __name__ == "__main__":
    test_db()