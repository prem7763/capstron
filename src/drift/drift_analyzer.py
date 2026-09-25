"""
Topic Drift Analyzer (FR-7)
Computes temporal topic distributions across semesters and academic periods.
Classifies each topic as:
- 'Emerging': Significant increase (> 25% share gain)
- 'Declining': Significant decrease (> 25% share loss)
- 'Persistent': Stable, sustained volume across semesters
- 'New': Topic appearing newly in a semester with zero presence prior
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List

class TopicDriftAnalyzer:
    def __init__(self, time_col: str = "Semester", topic_col: str = "Topic_Name"):
        self.time_col = time_col
        self.topic_col = topic_col

    def _resolve_col(self, df: pd.DataFrame, candidates: List[str]) -> str:
        for c in candidates:
            if c in df.columns:
                return c
        return candidates[0]

    def analyze_drift(self, df: pd.DataFrame, semester_order: List[str] = None) -> Dict[str, Any]:
        """
        Analyzes topic frequency and proportions across ordered semesters.
        Returns:
        - temporal_matrix: raw count and percentage per semester
        - classifications: Emerging / Declining / Persistent / New per topic and period
        - drift_summary: key trends and insights
        """
        time_col = self._resolve_col(df, [self.time_col, self.time_col.lower(), "semester", "Semester"])
        topic_col = self._resolve_col(df, [self.topic_col, self.topic_col.lower(), "topic_name", "Topic_Name"])

        if semester_order is None:
            # Try to order chronologically if standard names
            unique_sems = df[time_col].dropna().unique().tolist()
            try:
                semester_order = sorted(unique_sems, key=lambda s: int(s.replace("Sem ", "")))
            except Exception:
                semester_order = sorted(unique_sems)

        # Cross tabulation of topic vs semester
        ct_counts = pd.crosstab(df[topic_col], df[time_col])
        ct_counts.index.name = "Topic_Name"
        
        # Ensure all semesters exist in columns
        for sem in semester_order:
            if sem not in ct_counts.columns:
                ct_counts[sem] = 0
        ct_counts = ct_counts[semester_order]

        # Calculate proportions per semester (column percentage)
        sem_totals = ct_counts.sum(axis=0)
        ct_proportions = ct_counts.div(sem_totals.replace(0, 1), axis=1) * 100.0
        ct_proportions.index.name = "Topic_Name"

        # Classify each topic over time
        classifications = []
        topics = ct_counts.index.tolist()

        for topic in topics:
            props = ct_proportions.loc[topic].values
            counts = ct_counts.loc[topic].values

            # Classify overall trajectory
            # Compare first half vs second half or consecutive periods
            first_period_prop = props[0]
            last_period_prop = props[-1]

            mean_prop = np.mean(props)
            std_prop = np.std(props)
            cv = (std_prop / (mean_prop + 1e-6)) # Coefficient of variation

            # Consecutive transitions
            period_status = {}
            for i in range(len(semester_order)):
                curr_sem = semester_order[i]
                curr_p = props[i]
                
                if i == 0:
                    status = "Baseline"
                else:
                    prev_p = props[i - 1]
                    if prev_p == 0 and curr_p > 0:
                        status = "New"
                    elif prev_p > 0 and (curr_p - prev_p) / prev_p >= 0.25:
                        status = "Emerging"
                    elif prev_p > 0 and (prev_p - curr_p) / prev_p >= 0.25:
                        status = "Declining"
                    else:
                        status = "Persistent"
                period_status[curr_sem] = status

            # Overall trajectory category
            if first_period_prop == 0 and last_period_prop > 2.0:
                overall_status = "New"
            elif (last_period_prop - first_period_prop) >= 4.0 or (first_period_prop > 0 and (last_period_prop - first_period_prop) / first_period_prop >= 0.40):
                overall_status = "Emerging"
            elif (first_period_prop - last_period_prop) >= 4.0 or (first_period_prop > 0 and (first_period_prop - last_period_prop) / first_period_prop >= 0.40):
                overall_status = "Declining"
            else:
                overall_status = "Persistent"

            classifications.append({
                "Topic_Name": topic,
                "Overall_Classification": overall_status,
                "Start_Share_Pct": round(first_period_prop, 2),
                "End_Share_Pct": round(last_period_prop, 2),
                "Delta_Pct_Points": round(last_period_prop - first_period_prop, 2),
                "Total_Mentions": int(counts.sum()),
                "Period_Status": period_status
            })

        class_df = pd.DataFrame(classifications).sort_values(by="Delta_Pct_Points", ascending=False).reset_index(drop=True)

        return {
            "counts_matrix": ct_counts,
            "proportions_matrix": ct_proportions.round(2),
            "classifications": class_df,
            "semester_order": semester_order
        }
