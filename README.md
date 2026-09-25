# Multilingual Course Feedback Intelligence

**3rd-Year Data Science Capstone Project**  
*Aspect-based sentiment analysis, topic modeling, and topic-drift analytics for student course feedback across English, Hindi, and Hinglish.*

---

## 🌟 Executive Overview
Traditional course evaluation systems rely heavily on a single numerical score (e.g. `3.8 / 5.0`), obscuring *why* students evaluated a course the way they did. Given compound feedback such as:
> *"Teacher explains concepts well but the assignments are too difficult and the lectures are too fast"*

This system decomposes unstructured student responses into granular per-aspect verdicts:
- **Teaching Quality**: `Positive` (94% conf)
- **Assignments**: `Negative` (91% conf)
- **Lecture Pace**: `Negative` (88% conf)

It tracks these sentiments across **English, Hindi (Devanagari), and Romanized Hinglish**, discovers underlying semantic discussion topics via **c-TF-IDF / BERTopic**, traces **topic drift across semesters** (Emerging, Declining, Persistent, New), and surfaces non-hardcoded dynamic statistical insights on an interactive **Streamlit Dashboard**.

---

## 🏗️ Architecture & Modules

```
c:\Users\bhara\capstron\
├── data/
│   ├── raw/
│   │   └── course_feedback_raw.csv         # 2,200+ multilingual benchmark records
│   ├── processed/
│   │   └── course_feedback_processed.csv   # Cleaned, tokenized, and tagged data
│   └── course_feedback.db                  # Normalized SQLite database (4 tables)
├── src/
│   ├── preprocessing/
│   │   └── cleaner.py                      # Negation preservation ('not', 'nahi', 'नहीं', emojis)
│   ├── language/
│   │   ├── detector.py                     # Trilingual detector (English, Hindi, Hinglish)
│   │   └── normalizer.py                   # Pipeline A (Translate) vs Pipeline B (Multilingual)
│   ├── sentiment/
│   │   ├── classifier.py                   # Pos/Neg/Neu classification with confidence & polarity
│   │   └── evaluator.py                    # Accuracy, Precision, Recall, F1, Confusion Matrix
│   ├── aspect/
│   │   ├── detector.py                     # 12 Course Aspects detector
│   │   └── aspect_sentiment.py             # Clause-level aspect sentiment extraction
│   ├── topic/
│   │   ├── bertopic_engine.py              # c-TF-IDF clustering with human-readable naming
│   │   ├── baseline_engine.py              # LDA & NMF baseline comparison models
│   │   └── coherence.py                    # Topic Coherence (c_v) and Diversity evaluation
│   ├── drift/
│   │   └── drift_analyzer.py               # Temporal bucketing & drift classification
│   ├── insights/
│   │   └── generator.py                    # Non-hardcoded dynamic statistical insight synthesis
│   ├── database/
│   │   └── db_manager.py                   # SQLite schema & high-speed indexed queries
│   └── data_generation/
│       └── generate_synthetic.py           # Realistic multilingual dataset generator
├── app.py                                  # Streamlit web application (All 6 PRD views + sandbox)
├── run_pipeline.py                         # End-to-end CLI pipeline runner
├── evaluate.py                             # Evaluation benchmark suite (PRD §11)
├── styles.css                              # Glassmorphic custom CSS styling
└── requirements.txt                        # Dependency specifications
```

---

## 🎯 Supported 12 Course Aspects
1. **Teaching Quality** (clarity, methodology, pedagogy, instructor engagement)
2. **Course Content** (syllabus modernity, theoretical rigor, practical balance)
3. **Assignments** (workload, problem clarity, deadlines, frequency)
4. **Exams** (midterm/final fairness, question alignment, time pressure)
5. **Difficulty** (pacing curve, prerequisites, complexity)
6. **Lecture Pace** (speed, rushing through slides, tempo)
7. **Faculty Support** (office hours, doubts resolution, responsiveness)
8. **Practical Sessions** (laboratory exercises, hands-on coding, manuals)
9. **Projects** (capstone implementation, mentor review, team fairness)
10. **Study Material** (slides quality, reference textbooks, portal uploads)
11. **Infrastructure** (lab PCs, Wi-Fi connectivity, GPUs, AC, projectors)
12. **Evaluation** (marking fairness, rubric transparency, score delays)

---

## ⚡ Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Full End-to-End Pipeline
```bash
python run_pipeline.py
```
This generates the benchmark dataset, runs preprocessing, language detection, ABSA, topic modeling, drift analysis, dynamic insight generation, and populates `data/course_feedback.db`.

### 3. Run the Evaluation Suite
```bash
python evaluate.py
```
Outputs validation accuracy, Macro F1, aspect precision/recall, topic coherence ($c_v$), and Pipeline A vs B benchmarks to `evaluation_report.json`.

### 4. Launch the Interactive Dashboard
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📊 Dashboard Views
1. **🏛️ Overview**: Executive KPIs, total feedback, average rating, sentiment donut, language breakdown, and dynamic statistical insights.
2. **📊 Sentiment Analysis**: Course-by-course stacked breakdowns, temporal trends, cross-language sentiment comparison, polarity histograms.
3. **🎯 Aspect Breakdown (ABSA)**: 12-aspect sentiment distribution, top strengths & pain points, interactive Course vs Aspect net sentiment heatmap.
4. **🧠 Topic Modeling**: Discovered topics with human-readable titles, interactive c-TF-IDF keyword inspector, and BERTopic vs LDA/NMF comparison.
5. **📈 Topic Drift Analytics**: Interactive streamgraphs/trendlines across semesters with Emerging (⚡), Declining (📉), Persistent (🔄), and New (✨) trajectory classifications.
6. **🔍 Feedback Explorer**: Multi-filter drilldown (< 3 clicks) by Course, Semester, Language, Sentiment, Aspect, and Topic with highlighted aspect cards.
7. **⚡ Live Predictor Sandbox**: Real-time interactive playground to test any new feedback in English, Hindi, or Hinglish with live language detection, translation preview, aspect extraction, and topic assignment.
