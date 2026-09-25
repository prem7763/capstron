"""
Semantic Topic Modeling Engine (FR-6)
Implements BERTopic-style modular architecture:
1. Document vectorization & dimensionality reduction
2. Semantic cluster discovery
3. Class-based TF-IDF (c-TF-IDF) for keyword extraction
4. Dynamic generation of human-readable topic names
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple
from collections import defaultdict
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

# Semantic theme descriptors for labeling clusters
TOPIC_THEME_RULES = [
    {
        "name": "Assignment Workload & Deadlines",
        "keywords": {"assignment", "assignments", "homework", "deadline", "deadlines", "submission", "workload", "grihakarya"}
    },
    {
        "name": "Lab Infrastructure & Hardware",
        "keywords": {"lab", "pc", "pcs", "workstation", "wifi", "internet", "gpu", "machine", "crash", "facilities", "ac", "hardware"}
    },
    {
        "name": "Exam Difficulty & Time Management",
        "keywords": {"exam", "exams", "paper", "midterm", "final", "test", "time", "quiz", "questions", "pariksha", "tough"}
    },
    {
        "name": "Lecture Pace & Fundamentals",
        "keywords": {"pace", "speed", "fast", "rush", "rushed", "lecture", "slides", "speed", "tezi", "dhire", "basics"}
    },
    {
        "name": "Faculty Support & Mentorship",
        "keywords": {"faculty", "teacher", "professor", "prof", "doubts", "doubt", "office", "hours", "mentor", "guidance", "responsive", "unresponsive", "help"}
    },
    {
        "name": "Grading Fairness & Evaluation",
        "keywords": {"grading", "marks", "evaluation", "score", "rubric", "checking", "check", "unfair", "transparent", "results"}
    },
    {
        "name": "Capstone Projects & Implementation",
        "keywords": {"project", "projects", "capstone", "portfolio", "team", "code", "architecture", "industry", "review"}
    },
    {
        "name": "Curriculum Modernity & Tools",
        "keywords": {"curriculum", "syllabus", "content", "modern", "frameworks", "tools", "theory", "industry", "standards"}
    },
    {
        "name": "Study Materials & Reference Notes",
        "keywords": {"notes", "slides", "material", "study", "portal", "book", "textbook", "reading", "repos"}
    },
    {
        "name": "Placement Prep & Coding Rounds",
        "keywords": {"placement", "interview", "coding", "algorithms", "problem", "prep", "practice", "rounds", "competitive"}
    }
]

# Comprehensive multilingual stopwords across English, Hindi, and Hinglish
MULTILINGUAL_STOPWORDS = {
    # English
    "the", "is", "at", "which", "on", "and", "a", "an", "in", "to", "for",
    "of", "it", "with", "as", "by", "this", "that", "from", "are", "was",
    "were", "be", "been", "have", "has", "had", "do", "does", "did", "but",
    "what", "all", "we", "when", "your", "can", "said", "there", "use",
    # Hinglish
    "hai", "hain", "tha", "thi", "the", "mein", "se", "ko", "ke", "ki", "ka",
    "kisi", "par", "lekin", "toh", "bhi", "sirf", "bas", "kuch", "karta",
    "karte", "raha", "rahe", "wali", "wale", "sath", "kare", "hoga", "honge",
    "bohot", "bahut", "kaafi", "zyada", "kam", "hota", "hote", "hoti", "aur",
    "thoda", "baad", "pehle", "bina", "bilkul", "waise", "unke", "unki",
    # Hindi (Devanagari)
    "और", "है", "हैं", "था", "थी", "थे", "में", "से", "को", "के", "की", "का",
    "पर", "लेकिन", "तो", "भी", "सिर्फ", "कुछ", "बहुत", "काफी", "रहा", "रहे",
    "होता", "होते", "सकते", "सकता", "किया", "गया", "गए", "साथ", "बाद", "पहले"
}

class ClassTFIDF:
    """Class-based TF-IDF (c-TF-IDF) as formulated in BERTopic."""
    def __init__(self, max_features=3000):
        self.max_features = max_features
        self.vectorizer = CountVectorizer(stop_words=list(MULTILINGUAL_STOPWORDS), max_features=max_features)
        self.words = []

    def fit_transform(self, documents_per_cluster: List[str]):
        # Term count matrix per cluster: shape (n_clusters, n_vocab)
        X = self.vectorizer.fit_transform(documents_per_cluster).toarray()
        self.words = np.array(self.vectorizer.get_feature_names_out())
        
        # Total words in each cluster
        cluster_words = X.sum(axis=1, keepdims=True)
        # Avoid division by zero
        tf = X / np.maximum(cluster_words, 1e-6)
        
        # Global frequency of each word across all clusters
        f_t = X.sum(axis=0, keepdims=True)
        # Average number of words per cluster
        A = cluster_words.mean()
        
        idf = np.log(1.0 + (A / np.maximum(f_t, 1e-6)))
        c_tfidf = tf * idf
        return c_tfidf

class SemanticTopicEngine:
    def __init__(self, num_topics=8, random_state=42):
        self.num_topics = num_topics
        self.random_state = random_state
        self.vectorizer = TfidfVectorizer(max_features=2500, stop_words=list(MULTILINGUAL_STOPWORDS), ngram_range=(1, 2))
        self.svd = TruncatedSVD(n_components=min(40, num_topics * 4), random_state=random_state)
        self.cluster_model = KMeans(n_clusters=num_topics, random_state=random_state, n_init=10)
        self.c_tfidf_model = ClassTFIDF()
        
        self.topic_names = {}
        self.topic_top_words = {}
        self.topic_sizes = {}

    def _generate_human_readable_name(self, top_words: List[str], topic_id: int) -> str:
        """Assigns an intuitive, human-readable title based on c-TF-IDF top keywords."""
        top_words_set = set(top_words[:10])
        best_match = None
        max_overlap = 0

        for rule in TOPIC_THEME_RULES:
            overlap = len(top_words_set.intersection(rule["keywords"]))
            if overlap > max_overlap:
                max_overlap = overlap
                best_match = rule["name"]

        if best_match and max_overlap >= 1:
            return best_match
        else:
            # Fallback combining top 3 terms
            primary_terms = [w.capitalize() for w in top_words[:3] if len(w) > 2]
            return " & ".join(primary_terms) if primary_terms else f"Course Theme {topic_id + 1}"

    def fit_transform(self, documents: List[str]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Fits topic model and returns:
        - topic_assignments: array of topic IDs per document
        - topic_probabilities: array of confidence scores per document
        """
        # Step 1: Document TF-IDF & SVD reduction (representing embedding space)
        X = self.vectorizer.fit_transform(documents)
        embeddings = self.svd.fit_transform(X)

        # Step 2: Clustering into coherent semantic topic groups
        cluster_labels = self.cluster_model.fit_predict(embeddings)

        # Step 3: Compute cluster centers and distance-based probabilities
        cluster_centers = self.cluster_model.cluster_centers_
        dists = np.linalg.norm(embeddings[:, np.newaxis, :] - cluster_centers[np.newaxis, :, :], axis=2)
        # Softmax / inverted distance for probability
        exp_dists = np.exp(-dists)
        probabilities = exp_dists / exp_dists.sum(axis=1, keepdims=True)
        assigned_probs = np.max(probabilities, axis=1)

        # Step 4: Class-based TF-IDF (c-TF-IDF)
        clustered_docs = defaultdict(list)
        for doc, lbl in zip(documents, cluster_labels):
            clustered_docs[lbl].append(doc)

        docs_per_cluster = [" ".join(clustered_docs[i]) for i in range(self.num_topics)]
        c_tfidf_matrix = self.c_tfidf_model.fit_transform(docs_per_cluster)

        # Step 5: Extract top keywords and generate human-readable topic labels
        used_names = set()
        for topic_id in range(self.num_topics):
            scores = c_tfidf_matrix[topic_id]
            top_word_indices = scores.argsort()[::-1][:15]
            top_words = self.c_tfidf_model.words[top_word_indices].tolist()
            
            self.topic_top_words[topic_id] = top_words
            self.topic_sizes[topic_id] = len(clustered_docs[topic_id])

            name = self._generate_human_readable_name(top_words, topic_id)
            if name in used_names:
                # Add differentiator
                name = f"{name} (Track {topic_id + 1})"
            used_names.add(name)
            self.topic_names[topic_id] = name

        return cluster_labels, assigned_probs

    def get_topic_info(self) -> pd.DataFrame:
        """Returns summary dataframe of all discovered topics."""
        rows = []
        for topic_id in range(self.num_topics):
            top_terms = ", ".join(self.topic_top_words.get(topic_id, [])[:6])
            rows.append({
                "Topic_ID": topic_id,
                "Topic_Name": self.topic_names.get(topic_id, f"Topic {topic_id}"),
                "Count": self.topic_sizes.get(topic_id, 0),
                "Top_Keywords": top_terms
            })
        df = pd.DataFrame(rows)
        return df.sort_values(by="Count", ascending=False).reset_index(drop=True)
