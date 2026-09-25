"""
Topic Coherence & Diversity Metrics (Section 11)
Calculates:
- Topic Diversity (percentage of unique words in top-k terms across all topics)
- Topic Coherence (NPMI / pairwise co-occurrence coherence approximation)
"""

from typing import List, Dict, Any, Set
import numpy as np
from collections import Counter
import math

class TopicMetrics:
    @staticmethod
    def topic_diversity(topics_top_words: List[List[str]], top_k: int = 10) -> float:
        """
        Computes topic diversity: the fraction of unique words in the top-k words
        across all topics. 0.0 means all topics share same words, 1.0 means completely distinct.
        """
        if not topics_top_words:
            return 0.0

        all_words = []
        for words in topics_top_words:
            all_words.extend(words[:top_k])

        if not all_words:
            return 0.0

        unique_words = len(set(all_words))
        return round(unique_words / len(all_words), 4)

    @staticmethod
    def topic_coherence_c_v(topics_top_words: List[List[str]], corpus_texts: List[str], top_k: int = 10) -> float:
        """
        Computes NPMI-based coherence across top-k topic terms using the input corpus.
        Returns average topic coherence score.
        """
        # Tokenize corpus into sets of words per document
        doc_word_sets = [set(text.lower().split()) for text in corpus_texts]
        total_docs = len(doc_word_sets)
        if total_docs == 0:
            return 0.0

        topic_coherences = []

        for words in topics_top_words:
            top_words = words[:top_k]
            pairs_npmi = []

            for i in range(len(top_words)):
                for j in range(i + 1, len(top_words)):
                    w1 = top_words[i]
                    w2 = top_words[j]

                    # Document frequency
                    count_w1 = sum(1 for doc in doc_word_sets if w1 in doc)
                    count_w2 = sum(1 for doc in doc_word_sets if w2 in doc)
                    count_w1_w2 = sum(1 for doc in doc_word_sets if (w1 in doc and w2 in doc))

                    if count_w1_w2 == 0:
                        npmi = -1.0
                    else:
                        p_w1 = count_w1 / total_docs
                        p_w2 = count_w2 / total_docs
                        p_w1_w2 = count_w1_w2 / total_docs

                        pmi = math.log(p_w1_w2 / (p_w1 * p_w2 + 1e-12) + 1e-12)
                        npmi = pmi / (-math.log(p_w1_w2 + 1e-12))

                    pairs_npmi.append(npmi)

            if pairs_npmi:
                topic_coherences.append(np.mean(pairs_npmi))

        return round(float(np.mean(topic_coherences)), 4) if topic_coherences else 0.0
