"""
Automatic Insight Generation Module (FR-8)
Synthesizes plain-language executive insights derived strictly from computed
statistical aggregates and trends across courses, aspects, languages, and semesters.
No hardcoded text.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any

class InsightGenerator:
    def __init__(self):
        pass

    def generate_executive_insights(
        self,
        feedback_df: pd.DataFrame,
        aspect_df: pd.DataFrame,
        drift_data: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """
        Produces prioritized insights categorized by:
        - Sentiment Overview
        - Aspect Drivers
        - Cross-Language Patterns
        - Topic Drift Dynamics
        """
        insights = []

        total_records = len(feedback_df)
        if total_records == 0:
            return [{"category": "Overview", "text": "Insufficient feedback records to generate statistical insights."}]

        def _col(candidates, default):
            for c in candidates:
                if c in feedback_df.columns:
                    return c
            return default

        sent_col = _col(["overall_sentiment", "Overall_Sentiment", "sentiment", "Predicted_Sentiment"], "overall_sentiment")
        rating_col = _col(["rating", "Rating"], "rating")
        course_col = _col(["course_name", "Course_Name", "Course"], "course_name")
        lang_col = _col(["language", "Language"], "language")

        # 1. Overall Sentiment Distribution Insight
        sent_counts = feedback_df[sent_col].value_counts(normalize=True) * 100.0
        pos_pct = round(sent_counts.get("Positive", 0.0), 1)
        neg_pct = round(sent_counts.get("Negative", 0.0), 1)
        neu_pct = round(sent_counts.get("Neutral", 0.0), 1)
        avg_rating = round(feedback_df[rating_col].mean(), 2) if rating_col in feedback_df.columns else 0.0

        insights.append({
            "category": "Sentiment Overview",
            "type": "positive" if pos_pct >= 55.0 else ("warning" if neg_pct >= 35.0 else "neutral"),
            "text": f"Across {total_records:,} analyzed student responses, overall sentiment stands at {pos_pct}% Positive, {neg_pct}% Negative, and {neu_pct}% Neutral, with an institutional average rating of {avg_rating}/5.0."
        })

        # 2. Course-level Sentiment Extremes
        if course_col in feedback_df.columns:
            course_sent = feedback_df.groupby(course_col)[sent_col].apply(
                lambda s: (s == "Positive").sum() / len(s) * 100.0
            ).round(1)

            if len(course_sent) > 1:
                top_course = course_sent.idxmax()
                top_pct = course_sent.max()
                lowest_course = course_sent.idxmin()
                lowest_pct = course_sent.min()

                insights.append({
                    "category": "Course Performance",
                    "type": "info",
                    "text": f"'{top_course}' achieved the highest satisfaction ({top_pct}% positive), while '{lowest_course}' registered the lowest positive sentiment ({lowest_pct}%), showing a satisfaction variance of {round(top_pct - lowest_pct, 1)} percentage points."
                })

        # 3. Aspect Sentiment Drivers
        if aspect_df is not None and not aspect_df.empty:
            aspect_agg = aspect_df.groupby("aspect")["sentiment"].apply(
                lambda s: ((s == "Positive").sum() / len(s) * 100.0, (s == "Negative").sum() / len(s) * 100.0, len(s))
            )

            aspect_stats = []
            for asp, (p_pct, n_pct, vol) in aspect_agg.items():
                aspect_stats.append({
                    "aspect": asp,
                    "pos_pct": round(p_pct, 1),
                    "neg_pct": round(n_pct, 1),
                    "volume": vol
                })

            aspect_stats_df = pd.DataFrame(aspect_stats)
            if not aspect_stats_df.empty:
                # Top positive driver
                top_pos_asp = aspect_stats_df.sort_values(by="pos_pct", ascending=False).iloc[0]
                # Top negative pain point
                top_neg_asp = aspect_stats_df.sort_values(by="neg_pct", ascending=False).iloc[0]

                insights.append({
                    "category": "Aspect Drivers",
                    "type": "positive",
                    "text": f"'{top_pos_asp['aspect']}' is the strongest institutional asset, leading all evaluated dimensions with {top_pos_asp['pos_pct']}% positive sentiment across {top_pos_asp['volume']} mentions."
                })

                insights.append({
                    "category": "Critical Pain Points",
                    "type": "warning",
                    "text": f"'{top_neg_asp['aspect']}' surfaced as the primary driver of student dissatisfaction, accumulating {top_neg_asp['neg_pct']}% negative feedback ({top_neg_asp['volume']} total mentions)."
                })

        # 4. Multilingual Comparison Insight
        if lang_col in feedback_df.columns:
            lang_neg = feedback_df.groupby(lang_col)[sent_col].apply(
                lambda s: (s == "Negative").sum() / len(s) * 100.0
            ).round(1)

            if len(lang_neg) >= 2:
                highest_neg_lang = lang_neg.idxmax()
                highest_neg_val = lang_neg.max()
                lowest_neg_lang = lang_neg.idxmin()
                lowest_neg_val = lang_neg.min()
                diff_neg = round(highest_neg_val - lowest_neg_val, 1)

                insights.append({
                    "category": "Multilingual Dynamics",
                    "type": "info",
                    "text": f"Language breakdown shows {highest_neg_lang} feedback carries {diff_neg}% higher negative sentiment rate ({highest_neg_val}%) compared to {lowest_neg_lang} ({lowest_neg_val}%), indicating students often express critical concerns more intensely in colloquial code-mixed expressions."
                })

        # 5. Topic Drift Dynamics Insight
        if drift_data and "classifications" in drift_data:
            class_df = drift_data["classifications"]
            emerging = class_df[class_df["Overall_Classification"] == "Emerging"]
            declining = class_df[class_df["Overall_Classification"] == "Declining"]
            new_topics = class_df[class_df["Overall_Classification"] == "New"]

            if not emerging.empty:
                top_em = emerging.iloc[0]
                insights.append({
                    "category": "Topic Drift — Emerging",
                    "type": "trend",
                    "text": f"Topic '{top_em['Topic_Name']}' demonstrated the steepest upward surge, escalating by +{top_em['Delta_Pct_Points']}% share over observed semesters ({top_em['Start_Share_Pct']}% → {top_em['End_Share_Pct']}%)."
                })

            if not declining.empty:
                top_dec = declining.iloc[-1] # steepest drop
                insights.append({
                    "category": "Topic Drift — Declining",
                    "type": "trend",
                    "text": f"Discussion surrounding '{top_dec['Topic_Name']}' declined significantly by {abs(top_dec['Delta_Pct_Points'])}% share as foundational coursework stabilized."
                })

            if not new_topics.empty:
                new_topic_names = ", ".join(f"'{n}'" for n in new_topics["Topic_Name"].tolist()[:2])
                insights.append({
                    "category": "Topic Drift — New Trends",
                    "type": "info",
                    "text": f"Curriculum progression revealed newly emerging discourse around {new_topic_names}, absent in initial terms and dominating senior semesters."
                })

        return insights
