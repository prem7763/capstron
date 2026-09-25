"""
Multilingual Normalization Module (FR-3)
Implements:
- Pipeline A: Translation & transliteration of Hindi / Hinglish to English.
- Pipeline B: Direct multilingual representation (language-agnostic feature space).
Provides comparative metrics (speed, vocabulary coverage, and representation density).
"""

import time
import re
from typing import Dict, Any, List
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Comprehensive lexicon mapping from Hinglish and Hindi words to English equivalents
HINGLISH_TO_ENGLISH_MAP = {
    # Sentiment & Quality
    "accha": "good", "achha": "good", "acche": "good", "achhe": "good", "acchi": "good",
    "badhiya": "great", "shandaar": "fantastic", "zabardast": "awesome", "badiya": "great",
    "bura": "bad", "bure": "bad", "kharab": "broken bad", "bakwas": "terrible",
    "bekaar": "useless", "ghatiya": "awful", "mushkil": "difficult hard", "kathan": "difficult",
    "aasan": "easy", "saral": "simple easy", "clear": "clear", "unclear": "unclear",
    "boring": "boring", "interesting": "engaging", "help": "helpful", "helpful": "helpful",
    # Negation
    "nahi": "not", "nahin": "not", "na": "not", "mat": "do not", "kabhi nahi": "never",
    "bina": "without", "bilkul nahi": "absolutely not",
    # Academic Entities & Aspects
    "prof": "professor", "sir": "instructor", "mam": "instructor", "teacher": "teacher",
    "shikshak": "teacher", "adverse": "negative", "class": "lecture", "kaksha": "lecture",
    "padhai": "teaching study", "padhate": "teaches", "samajh": "understanding",
    "samjhate": "explains", "samjha": "understood", "doubt": "question doubt",
    "sankha": "doubt", "lab": "laboratory", "prayogshala": "laboratory",
    "practical": "practical session", "assignment": "assignment", "homework": "homework",
    "grihakarya": "assignment", "exam": "examination", "pariksha": "examination",
    "marks": "grades evaluation", "ank": "marks score", "checking": "grading evaluation",
    "paper": "examination paper", "syllabus": "curriculum content", "pathyakram": "curriculum",
    "pace": "lecture pace speed", "gati": "speed pace", "tez": "fast rushed",
    "dhire": "slow", "jaldi": "fast rushed", "time": "time duration", "samay": "time duration",
    "notes": "study material notes", "kitab": "textbook", "pustak": "textbook",
    "slides": "slides presentation", "computer": "infrastructure computer",
    "wi-fi": "infrastructure internet wifi", "wifi": "infrastructure internet wifi",
    "ac": "air conditioning", "hall": "lecture hall classroom", "project": "project capstone",
    # Adverbs & Intensifiers
    "bohot": "very", "bahut": "very", "kaafi": "quite", "zyada": "too much excessive",
    "kam": "little inadequate", "thoda": "slightly", "sirf": "only", "bas": "just only",
    "hamesha": "always", "kabhi": "ever", "ekdum": "completely", "bilkul": "totally"
}

HINDI_DEVANAGARI_TO_ENGLISH_MAP = {
    # Sentiment & Quality
    "अच्छा": "good", "अच्छे": "good", "अच्छी": "good", "शानदार": "great", "उत्कृष्ट": "excellent",
    "बुरा": "bad", "खराब": "bad broken", "कठिन": "difficult hard", "आसान": "easy",
    "सरल": "simple easy", "उबाऊ": "boring", "रोचक": "interesting", "उपयोगी": "useful helpful",
    # Negation
    "नहीं": "not", "ना": "not", "मत": "do not", "कभी नहीं": "never", "बिना": "without",
    # Academic Aspects
    "शिक्षक": "teacher professor", "प्राध्यापक": "professor", "पढ़ाते": "teaches",
    "पढ़ाने": "teaching", "समझाते": "explains", "स्पष्ट": "clear", "अस्पष्ट": "unclear",
    "व्याख्यान": "lecture", "कक्षा": "class", "गति": "speed pace", "तेज": "fast rushed",
    "धीमी": "slow", "असाइनमेंट": "assignment", "गृहकार्य": "assignment homework",
    "परीक्षा": "examination test", "प्रश्न": "question", "मूल्यांकन": "evaluation grading",
    "अंक": "marks score", "लैब": "laboratory practical", "प्रैक्टिकल": "practical lab",
    "प्रोजेक्ट": "project", "सामग्री": "study material", "नोट्स": "notes slides",
    "पुस्तकालय": "library", "सुविधा": "infrastructure facilities", "कंप्यूटर": "computer",
    "इंटरनेट": "internet wifi", "संदेह": "doubt query", "मदद": "help support",
    "सहायता": "support assistance", "पाठ्यक्रम": "syllabus course content",
    # Intensifiers
    "बहुत": "very", "अत्यधिक": "excessive too much", "काफी": "quite", "कम": "inadequate low",
    "थोड़ा": "little", "हमेशा": "always", "समय": "time duration"
}

