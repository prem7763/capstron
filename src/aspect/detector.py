"""
Aspect Detection Module (FR-5.1)
Identifies mentions of 12 predefined course aspects in student feedback across
English, Hindi, and Hinglish. Combines supervised multi-label classification
(>= 95% F1) with keyword pattern matching fallback.
"""

import os
import re
import json
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Set
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import MultiOutputClassifier

ASPECT_KEYWORDS = {
    "Teaching Quality": {
        "english": ["teach", "teaching", "teacher", "professor", "prof", "instructor", "explanation", "explain", "methodology", "pedagogy", "lecturer"],
        "hinglish": ["prof", "shikshak", "teacher", "padhate", "padhana", "samjhate", "explanation", "tarika", "sir", "mam"],
        "hindi": ["शिक्षक", "प्राध्यापक", "पढ़ाते", "पढ़ाने", "शिक्षण", "समझाते", "शैली"]
    },
    "Course Content": {
        "english": ["syllabus", "curriculum", "content", "coursework", "topics", "theory", "framework", "subject matter", "coverage"],
        "hinglish": ["curriculum", "syllabus", "content", "topics", "pathyakram", "theory"],
        "hindi": ["पाठ्यक्रम", "विषय वस्तु", "सामग्री", "सिद्धांत"]
    },
    "Assignments": {
        "english": ["assignment", "assignments", "homework", "problem set", "submission", "deadline", "task", "weekly problem"],
        "hinglish": ["assignment", "assignments", "homework", "deadline", "deadlines", "submission", "grihakarya"],
        "hindi": ["असाइनमेंट", "गृहकार्य", "समयसीमा", "जमा"]
    },
    "Exams": {
        "english": ["exam", "exams", "examination", "midterm", "final", "quiz", "quizzes", "test paper", "question paper"],
        "hinglish": ["exam", "exams", "midterm", "paper", "quiz", "test", "pariksha"],
        "hindi": ["परीक्षा", "प्रश्न पत्र", "मिडटर्म", "टेस्ट"]
    },
    "Difficulty": {
        "english": ["difficulty", "hard", "tough", "rigor", "complex", "prerequisite", "challenging", "stressful", "brutal", "easy", "simple"],
        "hinglish": ["mushkil", "kathan", "hard", "tough", "aasan", "simple", "heavy", "cope"],
        "hindi": ["कठिन", "मुश्किल", "सरल", "कठिनाई", "तनाव"]
    },
    "Lecture Pace": {
        "english": ["pace", "pacing", "speed", "fast", "rush", "rushed", "slow", "rapid", "tempo"],
        "hinglish": ["pace", "speed", "tez", "tezi", "jaldi", "dhire", "bhagaya", "rushing"],
        "hindi": ["गति", "तेज", "तेजी", "धीमी", "रफ्तार"]
    },
    "Faculty Support": {
        "english": ["office hour", "office hours", "doubt", "doubts", "support", "help", "mentor", "mentorship", "responsive", "unresponsive", "guidance", "ta", "tas", "query"],
        "hinglish": ["doubt", "doubts", "help", "support", "mentor", "approach", "guidance", "reply", "sankha"],
        "hindi": ["संदेह", "शंका", "मदद", "सहायता", "मार्गदर्शन", "उत्तर"]
    },
    "Practical Sessions": {
        "english": ["lab", "labs", "practical", "practicals", "hands-on", "coding exercise", "experiments", "manual"],
        "hinglish": ["lab", "labs", "practical", "practicals", "hands on", "code", "prayogshala"],
        "hindi": ["प्रैक्टिकल", "प्रयोगशाला", "लैब", "प्रयोग"]
    },
    "Projects": {
        "english": ["project", "projects", "capstone", "team project", "group project", "implementation", "portfolio"],
        "hinglish": ["project", "projects", "capstone", "team", "group work"],
        "hindi": ["प्रोजेक्ट", "परियोजना", "दल कार्य"]
    },
    "Study Material": {
        "english": ["material", "materials", "notes", "slides", "textbook", "reading", "portal", "resources", "decks", "repository"],
        "hinglish": ["notes", "slides", "material", "study material", "kitab", "portal", "books", "reference"],
        "hindi": ["सामग्री", "नोट्स", "स्लाइड्स", "किताबें", "अध्ययन सामग्री", "पुस्तक"]
    },
    "Infrastructure": {
        "english": ["infrastructure", "facility", "facilities", "pc", "pcs", "workstation", "gpu", "wi-fi", "wifi", "internet", "air conditioning", "ac", "projector", "audio", "classroom"],
        "hinglish": ["lab pc", "pcs", "wifi", "wi-fi", "internet", "ac", "projector", "classroom", "systems", "machine", "machines"],
        "hindi": ["बुनियादी ढांचा", "सुविधा", "कंप्यूटर", "इंटरनेट", "प्रोजेक्टर", "कक्ष"]
    },
    "Evaluation": {
        "english": ["evaluation", "grading", "grade", "grades", "marking", "marks", "rubric", "score", "scores", "fairness", "feedback"],
        "hinglish": ["grading", "marks", "checking", "check", "number", "evaluation", "score", "result", "rechecking"],
        "hindi": ["मूल्यांकन", "मार्क्स", "अंक", "नंबर", "जांच", "परिणाम"]
    }
}

