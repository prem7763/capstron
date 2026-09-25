"""
Language Detection Module (FR-2)
Accurately detects English, Hindi (Devanagari script), and Hinglish (Romanized Hindi-English code-mixed)
with confidence scoring and persistence.
"""

import re
from typing import Dict, Any

# Extensive vocabulary of common Hinglish function words, particles, and academic terms
HINGLISH_VOCAB = {
    "hai", "hain", "tha", "thi", "the", "nahi", "nahin", "na", "mat",
    "bohot", "bahut", "kaafi", "kuch", "sab", "sabhi", "aur", "lekin",
    "par", "magar", "toh", "bhi", "sirf", "bas", "karta", "karte",
    "karti", "karna", "kiya", "karo", "karenge", "hota", "hote", "hoti",
    "raha", "rahe", "rahi", "hoga", "honge", "hogi", "accha", "achha",
    "acche", "achhe", "acchi", "bura", "bure", "buri", "sahi", "galat",
    "samajh", "samjha", "padhate", "padhai", "seekha", "seekhne",
    "mushkil", "aasan", "zyada", "kam", "jaldi", "dhire", "tezi",
    "pehle", "baad", "mein", "se", "ko", "ke", "ki", "ka", "kisi",
    "apne", "apna", "apni", "kare", "sakta", "sakte", "sakti", "waise",
    "bilkul", "waala", "waali", "wale", "kahan", "kaise", "kyun",
    "bhai", "sir", "mam", "paper", "marks", "check", "bataya"
}

# Common English stop words
ENGLISH_STOPWORDS = {
    "the", "is", "at", "which", "on", "and", "a", "an", "in", "to", "for",
    "of", "it", "with", "as", "by", "this", "that", "from", "are", "was",
    "were", "be", "been", "have", "has", "had", "do", "does", "did", "but",
    "what", "all", "were", "we", "when", "your", "can", "said", "there",
    "use", "an", "each", "which", "she", "do", "how", "their", "if", "will"
}

class LanguageDetector:
    def __init__(self):
        # Devanagari Unicode range: \u0900 to \u097F
        self.devanagari_pattern = re.compile(r"[\u0900-\u097F]")
        self.word_token_pattern = re.compile(r"\b[a-zA-Z]+\b")

    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detects language of given text:
        - 'Hindi': If significant Devanagari characters are present (>15% of alphabetical characters)
        - 'Hinglish': If Latin script with >= 2 distinct Hinglish tokens or >10% Hinglish density
        - 'English': Default for Latin text without Hinglish marker density
        """
        if not isinstance(text, str) or not text.strip():
            return {"language": "English", "confidence": 0.50, "script": "Latin"}

        # Check for Devanagari script
        devanagari_chars = len(self.devanagari_pattern.findall(text))
        total_alpha = len(re.findall(r"[a-zA-Z\u0900-\u097F]", text))

        if total_alpha > 0 and (devanagari_chars / total_alpha) > 0.15:
            # Predominantly Devanagari script
            conf = min(0.99, max(0.85, devanagari_chars / (total_alpha + 1e-5)))
            return {
                "language": "Hindi",
                "confidence": round(conf, 2),
                "script": "Devanagari"
            }

        # Otherwise, Latin script text: check English vs Hinglish code-mixing
        words = [w.lower() for w in self.word_token_pattern.findall(text)]
        if not words:
            return {"language": "English", "confidence": 0.50, "script": "Latin"}

        hinglish_matches = [w for w in words if w in HINGLISH_VOCAB]
        english_matches = [w for w in words if w in ENGLISH_STOPWORDS]

        hinglish_ratio = len(hinglish_matches) / len(words)

        if len(hinglish_matches) >= 2 or (len(words) <= 5 and len(hinglish_matches) >= 1) or hinglish_ratio >= 0.08:
            conf = min(0.98, max(0.80, 0.70 + (hinglish_ratio * 0.5)))
            return {
                "language": "Hinglish",
                "confidence": round(conf, 2),
                "script": "Latin"
            }
        else:
            conf = min(0.98, max(0.82, 0.75 + (len(english_matches) / (len(words) + 1e-5) * 0.4)))
            return {
                "language": "English",
                "confidence": round(conf, 2),
                "script": "Latin"
            }

    def process_dataframe(self, df, text_col="Feedback_Text", out_col="Detected_Language"):
        """Applies language detection across a dataframe."""
        df = df.copy()
        res = df[text_col].apply(self.detect_language)
        df[out_col] = [r["language"] for r in res]
        df["Language_Confidence"] = [r["confidence"] for r in res]
        return df
