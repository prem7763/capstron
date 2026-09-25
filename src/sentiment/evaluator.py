"""
Sentiment Evaluator Module (Section 11)
Calculates Accuracy, Precision, Recall, F1-score (macro and weighted),
generates Confusion Matrix, and computes cross-language diagnostics.
"""

from typing import Dict, Any, List
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

class SentimentEvaluator:
    @staticmethod
    def evaluate(y_true: List[str], y_pred: List[str], labels: List[str] = None) -> Dict[str, Any]:
        if labels is None:
            labels = ["Positive", "Negative", "Neutral"]

        acc = accuracy_score(y_true, y_pred)
        p_macro, r_macro, f1_macro, _ = precision_recall_fscore_support(
            y_true, y_pred, labels=labels, average="macro", zero_division=0
        )
        p_weighted, r_weighted, f1_weighted, _ = precision_recall_fscore_support(
            y_true, y_pred, labels=labels, average="weighted", zero_division=0
        )

        p_per_class, r_per_class, f1_per_class, support = precision_recall_fscore_support(
            y_true, y_pred, labels=labels, average=None, zero_division=0
        )

        cm = confusion_matrix(y_true, y_pred, labels=labels)

        per_class_metrics = {}
        for idx, lbl in enumerate(labels):
            per_class_metrics[lbl] = {
                "precision": round(float(p_per_class[idx]), 4),
                "recall": round(float(r_per_class[idx]), 4),
                "f1_score": round(float(f1_per_class[idx]), 4),
                "support": int(support[idx])
            }

        return {
            "accuracy": round(float(acc), 4),
            "macro_precision": round(float(p_macro), 4),
            "macro_recall": round(float(r_macro), 4),
            "macro_f1": round(float(f1_macro), 4),
            "weighted_f1": round(float(f1_weighted), 4),
            "per_class": per_class_metrics,
            "confusion_matrix": cm.tolist(),
            "labels": labels
        }

    @staticmethod
    def evaluate_by_group(df, group_col: str, y_true_col: str, y_pred_col: str) -> Dict[str, Any]:
        """Evaluates sentiment metrics broken down by language or course."""
        groups = df[group_col].unique()
        res = {}
        for g in groups:
            sub = df[df[group_col] == g]
            if len(sub) > 0:
                res[str(g)] = SentimentEvaluator.evaluate(
                    sub[y_true_col].tolist(), sub[y_pred_col].tolist()
                )
        return res
