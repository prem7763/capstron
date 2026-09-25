"""
Evaluation & Benchmarking Script (evaluate.py)
Implements all evaluation metrics specified in PRD Section 11:
1. Sentiment Classification: Accuracy, Precision, Recall, F1-score, Confusion Matrix
2. Aspect Classification: Precision, Recall, F1-score per aspect and macro-averaged
3. Topic Modeling: Topic Coherence (c_v approximation), Topic Diversity, Baseline Comparison (LDA / NMF)
4. Multilingual Normalization Benchmark: Pipeline A (Translate-to-EN) vs Pipeline B (Multilingual Embeddings)
5. Cross-Language Sentiment Diagnostic
"""

import os
import sys
import json
import time
import pandas as pd
import numpy as np

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from sklearn.metrics import precision_recall_fscore_support

from src.sentiment.evaluator import SentimentEvaluator
from src.sentiment.classifier import SentimentClassifier
from src.aspect.detector import AspectDetector, ASPECT_KEYWORDS
from src.topic.bertopic_engine import SemanticTopicEngine
from src.topic.baseline_engine import BaselineTopicEngine
from src.topic.coherence import TopicMetrics
from src.language.normalizer import MultilingualNormalizer

def main():
    print("=" * 70)
    print("📊 RUNNING MULTILINGUAL COURSE FEEDBACK EVALUATION SUITE")
    print("=" * 70)

    raw_path = "data/raw/course_feedback_raw.csv"
    if not os.path.exists(raw_path):
        from src.data_generation.generate_synthetic import generate_dataset
        generate_dataset(num_records=2200, output_path=raw_path)

    df = pd.read_csv(raw_path)
    print(f"Loaded evaluation sample of {len(df)} records.")

    eval_report = {}

    # -------------------------------------------------------------
    # 1. Sentiment Classification Evaluation (PRD Target: >= 85% F1)
    # -------------------------------------------------------------
    print("\n[1] Evaluating Sentiment Classification...")
    classifier = SentimentClassifier()
    predictions = [classifier.predict(t)["sentiment"] for t in df["Feedback_Text"]]
    df["Predicted_Sentiment"] = predictions

    sent_metrics = SentimentEvaluator.evaluate(
        df["Overall_Sentiment"].tolist(), df["Predicted_Sentiment"].tolist()
    )
    eval_report["sentiment_classification"] = sent_metrics

    print(f"  - Overall Accuracy: {sent_metrics['accuracy'] * 100:.2f}%")
    print(f"  - Macro F1-Score:   {sent_metrics['macro_f1'] * 100:.2f}%")
    print(f"  - Weighted F1-Score:{sent_metrics['weighted_f1'] * 100:.2f}%")
    print("  - Per-Class Metrics:")
    for lbl, m in sent_metrics["per_class"].items():
        print(f"    * {lbl:8s} | Prec: {m['precision']:.3f}, Rec: {m['recall']:.3f}, F1: {m['f1_score']:.3f} (n={m['support']})")

    # -------------------------------------------------------------
    # 2. Aspect Detection Evaluation (PRD Target: >= 80% Prec/Rec)
    # -------------------------------------------------------------
    print("\n[2] Evaluating Aspect Detection across 12 Dimensions...")
    detector = AspectDetector()
    all_aspect_names = list(ASPECT_KEYWORDS.keys())

    # Ground truth multi-hot vector
    y_true_aspects = []
    y_pred_aspects = []

    for _, row in df.iterrows():
        gt_aspects = set()
        try:
            records = json.loads(row["Aspect_Records"])
            for r in records:
                gt_aspects.add(r["aspect"])
        except Exception:
            pass

        pred_aspects = set(detector.detect_aspects(row["Feedback_Text"]))

        # Build binary vector for all 12 aspects
        true_vec = [1 if a in gt_aspects else 0 for a in all_aspect_names]
        pred_vec = [1 if a in pred_aspects else 0 for a in all_aspect_names]

        y_true_aspects.append(true_vec)
        y_pred_aspects.append(pred_vec)

    y_true_aspects = np.array(y_true_aspects)
    y_pred_aspects = np.array(y_pred_aspects)

    p_per_asp, r_per_asp, f1_per_asp, support_asp = precision_recall_fscore_support(
        y_true_aspects, y_pred_aspects, average=None, zero_division=0
    )
    macro_p, macro_r, macro_f1, _ = precision_recall_fscore_support(
        y_true_aspects, y_pred_aspects, average="macro", zero_division=0
    )

    aspect_eval = {
        "macro_precision": round(float(macro_p), 4),
        "macro_recall": round(float(macro_r), 4),
        "macro_f1": round(float(macro_f1), 4),
        "per_aspect": {}
    }

    print(f"  - Macro Aspect Precision: {macro_p * 100:.2f}%")
    print(f"  - Macro Aspect Recall:    {macro_r * 100:.2f}%")
    print(f"  - Macro Aspect F1:        {macro_f1 * 100:.2f}%")

    for i, asp in enumerate(all_aspect_names):
        aspect_eval["per_aspect"][asp] = {
            "precision": round(float(p_per_asp[i]), 4),
            "recall": round(float(r_per_asp[i]), 4),
            "f1_score": round(float(f1_per_asp[i]), 4),
            "support": int(support_asp[i])
        }

    eval_report["aspect_detection"] = aspect_eval

    # -------------------------------------------------------------
    # 3. Topic Modeling Coherence & Diversity (BERTopic vs LDA vs NMF)
    # -------------------------------------------------------------
    print("\n[3] Evaluating Topic Modeling: BERTopic-style vs LDA vs NMF...")
    corpus = df["Feedback_Text"].tolist()

    # 3A. Semantic Topic Engine (BERTopic style)
    sem_engine = SemanticTopicEngine(num_topics=8, random_state=42)
    sem_engine.fit_transform(corpus)
    sem_top_words = [sem_engine.topic_top_words[i] for i in range(8)]
    sem_diversity = TopicMetrics.topic_diversity(sem_top_words, top_k=10)
    sem_coherence = TopicMetrics.topic_coherence_c_v(sem_top_words, corpus, top_k=10)

    # 3B. LDA Baseline
    baseline = BaselineTopicEngine(num_topics=8, random_state=42)
    lda_res = baseline.fit_lda(corpus)
    lda_top_words = [lda_res["topics"][i]["top_words"] for i in range(8)]
    lda_diversity = TopicMetrics.topic_diversity(lda_top_words, top_k=10)
    lda_coherence = TopicMetrics.topic_coherence_c_v(lda_top_words, corpus, top_k=10)

    # 3C. NMF Baseline
    nmf_res = baseline.fit_nmf(corpus)
    nmf_top_words = [nmf_res["topics"][i]["top_words"] for i in range(8)]
    nmf_diversity = TopicMetrics.topic_diversity(nmf_top_words, top_k=10)
    nmf_coherence = TopicMetrics.topic_coherence_c_v(nmf_top_words, corpus, top_k=10)

    topic_comparison = {
        "Semantic_BERTopic": {
            "topic_diversity": sem_diversity,
            "topic_coherence_npmi": sem_coherence,
            "human_readable_naming": True
        },
        "LDA_Baseline": {
            "topic_diversity": lda_diversity,
            "topic_coherence_npmi": lda_coherence,
            "perplexity": lda_res["perplexity"],
            "human_readable_naming": False
        },
        "NMF_Baseline": {
            "topic_diversity": nmf_diversity,
            "topic_coherence_npmi": nmf_coherence,
            "reconstruction_error": nmf_res["reconstruction_err"],
            "human_readable_naming": False
        }
    }
    eval_report["topic_modeling"] = topic_comparison

    print("  - Topic Coherence & Diversity Comparison:")
    print(f"    * BERTopic / Semantic : Diversity = {sem_diversity:.3f} | Coherence = {sem_coherence:.3f} | Human Labels = Yes")
    print(f"    * LDA Baseline        : Diversity = {lda_diversity:.3f} | Coherence = {lda_coherence:.3f} | Perplexity = {lda_res['perplexity']}")
    print(f"    * NMF Baseline        : Diversity = {nmf_diversity:.3f} | Coherence = {nmf_coherence:.3f} | Recon Err = {nmf_res['reconstruction_err']}")

    # -------------------------------------------------------------
    # 4. Multilingual Normalization Benchmark (Pipeline A vs B)
    # -------------------------------------------------------------
    print("\n[4] Benchmarking Multilingual Normalization (Pipeline A vs B)...")
    normalizer = MultilingualNormalizer()
    norm_benchmark = normalizer.compare_pipelines(df.to_dict(orient="records")[:500])
    eval_report["multilingual_normalization_benchmark"] = norm_benchmark

    print(f"  - Pipeline A (Translate-to-EN)  : {norm_benchmark['pipeline_a']['throughput_records_per_sec']} rec/s | Vocab: {norm_benchmark['pipeline_a']['vocab_size']} | Sparsity: {norm_benchmark['pipeline_a']['matrix_sparsity_percent']}%")
    print(f"  - Pipeline B (Direct Multiling) : {norm_benchmark['pipeline_b']['throughput_records_per_sec']} rec/s | Vocab: {norm_benchmark['pipeline_b']['vocab_size']} | Sparsity: {norm_benchmark['pipeline_b']['matrix_sparsity_percent']}%")
    print(f"  - System Recommendation: {norm_benchmark['recommendation']}")

    # -------------------------------------------------------------
    # 5. Cross-Language Sentiment Diagnostic Check
    # -------------------------------------------------------------
    print("\n[5] Cross-Language Sentiment Accuracy Diagnostic...")
    cross_lang = {}
    for lang in df["Language"].unique():
        sub = df[df["Language"] == lang]
        lang_res = SentimentEvaluator.evaluate(
            sub["Overall_Sentiment"].tolist(), sub["Predicted_Sentiment"].tolist()
        )
        cross_lang[lang] = {
            "accuracy": lang_res["accuracy"],
            "macro_f1": lang_res["macro_f1"],
            "records": len(sub)
        }
        print(f"  - {lang:9s} : Accuracy = {lang_res['accuracy'] * 100:.2f}%, F1 = {lang_res['macro_f1'] * 100:.2f}% (n={len(sub)})")
    
    eval_report["cross_language_diagnostics"] = cross_lang

    # Save full evaluation report to JSON
    out_file = "evaluation_report.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(eval_report, f, indent=2)

    print("\n" + "=" * 70)
    print(f"✅ EVALUATION SUITE COMPLETED. Report saved to {out_file}")
    print("=" * 70)

if __name__ == "__main__":
    main()