class MultilingualNormalizer:
    def __init__(self):
        self.hinglish_map = HINGLISH_TO_ENGLISH_MAP
        self.hindi_map = HINDI_DEVANAGARI_TO_ENGLISH_MAP
        # Regex patterns for fast lookup
        self.word_regex = re.compile(r"\b\w+\b")

    def translate_to_english_pipeline_a(self, text: str, detected_lang: str = "Hinglish") -> str:
        """
        Pipeline A: Transliteration & Lexicon-based Translation to standardized English tokens.
        Preserves original sentence syntax while replacing multilingual terms with English anchors.
        """
        if not isinstance(text, str) or not text.strip():
            return ""

        result = text
        if detected_lang in ["Hinglish", "English"]:
            # Word-level replacement for Hinglish
            words = text.split()
            translated_words = []
            for w in words:
                clean_w = re.sub(r"[^\w]", "", w.lower())
                if clean_w in self.hinglish_map:
                    translated_words.append(self.hinglish_map[clean_w])
                else:
                    translated_words.append(w)
            result = " ".join(translated_words)

        if detected_lang == "Hindi" or re.search(r"[\u0900-\u097F]", text):
            # Devanagari replacement
            for hi_word, en_word in self.hindi_map.items():
                if hi_word in result:
                    result = result.replace(hi_word, f" {en_word} ")

        # Clean excess spaces
        result = re.sub(r"\s+", " ", result).strip()
        return result

    def multilingual_representation_pipeline_b(self, texts: List[str]):
        """
        Pipeline B: Direct Multilingual Representation without translation.
        Extracts cross-lingual character and word n-grams preserving native multilingual morphology.
        """
        vectorizer = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(3, 5),
            min_df=2,
            max_features=5000
        )
        matrix = vectorizer.fit_transform(texts)
        return vectorizer, matrix

    def compare_pipelines(self, sample_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compares Pipeline A (Translate-to-English) vs Pipeline B (Direct Multilingual Representation)
        on Latency, Vocabulary Coverage, and Information Density.
        """
        texts = [r["Feedback_Text"] for r in sample_records]
        langs = [r.get("Language", "English") for r in sample_records]
        n_samples = len(texts)

        # Benchmark Pipeline A
        start_a = time.perf_counter()
        normalized_texts_a = [
            self.translate_to_english_pipeline_a(t, l) for t, l in zip(texts, langs)
        ]
        vec_a = TfidfVectorizer(max_features=3000)
        mat_a = vec_a.fit_transform(normalized_texts_a)
        duration_a = time.perf_counter() - start_a

        # Benchmark Pipeline B
        start_b = time.perf_counter()
        vec_b, mat_b = self.multilingual_representation_pipeline_b(texts)
        duration_b = time.perf_counter() - start_b

        # Compute sparsity and throughput
        throughput_a = round(n_samples / (duration_a + 1e-6), 1)
        throughput_b = round(n_samples / (duration_b + 1e-6), 1)
        
        sparsity_a = round(100.0 * (1.0 - mat_a.nnz / (mat_a.shape[0] * mat_a.shape[1])), 2)
        sparsity_b = round(100.0 * (1.0 - mat_b.nnz / (mat_b.shape[0] * mat_b.shape[1])), 2)

        return {
            "num_samples_evaluated": n_samples,
            "pipeline_a": {
                "name": "Pipeline A: Translate / Transliterate to English",
                "duration_seconds": round(duration_a, 4),
                "throughput_records_per_sec": throughput_a,
                "vocab_size": mat_a.shape[1],
                "matrix_sparsity_percent": sparsity_a,
                "strengths": "Direct interoperability with English sentiment lexicons & BERT models, highly interpretable topic names.",
                "tradeoffs": "Requires translation lexicon maintenance."
            },
            "pipeline_b": {
                "name": "Pipeline B: Direct Multilingual Character / Word Representation",
                "duration_seconds": round(duration_b, 4),
                "throughput_records_per_sec": throughput_b,
                "vocab_size": mat_b.shape[1],
                "matrix_sparsity_percent": sparsity_b,
                "strengths": "Zero translation overhead, preserves original colloquial nuances and code-switching tokens.",
                "tradeoffs": "Higher dimensional feature matrix, multilingual vocabulary overlap challenges."
            },
            "recommendation": "Pipeline A achieves higher semantic cohesion for downstream ABSA and topic labeling, while Pipeline B provides low-latency baseline embeddings."
        }
