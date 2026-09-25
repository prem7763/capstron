"""
Complete End-to-End Execution Pipeline (run_pipeline.py)
Executes:
1. Synthetic Multilingual Data Generation (English, Hindi, Hinglish)
2. Preprocessing & Negation-Preserving Cleaning
3. Trilingual Language Detection
4. Sentiment Analysis with Confidence Scores
5. 12-Aspect ABSA & Clause Extraction
6. Semantic Topic Modeling with c-TF-IDF & Human-Readable Labels
7. Topic Drift Classification Across Semesters
8. Dynamic Insight Generation
9. Normalized SQLite Database Persistence
"""

import os
import sys
import json
import time
import pandas as pd
from datetime import datetime

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from src.data_generation.generate_synthetic import generate_dataset
from src.preprocessing.cleaner import FeedbackCleaner
from src.language.detector import LanguageDetector
from src.sentiment.classifier import SentimentClassifier
from src.aspect.aspect_sentiment import AspectSentimentExtractor
from src.topic.bertopic_engine import SemanticTopicEngine
from src.drift.drift_analyzer import TopicDriftAnalyzer
from src.insights.generator import InsightGenerator
from src.database.db_manager import DatabaseManager

def main():
    print("=" * 70)
    print("🚀 STARTING MULTILINGUAL COURSE FEEDBACK INTELLIGENCE PIPELINE")
    print("=" * 70)
    t0 = time.time()

    raw_path = "data/raw/course_feedback_raw.csv"
    processed_path = "data/processed/course_feedback_processed.csv"
    db_path = "data/course_feedback.db"

    # Step 1: Generate Raw Benchmark Dataset
    print("\n[Phase 1] Ingesting / Generating Synthetic Multilingual Dataset...")
    if not os.path.exists(raw_path):
        raw_df = generate_dataset(num_records=2200, output_path=raw_path)
    else:
        raw_df = pd.read_csv(raw_path)
        print(f"Loaded existing raw dataset with {len(raw_df)} records.")

    # Step 2: Preprocessing & Negation Preservation
    print("\n[Phase 2] Preprocessing & Cleaning (Negation Preservation)...")
    cleaner = FeedbackCleaner(min_char_length=6)
    cleaned_df = cleaner.clean_dataframe(raw_df, text_col="Feedback_Text")

    # Step 3: Trilingual Language Detection
    print("\n[Phase 3] Language Detection (English, Hindi, Hinglish)...")
    detector = LanguageDetector()
    cleaned_df = detector.process_dataframe(cleaned_df, text_col="Feedback_Text", out_col="Detected_Language")
    print("Detected Languages:")
    for lang, count in cleaned_df["Detected_Language"].value_counts().items():
        print(f"  - {lang}: {count} records ({round(count / len(cleaned_df) * 100, 1)}%)")

    # Step 4: Overall Sentiment Classification
    print("\n[Phase 4] Sentiment Classification & Polarity Scoring...")
    sentiment_clf = SentimentClassifier()
    sentiment_results = [sentiment_clf.predict(t) for t in cleaned_df["Cleaned_Text"]]
    
    cleaned_df["Predicted_Sentiment"] = [r["sentiment"] for r in sentiment_results]
    cleaned_df["Sentiment_Confidence"] = [r["confidence"] for r in sentiment_results]
    cleaned_df["Polarity_Score"] = [r["score"] for r in sentiment_results]

    print("Predicted Sentiments:")
    for sent, count in cleaned_df["Predicted_Sentiment"].value_counts().items():
        print(f"  - {sent}: {count} records ({round(count / len(cleaned_df) * 100, 1)}%)")

    # Step 5: Aspect-Based Sentiment Analysis (12 Aspects)
    print("\n[Phase 5] Aspect-Based Sentiment Analysis (ABSA)...")
    absa_extractor = AspectSentimentExtractor()
    all_aspect_records = []
    
    for _, row in cleaned_df.iterrows():
        fb_id = row["Feedback_ID"]
        aspects_found = absa_extractor.analyze_aspects(row["Feedback_Text"])
        for asp in aspects_found:
            all_aspect_records.append({
                "feedback_id": fb_id,
                "aspect": asp["aspect"],
                "sentiment": asp["sentiment"],
                "confidence": asp["confidence"],
                "evidence_snippet": asp["evidence_snippet"]
            })

    aspects_df = pd.DataFrame(all_aspect_records)
    print(f"Extracted {len(aspects_df)} aspect mentions across 12 course dimensions.")
    print("Top 5 Mentioned Aspects:")
    for asp, count in aspects_df["aspect"].value_counts().head(5).items():
        print(f"  - {asp}: {count} mentions")

    # Step 6: Semantic Topic Modeling
    print("\n[Phase 6] Semantic Topic Modeling (c-TF-IDF & Naming)...")
    topic_engine = SemanticTopicEngine(num_topics=8, random_state=42)
    topic_labels, topic_probs = topic_engine.fit_transform(cleaned_df["Cleaned_Text"].tolist())
    
    cleaned_df["Topic_ID"] = topic_labels
    cleaned_df["Topic_Name"] = [topic_engine.topic_names[t_id] for t_id in topic_labels]
    cleaned_df["Topic_Probability"] = [round(float(p), 2) for p in topic_probs]

    print("Discovered Topics:")
    topic_summary = topic_engine.get_topic_info()
    for _, row in topic_summary.iterrows():
        print(f"  - [{row['Topic_ID']}] {row['Topic_Name']} ({row['Count']} records) | Top: {row['Top_Keywords']}")

    # Step 7: Topic Drift Analytics
    print("\n[Phase 7] Topic Drift Analysis Across Semesters...")
    drift_analyzer = TopicDriftAnalyzer()
    drift_results = drift_analyzer.analyze_drift(cleaned_df)
    class_df = drift_results["classifications"]
    print("Topic Drift Trajectories:")
    for _, row in class_df.iterrows():
        print(f"  - {row['Topic_Name']}: {row['Overall_Classification']} (Start: {row['Start_Share_Pct']}%, End: {row['End_Share_Pct']}%, Delta: {row['Delta_Pct_Points']}%)")

    # Step 8: Dynamic Insight Generation
    print("\n[Phase 8] Generating Non-Hardcoded Statistical Insights...")
    insight_gen = InsightGenerator()
    insights = insight_gen.generate_executive_insights(cleaned_df, aspects_df, drift_results)
    for ins in insights:
        print(f"  [{ins['category']}] {ins['text']}")

    # Step 9: SQLite Database Persistence
    print("\n[Phase 9] Persisting to SQLite Database...")
    db_manager = DatabaseManager(db_path=db_path)

    # Format feedback table
    feedback_table = cleaned_df[[
        "Feedback_ID", "Student_ID", "Course_ID", "Course_Name",
        "Semester", "Date", "Language", "Rating", "Feedback_Text", "Cleaned_Text"
    ]].rename(columns={
        "Feedback_ID": "feedback_id",
        "Student_ID": "student_id",
        "Course_ID": "course_id",
        "Course_Name": "course_name",
        "Semester": "semester",
        "Date": "date",
        "Language": "language",
        "Rating": "rating",
        "Feedback_Text": "feedback_text",
        "Cleaned_Text": "cleaned_text"
    })

    # Format sentiment table
    sentiment_table = pd.DataFrame({
        "feedback_id": cleaned_df["Feedback_ID"],
        "sentiment": cleaned_df["Predicted_Sentiment"],
        "confidence": cleaned_df["Sentiment_Confidence"],
        "polarity_score": cleaned_df["Polarity_Score"]
    })

    # Format topic table
    topic_table = pd.DataFrame({
        "feedback_id": cleaned_df["Feedback_ID"],
        "topic_id": cleaned_df["Topic_ID"],
        "topic_name": cleaned_df["Topic_Name"],
        "probability": cleaned_df["Topic_Probability"]
    })

    db_manager.store_pipeline_results(feedback_table, sentiment_table, all_aspect_records, topic_table)

    # Save processed CSV
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    cleaned_df.to_csv(processed_path, index=False, encoding="utf-8")
    print(f"Saved processed dataset to {processed_path}")

    elapsed = round(time.time() - t0, 2)
    print("\n" + "=" * 70)
    print(f"✅ PIPELINE COMPLETED SUCCESSFULLY IN {elapsed}s")
    print("=" * 70)

if __name__ == "__main__":
    main()