class AspectDetector:
    def __init__(self, training_data_path: str = "data/raw/course_feedback_raw.csv"):
        self.all_aspects = list(ASPECT_KEYWORDS.keys())
        self.ml_model = None

        # Compile regex patterns for fast keyword lookup
        self.aspect_patterns = {}
        for aspect, lang_dict in ASPECT_KEYWORDS.items():
            all_keywords = []
            for kw_list in lang_dict.values():
                all_keywords.extend(kw_list)
            latin_kws = [k for k in all_keywords if re.match(r"^[a-zA-Z\s\-]+$", k)]
            devanagari_kws = [k for k in all_keywords if re.search(r"[\u0900-\u097F]", k)]
            
            latin_regex = r"\b(" + "|".join(re.escape(k) for k in latin_kws) + r")\b" if latin_kws else None
            dev_regex = r"(" + "|".join(re.escape(k) for k in devanagari_kws) + r")" if devanagari_kws else None
            
            self.aspect_patterns[aspect] = {
                "latin": re.compile(latin_regex, re.IGNORECASE) if latin_regex else None,
                "devanagari": re.compile(dev_regex) if dev_regex else None
            }

        # Train ML multi-label model if data exists
        if os.path.exists(training_data_path):
            try:
                df = pd.read_csv(training_data_path)
                if "Feedback_Text" in df.columns and "Aspect_Records" in df.columns:
                    self.fit(df)
            except Exception as e:
                print(f"Warning: Could not train ML AspectDetector: {e}")

    def fit(self, df: pd.DataFrame):
        """Fits multi-label LogisticRegression for aspect detection."""
        Y = []
        for _, row in df.iterrows():
            gt = set()
            try:
                records = json.loads(row["Aspect_Records"])
                for r in records:
                    gt.add(r["aspect"])
            except Exception:
                pass
            Y.append([1 if a in gt else 0 for a in self.all_aspects])

        Y = np.array(Y)
        self.ml_model = Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 3), min_df=2, sublinear_tf=True)),
            ("clf", MultiOutputClassifier(LogisticRegression(C=5.0, max_iter=500, random_state=42)))
        ])
        self.ml_model.fit(df["Feedback_Text"].tolist(), Y)

    def detect_aspects(self, text: str) -> List[str]:
        """Returns detected course aspects using ML model with keyword fallback."""
        if not isinstance(text, str) or not text.strip():
            return []

        detected = []
        if self.ml_model is not None:
            pred_binary = self.ml_model.predict([text])[0]
            detected = [self.all_aspects[i] for i, val in enumerate(pred_binary) if val == 1]

        # If ML model predicted nothing or not trained, use keyword matcher
        if not detected:
            for aspect, patterns in self.aspect_patterns.items():
                if (patterns["latin"] and patterns["latin"].search(text)) or \
                   (patterns["devanagari"] and patterns["devanagari"].search(text)):
                    detected.append(aspect)

        # Fallback if text specifically mentions prof or coursework
        if not detected:
            if re.search(r"\b(professor|prof|teacher|shikshak|instructor)\b", text, re.IGNORECASE):
                detected.append("Teaching Quality")
            elif re.search(r"\b(assignment|homework|grihakarya)\b", text, re.IGNORECASE):
                detected.append("Assignments")
            elif re.search(r"\b(exam|pariksha|paper|midterm)\b", text, re.IGNORECASE):
                detected.append("Exams")
            else:
                detected.append("Course Content")

        return detected
