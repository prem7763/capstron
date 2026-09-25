"""
FastAPI REST API Backend (server.py)
Powers the Modern Full-Stack Web Frontend for Multilingual Course Feedback Intelligence.
Provides complete CRUD (Add, Edit, Delete feedback), real-time NLP inference,
interactive analytics, and static file serving.
"""

import os
import sys
import json
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

# Backend NLP & Database modules
from src.database.db_manager import DatabaseManager
from src.preprocessing.cleaner import FeedbackCleaner
from src.language.detector import LanguageDetector
from src.language.normalizer import MultilingualNormalizer
from src.sentiment.classifier import SentimentClassifier
from src.aspect.aspect_sentiment import AspectSentimentExtractor
from src.drift.drift_analyzer import TopicDriftAnalyzer
from src.insights.generator import InsightGenerator

app = FastAPI(
    title="Multilingual Course Feedback Intelligence API",
    description="REST backend for aspect-based sentiment, topic modeling, and feedback management",
    version="2.0.0"
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize singletons
DB_PATH = "data/course_feedback.db"
db_manager = DatabaseManager(db_path=DB_PATH)
cleaner = FeedbackCleaner()
detector = LanguageDetector()
normalizer = MultilingualNormalizer()
sentiment_clf = SentimentClassifier(training_data_path="data/raw/course_feedback_raw.csv")
aspect_extractor = AspectSentimentExtractor()
drift_analyzer = TopicDriftAnalyzer()
insight_gen = InsightGenerator()

# ----------------- Pydantic Models -----------------
class NewFeedbackRequest(BaseModel):
    course_id: str
    course_name: str
    semester: str
    rating: int
    feedback_text: str
    student_id: Optional[str] = None

class LivePredictRequest(BaseModel):
    text: str

# ----------------- Helper Functions -----------------
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ----------------- API Endpoints -----------------

@app.get("/api/overview")
def get_overview():
    """Returns high-level institutional KPIs, distributions, and dynamic AI insights."""
    df = db_manager.query_complete_dataset()
    aspect_df = db_manager.query_aspects_data()
    drift_data = drift_analyzer.analyze_drift(df)
    insights = insight_gen.generate_executive_insights(df, aspect_df, drift_data)

    total_records = len(df)
    avg_rating = round(float(df["rating"].mean()), 2) if total_records > 0 else 0.0

    # Sentiment distribution
    sent_counts = df["overall_sentiment"].value_counts().to_dict()
    pos_count = sent_counts.get("Positive", 0)
    neg_count = sent_counts.get("Negative", 0)
    neu_count = sent_counts.get("Neutral", 0)

    # Language distribution
    lang_counts = df["language"].value_counts().to_dict()

    # Rating counts 1 to 5
    rating_counts = df["rating"].value_counts().sort_index().to_dict()
    formatted_ratings = {f"{k} Star": int(v) for k, v in rating_counts.items()}

    # Course satisfaction ranking
    course_agg = df.groupby(["course_id", "course_name"]).agg(
        total=("feedback_id", "count"),
        avg_rating=("rating", "mean"),
        pos=("overall_sentiment", lambda s: (s == "Positive").sum()),
        neg=("overall_sentiment", lambda s: (s == "Negative").sum())
    ).reset_index()

    course_agg["pos_rate"] = (course_agg["pos"] / course_agg["total"] * 100.0).round(1)
    course_agg["neg_rate"] = (course_agg["neg"] / course_agg["total"] * 100.0).round(1)
    course_agg["avg_rating"] = course_agg["avg_rating"].round(2)
    courses_leaderboard = course_agg.sort_values(by="pos_rate", ascending=False).to_dict(orient="records")

    return {
        "kpis": {
            "total_feedback": total_records,
            "avg_rating": avg_rating,
            "positive_count": pos_count,
            "positive_pct": round(pos_count / max(1, total_records) * 100.0, 1),
            "negative_count": neg_count,
            "negative_pct": round(neg_count / max(1, total_records) * 100.0, 1),
            "neutral_count": neu_count,
            "neutral_pct": round(neu_count / max(1, total_records) * 100.0, 1),
            "active_courses": df["course_id"].nunique(),
            "active_languages": df["language"].nunique()
        },
        "insights": insights,
        "sentiment_distribution": {
            "Positive": pos_count,
            "Negative": neg_count,
            "Neutral": neu_count
        },
        "language_distribution": lang_counts,
        "rating_distribution": formatted_ratings,
        "courses_leaderboard": courses_leaderboard
    }

@app.get("/api/aspects")
def get_aspects_breakdown():
    """Returns granular 12-aspect sentiment statistics and course heatmap matrix."""
    aspect_df = db_manager.query_aspects_data()

    if aspect_df.empty:
        return {"aspects": [], "heatmap": {}, "strengths": [], "pain_points": []}

    asp_agg = aspect_df.groupby("aspect").agg(
        total=("aspect_id", "count"),
        positive=("sentiment", lambda s: (s == "Positive").sum()),
        negative=("sentiment", lambda s: (s == "Negative").sum()),
        neutral=("sentiment", lambda s: (s == "Neutral").sum())
    ).reset_index()

    asp_agg["pos_rate"] = (asp_agg["positive"] / asp_agg["total"] * 100.0).round(1)
    asp_agg["neg_rate"] = (asp_agg["negative"] / asp_agg["total"] * 100.0).round(1)
    asp_agg["net_score"] = (asp_agg["pos_rate"] - asp_agg["neg_rate"]).round(1)
    asp_agg = asp_agg.sort_values(by="net_score", ascending=False)

    strengths = asp_agg.head(3).to_dict(orient="records")
    pain_points = asp_agg.sort_values(by="neg_rate", ascending=False).head(3).to_dict(orient="records")

    # Heatmap matrix: Course x Aspect Net Score
    course_asp = aspect_df.groupby(["course_name", "aspect"])["sentiment"].apply(
        lambda s: (s == "Positive").sum() / len(s) * 100.0 - (s == "Negative").sum() / len(s) * 100.0
    ).unstack(fill_value=0.0).round(1)

    heatmap_data = {
        "courses": course_asp.index.tolist(),
        "aspects": course_asp.columns.tolist(),
        "matrix": course_asp.values.tolist()
    }

    return {
        "aspects_summary": asp_agg.to_dict(orient="records"),
        "strengths": strengths,
        "pain_points": pain_points,
        "heatmap": heatmap_data
    }

@app.get("/api/drift")
def get_topic_drift():
    """Returns temporal topic frequencies across semesters with trajectory statuses."""
    df = db_manager.query_complete_dataset()
    drift_data = drift_analyzer.analyze_drift(df)

    props_matrix = drift_data["proportions_matrix"]
    class_df = drift_data["classifications"]

    # Transform props matrix to chartable series
    semesters = drift_data["semester_order"]
    chart_series = []
    for topic, row in props_matrix.iterrows():
        chart_series.append({
            "topic_name": topic,
            "data": [float(row[sem]) for sem in semesters]
        })

    return {
        "semesters": semesters,
        "chart_series": chart_series,
        "classifications": class_df.to_dict(orient="records")
    }

@app.get("/api/feedback")
def get_feedback_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    course: Optional[str] = None,
    semester: Optional[str] = None,
    language: Optional[str] = None,
    sentiment: Optional[str] = None,
    aspect: Optional[str] = None,
    search: Optional[str] = None
):
    """Returns filtered, searchable, and paginated student feedback records with aspects."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        base_query = """
            SELECT DISTINCT
                f.feedback_id, f.student_id, f.course_id, f.course_name,
                f.semester, f.date, f.language, f.rating, f.feedback_text,
                s.sentiment as overall_sentiment, s.confidence as sentiment_confidence,
                t.topic_name
            FROM Feedback f
            LEFT JOIN Sentiment s ON f.feedback_id = s.feedback_id
            LEFT JOIN Topic t ON f.feedback_id = t.feedback_id
            LEFT JOIN Aspect a ON f.feedback_id = a.feedback_id
            WHERE 1=1
        """
        params = []

        if course and course != "All":
            base_query += " AND f.course_name = ?"
            params.append(course)
        if semester and semester != "All":
            base_query += " AND f.semester = ?"
            params.append(semester)
        if language and language != "All":
            base_query += " AND f.language = ?"
            params.append(language)
        if sentiment and sentiment != "All":
            base_query += " AND s.sentiment = ?"
            params.append(sentiment)
        if aspect and aspect != "All":
            base_query += " AND a.aspect = ?"
            params.append(aspect)
        if search and search.strip():
            base_query += " AND (f.feedback_text LIKE ? OR f.course_name LIKE ?)"
            term = f"%{search.strip()}%"
            params.extend([term, term])

        # Get total matching count
        count_query = f"SELECT COUNT(*) FROM ({base_query})"
        cursor.execute(count_query, params)
        total_count = cursor.fetchone()[0]

        # Add pagination
        base_query += " ORDER BY f.date DESC, f.feedback_id DESC LIMIT ? OFFSET ?"
        params.extend([page_size, (page - 1) * page_size])

        cursor.execute(base_query, params)
        rows = [dict(r) for r in cursor.fetchall()]

        # Attach aspects to each record
        if rows:
            ids = [r["feedback_id"] for r in rows]
            placeholders = ",".join(["?"] * len(ids))
            asp_query = f"SELECT feedback_id, aspect, sentiment, confidence, evidence_snippet FROM Aspect WHERE feedback_id IN ({placeholders})"
            cursor.execute(asp_query, ids)
            aspects_rows = cursor.fetchall()
            aspects_by_id = {}
            for ar in aspects_rows:
                f_id = ar["feedback_id"]
                if f_id not in aspects_by_id:
                    aspects_by_id[f_id] = []
                aspects_by_id[f_id].append({
                    "aspect": ar["aspect"],
                    "sentiment": ar["sentiment"],
                    "confidence": ar["confidence"],
                    "evidence_snippet": ar["evidence_snippet"]
                })

            for r in rows:
                r["aspects"] = aspects_by_id.get(r["feedback_id"], [])

        return {
            "total_count": total_count,
            "page": page,
            "page_size": page_size,
            "total_pages": max(1, (total_count - 1) // page_size + 1),
            "records": rows
        }

@app.post("/api/feedback")
def add_new_feedback(req: NewFeedbackRequest):
    """
    INTERACTIVE CRUD: Adds a new student feedback record.
    Runs full real-time NLP analysis (language detection, sentiment, 12-aspect ABSA, topic)
    and persists directly into the SQLite database.
    """
    raw_text = req.feedback_text.strip()
    if not raw_text:
        raise HTTPException(status_code=400, detail="Feedback text cannot be empty.")

    # 1. Clean Text
    cleaned = cleaner.clean_text(raw_text)

    # 2. Detect Language
    lang_info = detector.detect_language(raw_text)
    detected_lang = lang_info["language"]

    # 3. Overall Sentiment
    sent_info = sentiment_clf.predict(raw_text)
    overall_sent = sent_info["sentiment"]
    overall_conf = sent_info["confidence"]
    polarity = sent_info["score"]

    # 4. Aspect-Based Sentiment Analysis (12 Dimensions)
    detected_aspects = aspect_extractor.analyze_aspects(raw_text)

    # 5. Generate IDs
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Feedback")
        cnt = cursor.fetchone()[0] + 1
        new_id = f"FB_USER_{cnt:05d}"
        student_id = req.student_id or f"STU_USER_{cnt:04d}"
        today_str = datetime.now().strftime("%Y-%m-%d")

        # 6. Insert Feedback
        cursor.execute("""
            INSERT INTO Feedback (feedback_id, student_id, course_id, course_name, semester, date, language, rating, feedback_text, cleaned_text)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (new_id, student_id, req.course_id, req.course_name, req.semester, today_str, detected_lang, req.rating, raw_text, cleaned))

        # 7. Insert Sentiment
        cursor.execute("""
            INSERT INTO Sentiment (feedback_id, sentiment, confidence, polarity_score)
            VALUES (?, ?, ?, ?)
        """, (new_id, overall_sent, overall_conf, polarity))

        # 8. Insert Aspects
        for asp in detected_aspects:
            cursor.execute("""
                INSERT INTO Aspect (feedback_id, aspect, sentiment, confidence, evidence_snippet)
                VALUES (?, ?, ?, ?, ?)
            """, (new_id, asp["aspect"], asp["sentiment"], asp["confidence"], asp["evidence_snippet"]))

        # 9. Assign Topic
        topic_name = "User Submitted Feedback"
        if detected_aspects:
            topic_name = f"{detected_aspects[0]['aspect']} Discussion"
        cursor.execute("""
            INSERT INTO Topic (feedback_id, topic_id, topic_name, probability)
            VALUES (?, ?, ?, ?)
        """, (new_id, 99, topic_name, 0.95))

        conn.commit()

    return {
        "status": "success",
        "message": "Feedback added and analyzed successfully!",
        "record": {
            "feedback_id": new_id,
            "student_id": student_id,
            "course_name": req.course_name,
            "semester": req.semester,
            "rating": req.rating,
            "language": detected_lang,
            "overall_sentiment": overall_sent,
            "sentiment_confidence": overall_conf,
            "aspects_count": len(detected_aspects),
            "aspects": detected_aspects
        }
    }

