"""
Text Preprocessing & Cleaning Module (FR-1)
Handles deduplication, missing values, emoji parsing, whitespace normalization,
and strictly preserves negation words across English, Hindi, and Hinglish.
"""

import re
import unicodedata
import pandas as pd

# Comprehensive emoji dictionary for student sentiment contexts
EMOJI_SENTIMENT_MAP = {
    "😊": " positive_feeling ",
    "😀": " positive_feeling ",
    "😁": " positive_feeling ",
    "👍": " thumbs_up ",
    "🔥": " great_performance ",
    "⭐": " excellent ",
    "💯": " top_marks ",
    "❤️": " loved_it ",
    "😍": " impressed ",
    "🎉": " celebration ",
    "🙌": " applause ",
    "👏": " well_done ",
    "😞": " disappointed ",
    "😢": " sad ",
    "😭": " crying_distress ",
    "😡": " angry_frustration ",
    "👎": " thumbs_down ",
    "💔": " heartbreak ",
    "😴": " boring_sleepy ",
    "🥱": " yawning_tedious ",
    "🤮": " terrible ",
    "🤯": " mind_blown_confused ",
    "❓": " query_doubt ",
    "⚠️": " warning_issue "
}

# Negation words across English, Hindi, and Hinglish that MUST be preserved
NEGATION_TOKENS = {
    # English
    "not", "no", "never", "neither", "nor", "none", "nobody", "nowhere",
    "cannot", "cant", "can't", "dont", "don't", "doesnt", "doesn't",
    "didnt", "didn't", "wont", "won't", "wouldnt", "wouldn't",
    "shouldnt", "shouldn't", "couldnt", "couldn't", "isnt", "isn't",
    "arent", "aren't", "wasnt", "wasn't", "werent", "weren't",
    "havent", "haven't", "hasnt", "hasn't", "hadnt", "hadn't",
    "barely", "hardly", "scarcely", "without",
    # Hindi (Devanagari)
    "नहीं", "न", "ना", "मत", "कदापि नहीं", "बगैर", "बिना", "शून्य",
    # Hinglish (Romanized)
    "nahi", "nahin", "na", "mat", "kabhi nahi", "bina", "kuch nahi",
    "bilkul nahi", "kuch bhi nahi"
}

class FeedbackCleaner:
    def __init__(self, min_char_length=6):
        self.min_char_length = min_char_length

    def replace_emojis(self, text: str) -> str:
        """Converts emojis to descriptive textual sentiment tokens."""
        if not isinstance(text, str):
            return ""
        for emoji_char, replacement in EMOJI_SENTIMENT_MAP.items():
            if emoji_char in text:
                text = text.replace(emoji_char, replacement)
        return text

    def clean_text(self, text: str, preserve_case: bool = False) -> str:
        """
        Cleans and normalizes a single feedback string.
        Preserves punctuation that affects phrasing while stripping noise.
        Specifically retains negation markers.
        """
        if not isinstance(text, str) or not text.strip():
            return ""

        # 1. Unicode normalization
        text = unicodedata.normalize("NFKC", text)

        # 2. Map emojis to textual cues
        text = self.replace_emojis(text)

        # 3. Standardize common contractions for negation preservation
        contractions = {
            "can't": "cannot",
            "won't": "will not",
            "n't": " not",
            "don't": "do not",
            "doesn't": "does not",
            "didn't": "did not",
            "isn't": "is not",
            "aren't": "are not",
            "wasn't": "was not",
            "weren't": "were not",
            "haven't": "have not",
            "hasn't": "has not",
            "hadn't": "had not"
        }
        for contr, expanded in contractions.items():
            text = re.sub(re.escape(contr), expanded, text, flags=re.IGNORECASE)

        # 4. Remove URLs and HTML tags if present
        text = re.sub(r"https?://\S+|www\.\S+", " ", text)
        text = re.sub(r"<.*?>", " ", text)

        # 5. Clean up special characters while keeping punctuation useful for clause splitting (. , ! ? - ;)
        # Keep Devanagari Unicode block (\u0900-\u097F), Latin letters, numbers, and basic punctuation
        text = re.sub(r"[^\w\s\u0900-\u097F.,!?;:\-']", " ", text)

        # 6. Normalize multiple whitespaces
        text = re.sub(r"\s+", " ", text).strip()

        if not preserve_case:
            # We lower for English & Hinglish, Devanagari has no case
            text = text.lower()

        return text

    def is_valid_feedback(self, text: str) -> bool:
        """Flags feedback that is too short, empty, or purely noise."""
        if not isinstance(text, str):
            return False
        cleaned = text.strip()
        if len(cleaned) < self.min_char_length:
            return False
        # Check if it has at least some alphabetic or Devanagari character
        if not re.search(r"[a-zA-Z\u0900-\u097F]", cleaned):
            return False
        return True

    def clean_dataframe(self, df: pd.DataFrame, text_col: str = "Feedback_Text") -> pd.DataFrame:
        """
        Processes entire DataFrame: deduplicates, removes nulls,
        flags invalid entries, and adds a Cleaned_Text column.
        """
        df = df.copy()
        initial_len = len(df)

        # Handle nulls
        df = df.dropna(subset=[text_col])

        # Deduplicate based on Student_ID, Course_ID, and Feedback_Text if present
        subset_cols = [c for c in ["Student_ID", "Course_ID", text_col] if c in df.columns]
        if subset_cols:
            df = df.drop_duplicates(subset=subset_cols)

        # Apply cleaning
        df["Cleaned_Text"] = df[text_col].apply(lambda t: self.clean_text(str(t)))

        # Flag valid feedback
        df["Is_Valid"] = df["Cleaned_Text"].apply(self.is_valid_feedback)
        valid_df = df[df["Is_Valid"]].drop(columns=["Is_Valid"]).reset_index(drop=True)

        print(f"Preprocessing complete: Retained {len(valid_df)}/{initial_len} valid feedback records.")
        return valid_df
