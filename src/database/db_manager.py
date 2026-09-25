"""
Database Persistence & Storage Module (Section 9)
Manages SQLite storage for:
- Feedback table
- Sentiment table
- Aspect table (1-to-many relationship)
- Topic table
Provides indexed, optimized query functions for the Streamlit dashboard views.
"""

import os
import sqlite3
import pandas as pd
from typing import Dict, Any, List, Optional

class DatabaseManager:
    def __init__(self, db_path: str = "data/course_feedback.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_schema()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_schema(self):
        """Initializes tables and indexes according to PRD Section 9."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 1. Feedback Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Feedback (
                    feedback_id TEXT PRIMARY KEY,
                    student_id TEXT NOT NULL,
                    course_id TEXT NOT NULL,
                    course_name TEXT NOT NULL,
                    semester TEXT NOT NULL,
                    date TEXT NOT NULL,
                    language TEXT NOT NULL,
                    rating INTEGER NOT NULL,
                    feedback_text TEXT NOT NULL,
                    cleaned_text TEXT NOT NULL
                )
            """)

            # 2. Sentiment Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Sentiment (
                    feedback_id TEXT PRIMARY KEY,
                    sentiment TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    polarity_score REAL NOT NULL,
                    FOREIGN KEY (feedback_id) REFERENCES Feedback (feedback_id) ON DELETE CASCADE
                )
            """)

            # 3. Aspect Table (One-to-many)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Aspect (
                    aspect_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    feedback_id TEXT NOT NULL,
                    aspect TEXT NOT NULL,
                    sentiment TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    evidence_snippet TEXT,
                    FOREIGN KEY (feedback_id) REFERENCES Feedback (feedback_id) ON DELETE CASCADE
                )
            """)

            # 4. Topic Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Topic (
                    feedback_id TEXT PRIMARY KEY,
                    topic_id INTEGER NOT NULL,
                    topic_name TEXT NOT NULL,
                    probability REAL NOT NULL,
                    FOREIGN KEY (feedback_id) REFERENCES Feedback (feedback_id) ON DELETE CASCADE
                )
            """)

            # Performance Indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_feedback_course ON Feedback(course_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_feedback_sem ON Feedback(semester)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_feedback_lang ON Feedback(language)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_sentiment_val ON Sentiment(sentiment)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_aspect_name ON Aspect(aspect)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_aspect_sent ON Aspect(sentiment)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_topic_name ON Topic(topic_name)")

            conn.commit()

    def store_pipeline_results(
        self,
        feedback_df: pd.DataFrame,
        sentiment_df: pd.DataFrame,
        aspect_records: List[Dict[str, Any]],
        topic_df: pd.DataFrame
    ):
        """Bulk persists all pipeline stages into the normalized database."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Clean existing records
            cursor.execute("DELETE FROM Aspect")
            cursor.execute("DELETE FROM Topic")
            cursor.execute("DELETE FROM Sentiment")
            cursor.execute("DELETE FROM Feedback")

            # 1. Insert Feedback
            feedback_df.to_sql("Feedback", conn, if_exists="append", index=False)

            # 2. Insert Sentiment
            sentiment_df.to_sql("Sentiment", conn, if_exists="append", index=False)

            # 3. Insert Aspect records
            aspect_df = pd.DataFrame(aspect_records)
            if not aspect_df.empty:
                aspect_df.to_sql("Aspect", conn, if_exists="append", index=False)

            # 4. Insert Topics
            topic_df.to_sql("Topic", conn, if_exists="append", index=False)

            conn.commit()
            print(f"Successfully populated SQLite database at {self.db_path}")

    def query_overview_metrics(self) -> Dict[str, Any]:
        """Queries high-level KPIs for Overview Dashboard."""
        with self.get_connection() as conn:
            total_records = conn.execute("SELECT COUNT(*) FROM Feedback").fetchone()[0]
            avg_rating = conn.execute("SELECT AVG(rating) FROM Feedback").fetchone()[0] or 0.0
            num_courses = conn.execute("SELECT COUNT(DISTINCT course_id) FROM Feedback").fetchone()[0]
            num_languages = conn.execute("SELECT COUNT(DISTINCT language) FROM Feedback").fetchone()[0]

            sentiment_counts = pd.read_sql_query(
                "SELECT sentiment, COUNT(*) as count FROM Sentiment GROUP BY sentiment", conn
            )
            total_sent = sentiment_counts["count"].sum() or 1
            sent_dist = {
                row["sentiment"]: round(row["count"] / total_sent * 100.0, 1)
                for _, row in sentiment_counts.iterrows()
            }

            return {
                "total_records": total_records,
                "avg_rating": round(float(avg_rating), 2),
                "num_courses": num_courses,
                "num_languages": num_languages,
                "sentiment_distribution": sent_dist
            }

    def query_complete_dataset(self) -> pd.DataFrame:
        """Loads unified feedback, sentiment, and primary topic representation for rapid dashboard filtering."""
        query = """
            SELECT 
                f.feedback_id, f.student_id, f.course_id, f.course_name,
                f.semester, f.date, f.language, f.rating, f.feedback_text, f.cleaned_text,
                s.sentiment as overall_sentiment, s.confidence as sentiment_confidence, s.polarity_score,
                t.topic_id, t.topic_name, t.probability as topic_probability
            FROM Feedback f
            LEFT JOIN Sentiment s ON f.feedback_id = s.feedback_id
            LEFT JOIN Topic t ON f.feedback_id = t.feedback_id
        """
        with self.get_connection() as conn:
            df = pd.read_sql_query(query, conn)
        return df

    def query_aspects_data(self) -> pd.DataFrame:
        """Loads all aspect extractions joined with feedback metadata."""
        query = """
            SELECT 
                a.aspect_id, a.feedback_id, a.aspect, a.sentiment, a.confidence, a.evidence_snippet,
                f.course_id, f.course_name, f.semester, f.language, f.rating
            FROM Aspect a
            JOIN Feedback f ON a.feedback_id = f.feedback_id
        """
        with self.get_connection() as conn:
            df = pd.read_sql_query(query, conn)
        return df