@app.delete("/api/feedback/{feedback_id}")
def delete_feedback(feedback_id: str):
    """INTERACTIVE CRUD: Deletes a feedback record from the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT feedback_id FROM Feedback WHERE feedback_id = ?", (feedback_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Feedback record not found.")

        cursor.execute("DELETE FROM Aspect WHERE feedback_id = ?", (feedback_id,))
        cursor.execute("DELETE FROM Sentiment WHERE feedback_id = ?", (feedback_id,))
        cursor.execute("DELETE FROM Topic WHERE feedback_id = ?", (feedback_id,))
        cursor.execute("DELETE FROM Feedback WHERE feedback_id = ?", (feedback_id,))
        conn.commit()

    return {"status": "success", "message": f"Feedback {feedback_id} deleted successfully."}

@app.post("/api/predict")
def live_predict(req: LivePredictRequest):
    """Real-time live NLP inference for the interactive sandbox playground."""
    text = req.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    lang_res = detector.detect_language(text)
    norm_text = normalizer.translate_to_english_pipeline_a(text, lang_res["language"])
    sent_res = sentiment_clf.predict(text)
    aspects = aspect_extractor.analyze_aspects(text)

    return {
        "input_text": text,
        "language": lang_res,
        "pipeline_a_translation": norm_text,
        "sentiment": sent_res,
        "aspects": aspects
    }

@app.get("/api/download/pdf/{lang}")
def download_viva_pdf(lang: str):
    """Direct PDF download endpoint for Viva Documentation."""
    filename = "Multilingual_Course_Feedback_Intelligence_Viva_Guide_English.pdf" if lang.lower() == "english" else "Multilingual_Course_Feedback_Intelligence_Viva_Guide.pdf"
    if os.path.exists(filename):
        return FileResponse(
            filename,
            media_type="application/pdf",
            filename=filename
        )
    else:
        raise HTTPException(status_code=404, detail="PDF guide not found.")

# ----------------- Mount Static Frontend -----------------
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 70)
    print("LAUNCHING FULL-STACK FASTAPI BACKEND SERVER")
    print("Web Frontend: http://127.0.0.1:8000")
    print("Swagger Docs: http://127.0.0.1:8000/docs")
    print("=" * 70)
    uvicorn.run(app, host="127.0.0.1", port=8000)
