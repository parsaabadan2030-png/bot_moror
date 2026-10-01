import sqlite3
from datetime import date, timedelta

DB_PATH = "data/study.db"

REVIEW_DAYS = [3, 7, 10, 21, 30, 40]


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            lesson TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lesson_id INTEGER NOT NULL,
            review_date TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            FOREIGN KEY (lesson_id) REFERENCES lessons(id)
        )
    """)

    conn.commit()
    conn.close()


def add_lesson(user_id, subject, lesson):
    today = date.today().isoformat()

    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO lessons (user_id, subject, lesson, created_at) VALUES (?, ?, ?, ?)",
        (user_id, subject, lesson, today)
    )

    lesson_id = cursor.lastrowid

    for days in REVIEW_DAYS:
        review_date = (date.today() + timedelta(days=days)).isoformat()
        conn.execute(
            "INSERT INTO reviews (lesson_id, review_date) VALUES (?, ?)",
            (lesson_id, review_date)
        )

    conn.commit()
    conn.close()


def get_today_reviews(user_id):
    today = date.today().isoformat()

    conn = get_connection()
    rows = conn.execute("""
        SELECT
            reviews.id AS review_id,
            lessons.id AS lesson_id,
            lessons.subject,
            lessons.lesson,
            reviews.review_date,
            reviews.completed
        FROM reviews
        JOIN lessons ON lessons.id = reviews.lesson_id
        WHERE lessons.user_id = ?
        AND reviews.review_date <= ?
        AND reviews.completed = 0
        ORDER BY reviews.review_date ASC
    """, (user_id, today)).fetchall()

    conn.close()
    return rows


def complete_review(review_id, user_id):
    conn = get_connection()

    conn.execute("""
        UPDATE reviews
        SET completed = 1
        WHERE id = ?
        AND lesson_id IN (
            SELECT id FROM lessons WHERE user_id = ?
        )
    """, (review_id, user_id))

    conn.commit()
    conn.close()