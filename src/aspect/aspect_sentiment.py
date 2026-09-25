"""
Aspect-Level Sentiment Extractor (FR-5.2)
Extracts local syntactic/clause windows for each detected aspect and assigns
independent sentiment (Positive/Negative/Neutral) and confidence score.
"""

import re
from typing import List, Dict, Any
from src.aspect.detector import AspectDetector, ASPECT_KEYWORDS
from src.sentiment.classifier import SentimentClassifier

class AspectSentimentExtractor:
    def __init__(self):
        self.detector = AspectDetector()
        self.classifier = SentimentClassifier()

    def extract_aspect_snippet(self, text: str, aspect: str) -> str:
        """
        Locates the aspect mention in text and extracts the corresponding clause/sentence
        to accurately isolate the sentiment specific to this aspect.
        """
        # Split text into logical clause units
        clauses = re.split(r"(?<=[.!?])\s+|(?<=[,;])\s+|\s+(?:however|but|although|lekin|par|aur|and|परन्तु|लेकिन|और)\s+", text, flags=re.IGNORECASE)
        
        # Check which clause contains the aspect trigger
        aspect_dict = ASPECT_KEYWORDS.get(aspect, {})
        all_kws = []
        for kw_list in aspect_dict.values():
            all_kws.extend(kw_list)

        matched_clauses = []
        for clause in clauses:
            for kw in all_kws:
                if re.search(r"[\u0900-\u097F]", kw):
                    if kw in clause:
                        matched_clauses.append(clause.strip())
                        break
                else:
                    if re.search(rf"\b{re.escape(kw)}\b", clause, re.IGNORECASE):
                        matched_clauses.append(clause.strip())
                        break

        if matched_clauses:
            return " ".join(matched_clauses)
        
        # Fallback to entire text if clause isolation yields nothing
        return text

    def analyze_aspects(self, text: str) -> List[Dict[str, Any]]:
        """
        Detects all aspects in the feedback and extracts per-aspect sentiment,
        confidence, and snippet.
        """
        detected_aspects = self.detector.detect_aspects(text)
        results = []

        for aspect in detected_aspects:
            snippet = self.extract_aspect_snippet(text, aspect)
            sentiment_res = self.classifier.predict(snippet)

            results.append({
                "aspect": aspect,
                "sentiment": sentiment_res["sentiment"],
                "confidence": sentiment_res["confidence"],
                "polarity_score": sentiment_res["score"],
                "evidence_snippet": snippet
            })

        return results
