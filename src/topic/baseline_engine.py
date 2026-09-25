"""
Baseline Topic Modeling Engine (Section 10 & 11)
Implements LDA (Latent Dirichlet Allocation) and NMF (Non-negative Matrix Factorization)
for rigorous baseline comparison against Semantic c-TF-IDF / BERTopic.
"""

from typing import List, Dict, Any, Tuple
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation, NMF

class BaselineTopicEngine:
    def __init__(self, num_topics=8, random_state=42):
        self.num_topics = num_topics
        self.random_state = random_state

    def fit_lda(self, documents: List[str]) -> Dict[str, Any]:
        """Trains Latent Dirichlet Allocation (LDA) baseline."""
        vectorizer = CountVectorizer(stop_words="english", max_features=2000, max_df=0.90, min_df=2)
        X = vectorizer.fit_transform(documents)
        feature_names = vectorizer.get_feature_names_out()

        lda = LatentDirichletAllocation(
            n_components=self.num_topics,
            random_state=self.random_state,
            max_iter=15,
            learning_method="online"
        )
        doc_topics = lda.fit_transform(X)

        topics_dict = {}
        for topic_idx, topic in enumerate(lda.components_):
            top_features_ind = topic.argsort()[:-11:-1]
            top_features = [feature_names[i] for i in top_features_ind]
            topics_dict[topic_idx] = {
                "top_words": top_features,
                "name": f"LDA Topic {topic_idx + 1}: " + " / ".join(top_features[:3])
            }

        return {
            "model_type": "LDA",
            "topics": topics_dict,
            "perplexity": round(float(lda.perplexity(X)), 2),
            "doc_topic_matrix": doc_topics
        }

    def fit_nmf(self, documents: List[str]) -> Dict[str, Any]:
        """Trains Non-negative Matrix Factorization (NMF) baseline."""
        vectorizer = TfidfVectorizer(stop_words="english", max_features=2000, max_df=0.90, min_df=2)
        X = vectorizer.fit_transform(documents)
        feature_names = vectorizer.get_feature_names_out()

        nmf = NMF(
            n_components=self.num_topics,
            random_state=self.random_state,
            max_iter=200,
            init="nndsvda"
        )
        doc_topics = nmf.fit_transform(X)

        topics_dict = {}
        for topic_idx, topic in enumerate(nmf.components_):
            top_features_ind = topic.argsort()[:-11:-1]
            top_features = [feature_names[i] for i in top_features_ind]
            topics_dict[topic_idx] = {
                "top_words": top_features,
                "name": f"NMF Topic {topic_idx + 1}: " + " / ".join(top_features[:3])
            }

        return {
            "model_type": "NMF",
            "topics": topics_dict,
            "reconstruction_err": round(float(nmf.reconstruction_err_), 3),
            "doc_topic_matrix": doc_topics
        }
