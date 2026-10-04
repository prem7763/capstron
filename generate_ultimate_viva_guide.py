"""
generate_ultimate_viva_guide.py
Generates the Ultimate, Comprehensive, 100% Complete Viva Defense & Project Master Guide PDF
for Prem Choudhary (Multilingual Course Feedback Intelligence).
Includes:
- 1-Minute Elevator Pitch
- Full Architectural Deep Dive (All 9 Phases)
- Codebase Walkthrough (what each file does)
- 12 Aspects & Taxonomy breakdown
- Machine Learning & NLP Theory (LinearSVC, Platt Scaling, c-TF-IDF, Negation Preservation)
- Top 25 Most Expected Viva Questions with Killer Hinglish & English Answers
- Examiner Trap / Cross-Questioning Defense Guide
- Live Demo Protocol (Step-by-step click guide)
- Formula & Stats Cheat-Sheet (Numbers to memorise)
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))
        
        # Header (pages after cover)
        if self._pageNumber > 1:
            self.drawString(54, 752, "MULTILINGUAL COURSE FEEDBACK INTELLIGENCE — ULTIMATE VIVA DEFENSE GUIDE")
            self.drawRightString(558, 752, "TY BSc. DATA SCIENCE (SEM VI)")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(54, 745, 558, 745)
        
        # Footer
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#64748B"))
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 38, page_str)
        self.drawString(54, 38, "Student: Prem Choudhary (TDDS009A) • Guide: Dr. Beena Kapadia • KES' Shroff College")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(54, 50, 558, 50)
        
        self.restoreState()

def build_pdf(filename="Multilingual_Course_Feedback_Intelligence_Ultimate_Viva_Guide.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    c_primary = colors.HexColor("#1E3A8A")   # Navy 900
    c_accent = colors.HexColor("#2563EB")    # Royal Blue
    c_dark = colors.HexColor("#0F172A")      # Slate 900
    c_sub = colors.HexColor("#334155")       # Slate 700
    c_q = colors.HexColor("#991B1B")         # Dark Crimson Red for Questions
    c_ans = colors.HexColor("#065F46")       # Dark Emerald Green for Answers
    c_box = colors.HexColor("#F1F5F9")       # Slate 100

    title_style = ParagraphStyle(
        'MainTitle', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=22, leading=26,
        textColor=c_primary, spaceAfter=6
    )
    sub_style = ParagraphStyle(
        'SubTitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=11, leading=15,
        textColor=c_sub, spaceAfter=12
    )
    h1_style = ParagraphStyle(
        'H1', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=14, leading=18,
        textColor=c_primary, spaceBefore=12, spaceAfter=6, keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'H2', parent=styles['Heading2'],
        fontName='Helvetica-Bold', fontSize=11, leading=15,
        textColor=c_accent, spaceBefore=8, spaceAfter=4, keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=13.5,
        textColor=c_dark, spaceAfter=5
    )
    body_bold = ParagraphStyle(
        'BodyBold', parent=body_style,
        fontName='Helvetica-Bold'
    )
    qa_q = ParagraphStyle(
        'QA_Q', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9.5, leading=13.5,
        textColor=c_q, spaceBefore=7, spaceAfter=2, keepWithNext=True
    )
    qa_ans = ParagraphStyle(
        'QA_Ans', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=13.5,
        textColor=c_ans, spaceAfter=6
    )
    box_style = ParagraphStyle(
        'BoxP', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=8.5, leading=12.5,
        textColor=colors.HexColor("#1E293B")
    )

    story = []

    # ================= COVER BANNER =================
    story.append(Paragraph("Multilingual Course Feedback Intelligence", title_style))
    story.append(Paragraph("<b>MASTER VIVA DEFENSE & TECHNICAL PREPARATION GUIDE</b><br/>"
                           "<i>Aspect-Based Sentiment Analysis (ABSA), Temporal Topic Drift, Trilingual Negation Handling & Full-Stack Deployment</i>", sub_style))

    meta_table = [
        [
            Paragraph("<b>Candidate Name:</b> Mr. Prem Choudhary", body_style),
            Paragraph("<b>Seat / Roll No:</b> TDDS009A (Div A)", body_style)
        ],
        [
            Paragraph("<b>Degree & Semester:</b> TY BSc. Data Science (Sem VI)", body_style),
            Paragraph("<b>Academic Year:</b> 2026 – 2027", body_style)
        ],
        [
            Paragraph("<b>Project Guide:</b> Dr. Beena Kapadia", body_style),
            Paragraph("<b>HOD & Vice Principal:</b> Dr. Vishesh Shrivastava", body_style)
        ],
        [
            Paragraph("<b>Coordinator:</b> Mr. Manish Singh", body_style),
            Paragraph("<b>Institution:</b> KES' Shroff College, Kandivali (W), Mumbai", body_style)
        ]
    ]
    t_m = Table(meta_table, colWidths=[256, 256])
    t_m.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#BFDBFE")),
        ('PADDING', (0,0), (-1,-1), 4.5),
    ]))
    story.append(t_m)
    story.append(Spacer(1, 10))

    # ================= SECTION 1: 1-MINUTE ELEVATOR PITCH =================
    story.append(Paragraph("1. The 1-Minute Project Pitch (Examiner ko shuruat me kya bolna hai?)", h1_style))
    pitch_box = [
        [Paragraph(
            "<b>Examiner Question:</b> <i>'Prem, please introduce your project in 1 minute and tell us what you have built.'</i><br/><br/>"
            "<b>YOUR EXACT ANSWER (Bolne ka script):</b><br/>"
            "\"Good morning / afternoon Respected Examiners. My capstone project is titled <b>'Multilingual Course Feedback Intelligence'</b>.<br/>"
            "In modern higher education, colleges collect student feedback but compress everything into a single blended score like 3.8 out of 5. "
            "This numerical score fails to diagnose <b>why</b> students are dissatisfied. For example, a student might write in Hinglish: "
            "<i>'Professor sir concepts bohot acche samjhate hain lekin lab PCs crash ho rahe hain aur assignments bohot tough hain'</i>.<br/>"
            "Conventional systems treat this as average or mixed. To solve this, I developed a production-ready AI intelligence platform that:<br/>"
            "1. <b>Natively supports Trilingual Feedback:</b> English, Devanagari Hindi, and code-mixed Romanized Hinglish.<br/>"
            "2. <b>Preserves Negation Operators:</b> Tokens like 'nahi', 'mat', and 'not' are preserved to avoid polarity corruption.<br/>"
            "3. <b>Decomposes feedback into 12 Pedagogical Aspects:</b> Using localized clause-level extraction (Teaching Quality, Labs, Pace, Exams, etc.).<br/>"
            "4. <b>Tracks Longitudinal Topic Drift:</b> Uses class-based TF-IDF (c-TF-IDF / BERTopic) across 6 sequential academic semesters.<br/>"
            "5. <b>Deployed Full-Stack:</b> Powered by a high-throughput FastAPI REST backend (<20ms latency), normalized SQLite 3NF storage, "
            "and an interactive glassmorphic web dashboard with real-time feedback CRUD and a Live AI Sandbox.<br/>"
            "The model achieves an outstanding <b>98.45% sentiment accuracy</b> and <b>99.79% aspect extraction F1</b>.\"",
            box_style
        )]
    ]
    t_pitch = Table(pitch_box, colWidths=[512])
    t_pitch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF3C7")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#F59E0B")),
        ('PADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_pitch)
    story.append(Spacer(1, 10))

    # ================= SECTION 2: ARCHITECTURE & 9 PHASES =================
    story.append(Paragraph("2. End-to-End System Architecture (The 9 Pipeline Stages)", h1_style))
    story.append(Paragraph(
        "Aapka project 9 independent modular stages me divided hai. Examiner agar pooche ki code kaise structured hai, toh ye 9 phases explain karna:", body_style
    ))

    arch_rows = [
        [Paragraph("<b>Phase</b>", body_style), Paragraph("<b>Component / Source File</b>", body_style), Paragraph("<b>Key Technical Functionality & Algorithms</b>", body_style)],
        [Paragraph("1. Ingestion", body_style), Paragraph("<code>src/data_generation/</code>", body_style), Paragraph("Synthesizes/ingests 2,200 benchmark evaluation records across 8 university courses and 6 sequential academic semesters in English, Hindi, and Hinglish.", body_style)],
        [Paragraph("2. Preprocessing", body_style), Paragraph("<code>src/preprocessing/cleaner.py</code>", body_style), Paragraph("Cleans HTML/URLs, maps emojis to sentiment tokens, and strictly enforces <b>Negation Preservation</b> ('nahi', 'mat', 'not') with token binding.", body_style)],
        [Paragraph("3. Language Identification", body_style), Paragraph("<code>src/language/detector.py</code>", body_style), Paragraph("Unicode script inspection (\u0900-\u097F for Hindi) + Hinglish lexical density scoring (tokens: <i>samajh, padhate, accha, tough, sir</i>).", body_style)],
        [Paragraph("4. Normalization", body_style), Paragraph("<code>src/language/normalizer.py</code>", body_style), Paragraph("Compares <b>Pipeline A</b> (transliteration / phonetic normalization at 28,640 rec/s) vs <b>Pipeline B</b> (subword character n-grams).", body_style)],
        [Paragraph("5. Calibrated Sentiment", body_style), Paragraph("<code>src/sentiment/classifier.py</code>", body_style), Paragraph("Calibrated Linear Support Vector Classifier (LinearSVC) with Platt Scaling (Isotonic Calibration). Achieves <b>98.45% accuracy</b>, 98.24% F1.", body_style)],
        [Paragraph("6. 12-Aspect ABSA", body_style), Paragraph("<code>src/aspect/extractor.py</code>", body_style), Paragraph("Localized syntactic clause window parsing across 12 pedagogical dimensions with independent confidence. Achieves <b>99.79% F1</b>.", body_style)],
        [Paragraph("7. Topic Modeling", body_style), Paragraph("<code>src/topic/bertopic_engine.py</code>", body_style), Paragraph("TruncatedSVD + KMeans clustering + Class-based TF-IDF (c-TF-IDF). Generates human-readable cluster titles. Benchmarked against LDA and NMF.", body_style)],
        [Paragraph("8. Temporal Drift", body_style), Paragraph("<code>src/drift/drift_analyzer.py</code>", body_style), Paragraph("Longitudinal OLS regression slopes across 6 semesters. Classifies trends into <b>Emerging (⚡)</b>, <b>Declining (📉)</b>, <b>Persistent (🔄)</b>, and <b>New (✨)</b>.", body_style)],
        [Paragraph("9. API & Dual UI", body_style), Paragraph("<code>server.py</code> & <code>frontend/</code>", body_style), Paragraph("FastAPI asynchronous REST microservices (<20ms latency), normalized SQLite 3NF relational database, and dual-theme glassmorphic Web UI + Streamlit.", body_style)]
    ]
    t_arch = Table(arch_rows, colWidths=[65, 140, 307])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('PADDING', (0,0), (-1,-1), 3.5),
    ]))
    story.append(t_arch)

    story.append(PageBreak())

    # ================= SECTION 3: CORE NLP INNOVATIONS =================
    story.append(Paragraph("3. Deep-Dive: Core NLP Innovations & Secret Weapons", h1_style))
    story.append(Paragraph(
        "Examiners always look for what makes your NLP system novel and mathematically sound. These are your 4 core technical pillars:", body_style
    ))

    story.append(Paragraph("A. Negation Preservation (The Polarity Inversion Shield)", h2_style))
    story.append(Paragraph(
        "<b>Concept:</b> Standard NLP pipelines remove stopwords like 'not', 'no', 'never'. In academic reviews, this causes catastrophic errors:<br/>"
        "• Original: <i>'Professor is not clear and questions were not easy.'</i><br/>"
        "• Without negation: <i>'professor clear questions easy'</i> $\\rightarrow$ <b>Classified as POSITIVE (100% wrong)!</b><br/>"
        "<b>Our Engineering Solution:</b> In <code>cleaner.py</code>, we explicitly preserve English negations ('not', 'never', 'hardly', 'barely') "
        "and Hindi/Hinglish negations ('nahi', 'nahin', 'mat', 'bina', 'नहीं', 'ना'). When tokenized, a 3-token forward context window binds the negation "
        "to the adjacent adjective (e.g. <code>not_clear</code>, <code>nahi_accha</code>) and flips the sentiment polarity.", body_style
    ))

    story.append(Paragraph("B. Trilingual Code-Mixed Language Identification", h2_style))
    story.append(Paragraph(
        "In Indian colleges, students naturally mix English and Hindi in Roman script. Our <code>LanguageDetector</code> uses a two-tier gate:<br/>"
        "1. <b>Devanagari Unicode Block:</b> If characters between Unicode <code>\\u0900</code> and <code>\\u097F</code> exceed 15% of alphabetical characters, it is classified as <b>Hindi</b>.<br/>"
        "2. <b>Hinglish Lexicon Density:</b> If text is written in Latin characters but contains markers from our 150+ colloquial Hinglish dictionary (e.g., <i>samajh, padhate, accha, bohot, lekin, tha, hai, sir</i>) exceeding 8% token density, it is classified as <b>Hinglish</b>.<br/>"
        "3. <b>English Default:</b> Otherwise classified as standard <b>English</b>.", body_style
    ))

    story.append(Paragraph("C. Calibrated Probability via Platt Scaling (LinearSVC)", h2_style))
    story.append(Paragraph(
        "Standard Linear Support Vector Classifiers output geometric distance margins from the separating hyperplane ($w^T x + b$), NOT true probabilities. "
        "To provide reliable confidence meters in our web UI, we wrap LinearSVC inside <b>CalibratedClassifierCV</b> using Platt Scaling (sigmoid link function):<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>P(y = 1 | f) = 1 / (1 + exp(A × f + B))</b><br/>"
        "This guarantees that when the system predicts 90% confidence, the empirical correctness is truly 90%, achieving a near-zero Brier calibration loss (0.0180).", body_style
    ))

    story.append(Paragraph("D. Class-Based TF-IDF (c-TF-IDF / BERTopic)", h2_style))
    story.append(Paragraph(
        "Standard TF-IDF treats each student review as an isolated document. In contrast, <b>c-TF-IDF</b> concatenates all student reviews belonging to the same cluster into a single composite document. "
        "The c-TF-IDF score of word $t$ in cluster $c$ is formulated as:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>W(t, c) = TF(t, c) × log(1 + Avg_Words / Freq(t))</b><br/>"
        "This directly surfaces words that are uniquely characteristic of that discussion theme (e.g. 'lab PCs', 'assignment deadlines') and enables automated semantic naming.", body_style
    ))

    # ================= SECTION 4: THE 12 ASPECTS =================
    story.append(Paragraph("4. The 12 Pedagogical Dimensions Evaluated", h1_style))
    aspects_table_data = [
        [Paragraph("<b>Aspect Dimension</b>", body_style), Paragraph("<b>Evaluated Pedagogical Area</b>", body_style), Paragraph("<b>Sample Trilingual Keyword Triggers</b>", body_style)],
        [Paragraph("1. Teaching Quality", body_style), Paragraph("Faculty clarity, explanation skills, lecture engagement", body_style), Paragraph("teach, explanation, methodology, padhate, shikshak, samjhate", body_style)],
        [Paragraph("2. Course Content", body_style), Paragraph("Syllabus modernity, theoretical vs practical depth", body_style), Paragraph("syllabus, curriculum, topics, theory, pathyakram, concepts", body_style)],
        [Paragraph("3. Assignments", body_style), Paragraph("Homework workload, clarity of questions, deadlines", body_style), Paragraph("assignment, homework, deadline, submission, grihakarya", body_style)],
        [Paragraph("4. Exams", body_style), Paragraph("Midterm and final fairness, coverage, time duration", body_style), Paragraph("exam, midterm, final, quiz, test paper, pariksha", body_style)],
        [Paragraph("5. Difficulty", body_style), Paragraph("Cognitive rigor, prerequisite curve, academic hardness", body_style), Paragraph("difficulty, hard, brutal, challenging, mushkil, kathan, simple", body_style)],
        [Paragraph("6. Lecture Pace", body_style), Paragraph("Delivery speed, rushing through slides, tempo", body_style), Paragraph("pace, speed, fast, rush, rushed, tezi, dhire, bhagaya", body_style)],
        [Paragraph("7. Faculty Support", body_style), Paragraph("Office hours accessibility, doubt clearing, mentorship", body_style), Paragraph("office hours, doubts, mentor, support, sankha, guidance", body_style)],
        [Paragraph("8. Practical Sessions", body_style), Paragraph("Hands-on coding labs, experiments, lab sheets", body_style), Paragraph("lab, practicals, coding, hands-on, prayogshala, exercises", body_style)],
        [Paragraph("9. Projects", body_style), Paragraph("Capstone implementation, team collaboration, reviews", body_style), Paragraph("project, capstone, team work, group project, portfolio", body_style)],
        [Paragraph("10. Study Material", body_style), Paragraph("Lecture notes, slide decks, textbook quality, portal", body_style), Paragraph("notes, slides, textbook, portal, reading, repository", body_style)],
        [Paragraph("11. Infrastructure", body_style), Paragraph("Lab PCs, Wi-Fi speed, GPUs, projector, AC, hardware", body_style), Paragraph("lab pc, pcs, wifi, internet, crash, projector, hardware", body_style)],
        [Paragraph("12. Evaluation", body_style), Paragraph("Grading fairness, rubric transparency, score delays", body_style), Paragraph("grading, marks, rubric, evaluation, checking, ank, result", body_style)]
    ]
    t_asp = Table(aspects_table_data, colWidths=[100, 205, 207])
    t_asp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('PADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_asp)

    story.append(PageBreak())

    # ================= SECTION 5: DATABASE ARCHITECTURE =================
    story.append(Paragraph("5. Relational Database Architecture (SQLite 3NF Schema)", h1_style))
    story.append(Paragraph(
        "Examiners frequently test relational database concepts. Your system stores data in a normalized Third Normal Form (3NF) SQLite database "
        "(<code>data/course_feedback.db</code>). Here is the exact schema and table relationships:", body_style
    ))

    db_rows = [
        [Paragraph("<b>Table Name</b>", body_style), Paragraph("<b>Key Columns & Data Types</b>", body_style), Paragraph("<b>Relationship & Integrity Rules</b>", body_style)],
        [
            Paragraph("<b>1. Feedback</b>", body_style),
            Paragraph("<code>feedback_id</code> (PK, Text)<br/><code>student_id</code> (Hashed, Text)<br/><code>course_id</code> (CS101..WD102)<br/><code>semester</code> (Sem 1..6)<br/><code>rating</code> (1..5)<br/><code>feedback_text</code> (Raw)<br/><code>cleaned_text</code> (Cleaned)", body_style),
            Paragraph("Primary parent entity. Stores anonymous student feedback submissions. Indexed on <code>course_id</code>, <code>semester</code>, and <code>rating</code> for sub-10ms query execution.", body_style)
        ],
        [
            Paragraph("<b>2. Sentiment</b>", body_style),
            Paragraph("<code>sentiment_id</code> (PK, Int)<br/><code>feedback_id</code> (FK, Text)<br/><code>sentiment</code> (Pos/Neg/Neu)<br/><code>confidence</code> (Float, 0..1)<br/><code>polarity_score</code> (-1.0..+1.0)", body_style),
            Paragraph("<b>1-to-1 Relationship</b> with Feedback. Enforces <code>ON DELETE CASCADE</code> so deleting a feedback record purges its sentiment metrics automatically.", body_style)
        ],
        [
            Paragraph("<b>3. Aspect</b>", body_style),
            Paragraph("<code>aspect_id</code> (PK, Int)<br/><code>feedback_id</code> (FK, Text)<br/><code>aspect</code> (One of 12)<br/><code>sentiment</code> (Pos/Neg/Neu)<br/><code>confidence</code> (Float)<br/><code>evidence_snippet</code> (Clause Text)", body_style),
            Paragraph("<b>1-to-Many Relationship</b> with Feedback. A single compound review can have multiple rows (e.g. Teaching Quality = +ve, Infrastructure = -ve).", body_style)
        ],
        [
            Paragraph("<b>4. Topic</b>", body_style),
            Paragraph("<code>topic_entry_id</code> (PK, Int)<br/><code>feedback_id</code> (FK, Text)<br/><code>topic_id</code> (Cluster Int)<br/><code>topic_name</code> (Human-readable)<br/><code>probability</code> (Float)", body_style),
            Paragraph("<b>1-to-1 Relationship</b> with Feedback. Stores the c-TF-IDF / BERTopic cluster assignment and probability score.", body_style)
        ]
    ]
    t_db = Table(db_rows, colWidths=[90, 200, 222])
    t_db.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_db)

    # ================= SECTION 6: BENCHMARKS & STATS =================
    story.append(Spacer(1, 10))
    story.append(Paragraph("6. Key Project Numbers & Verification Benchmarks", h1_style))
    story.append(Paragraph("Ye numbers aapko muh-zubani (memorized) yaad hone chahiye viva ke liye:", body_style))

    num_rows = [
        [Paragraph("<b>Metric / Benchmark</b>", body_style), Paragraph("<b>Target Threshold</b>", body_style), Paragraph("<b>Achieved Performance</b>", body_style), Paragraph("<b>Key Significance</b>", body_style)],
        [Paragraph("Overall Sentiment Accuracy", body_style), Paragraph(">= 85.0%", body_style), Paragraph("<b>98.45%</b>", body_style), Paragraph("Calibrated LinearSVC outperforming Naive Bayes & Random Forest.", body_style)],
        [Paragraph("Sentiment Macro F1", body_style), Paragraph(">= 85.0%", body_style), Paragraph("<b>98.24%</b>", body_style), Paragraph("Balances positive, neutral, and negative class distributions.", body_style)],
        [Paragraph("Aspect Extraction Precision", body_style), Paragraph(">= 80.0%", body_style), Paragraph("<b>100.00%</b>", body_style), Paragraph("Zero false aspect assignments across 12 dimensions.", body_style)],
        [Paragraph("Aspect Extraction Recall", body_style), Paragraph(">= 80.0%", body_style), Paragraph("<b>99.59%</b>", body_style), Paragraph("Near-perfect identification of student discussion points.", body_style)],
        [Paragraph("Aspect Extraction Macro F1", body_style), Paragraph(">= 80.0%", body_style), Paragraph("<b>99.79%</b>", body_style), Paragraph("State-of-the-art clause-level aspect extraction score.", body_style)],
        [Paragraph("English Sentiment Accuracy", body_style), Paragraph("Diagnostic", body_style), Paragraph("<b>98.81%</b>", body_style), Paragraph("Evaluated across 990 English evaluation records.", body_style)],
        [Paragraph("Hindi Sentiment Accuracy", body_style), Paragraph("Diagnostic", body_style), Paragraph("<b>97.13%</b>", body_style), Paragraph("Evaluated across 440 Devanagari Hindi evaluation records.", body_style)],
        [Paragraph("Hinglish Sentiment Accuracy", body_style), Paragraph("Diagnostic", body_style), Paragraph("<b>98.97%</b>", body_style), Paragraph("Evaluated across 770 code-mixed Romanized Hinglish records.", body_style)],
        [Paragraph("Topic Diversity Score", body_style), Paragraph("High Diversity", body_style), Paragraph("<b>0.880</b>", body_style), Paragraph("Outperforms standard LDA (0.850) and NMF (0.865).", body_style)],
        [Paragraph("Topic Coherence (c_v)", body_style), Paragraph("High Coherence", body_style), Paragraph("<b>0.584</b>", body_style), Paragraph("Semantically cohesive clusters matching academic themes.", body_style)],
        [Paragraph("Pipeline A Normalization Speed", body_style), Paragraph("Real-Time", body_style), Paragraph("<b>28,640 records/sec</b>", body_style), Paragraph("Sub-millisecond latency enabling instant feedback ingestion.", body_style)],
        [Paragraph("REST API Response Latency", body_style), Paragraph("< 100ms", body_style), Paragraph("<b>< 20ms</b>", body_style), Paragraph("FastAPI ASGI async endpoints delivering instant UI updates.", body_style)]
    ]
    t_num = Table(num_rows, colWidths=[130, 85, 95, 202])
    t_num.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('PADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_num)

    story.append(PageBreak())

    # ================= SECTION 7: TOP 25 VIVA QUESTIONS & KILLER ANSWERS =================
    story.append(Paragraph("7. Top 25 Most Expected Viva Questions & Killer Answers", h1_style))
    story.append(Paragraph("Ye questions examiners har saal zaroor poochte hain. Dono Hinglish explanation aur English answer dhyan se padh lo:", body_style))

    viva_qa_full = [
        (
            "Q1: What is the core problem this project solves? (Project ka main aim kya hai?)",
            "Hinglish: Traditional colleges feedback me bas 1 se 5 ka rating lete hain aur average nikal dete hain (jaise 3.8/5). Isse HOD ko ye samajh nahi aata ki student ko dikkat KAHAN hai. Humara project multilingual review text ko padhta hai, 12 aspects me todta hai, aur batata hai ki Teaching acchi hai par Lab infrastructure kharab hai.<br/>"
            "English: Conventional evaluation systems aggregate student ratings into a single uninformative average, concealing root causes. Our platform performs Aspect-Based Sentiment Analysis on trilingual feedback (English, Hindi, Hinglish), isolating 12 pedagogical dimensions with independent sentiment scores and tracking semester topic drift."
        ),
        (
            "Q2: How does Aspect-Based Sentiment Analysis (ABSA) differ from standard Sentiment Analysis?",
            "Hinglish: Standard sentiment pure sentence ko ek label (+ve ya -ve) de deta hai. Lekin student review compound hota hai: 'Sir explains well (+ve), but lab PCs crash (-ve)'. ABSA is sentence ko clause-level pe break karta hai aur Teaching Quality ko Positive aur Infrastructure ko Negative tag karta hai independently.<br/>"
            "English: Document-level sentiment analysis assigns a single global polarity. However, student reviews are compound sentences containing conflicting polarities. ABSA extracts syntactic clause windows, attributing positive sentiment to Teaching Quality while attributing negative sentiment to Infrastructure independently."
        ),
        (
            "Q3: Why is Negation Preservation your project's most critical preprocessing step?",
            "Hinglish: Normal NLP me stopwords ('not', 'nahi', 'no') drop kar diye jaate hain. Agar 'not' drop ho gaya, toh 'Professor is not clear and exam was not easy' ban jayega 'professor clear exam easy' — jo ki POSITIVE dikhayega jabki student gussa tha! Humne 'nahi', 'mat', 'not' preserve kiya aur 3-token window me polarity flip ki.<br/>"
            "English: Standard preprocessing drops negation stopwords. In student feedback, 'not approachable' becomes 'approachable', inverting negative feedback into false positives. We strictly preserve English, Hindi, and Hinglish negation markers and implement a 3-token contextual window that inverts the polarity of subsequent sentiment terms."
        ),
        (
            "Q4: How does your system detect and handle code-mixed Hinglish text?",
            "Hinglish: Hinglish Latin alphabets me likhi Hindi hoti hai (jaise: 'sir concept acche samjhate hain'). Humara LanguageDetector pehle Devanagari script check karta hai (>15% toh Hindi). Agar Latin script hai, toh 150+ Hinglish vocabulary tokens (samajh, padhate, accha, bohot, tha) ki density check karta hai (>8% toh Hinglish).<br/>"
            "English: We implement a two-pass detection module. First, it inspects Unicode character ranges (\\u0900-\\u097F for Devanagari Hindi). For Latin script, it computes lexical token density against a curated Hinglish vocabulary. If density exceeds 8%, it is tagged as Hinglish and routed to phonetic normalization."
        ),
        (
            "Q5: What is the difference between Pipeline A and Pipeline B in Normalization?",
            "Hinglish: Pipeline A Hinglish tokens ko standard English me transliterate/map karta hai (jaise 'bohot accha' -> 'very good'). Pipeline B character subwords (3-5 grams) banata hai. Humne dono ko benchmark kiya: Pipeline A ne 28,640 records/sec ka ultra-fast throughput diya aur downstream ABSA me highest accuracy di, isliye Pipeline A default hai.<br/>"
            "English: Pipeline A applies lexicon-based phonetic translation that maps colloquial Hinglish tokens to standardized English semantic anchors at 28,640 records/second. Pipeline B generates language-agnostic character n-grams. Pipeline A was selected as primary due to superior downstream topic interpretability."
        ),
        (
            "Q6: Why did you use LinearSVC instead of Random Forest, Naive Bayes, or Deep Neural Networks?",
            "Hinglish: TF-IDF n-gram text representations extremely high-dimensional aur sparse hote hain (10,000+ features). Support Vector Classifiers (LinearSVC) high-dimensional spaces me mathematically optimal separating hyperplane draw karte hain aur overfit nahi hote. Naive Bayes feature independence assume karta hai jo language me fail hota hai.<br/>"
            "English: TF-IDF feature spaces are high-dimensional and sparse. LinearSVC is mathematically optimal for finding the maximum-margin hyperplane in high dimensions with low computational overhead. Naive Bayes violates conditional independence on compound clauses, while Deep Neural Networks require unnecessary compute for tabular text classification."
        ),
        (
            "Q7: LinearSVC does not output probabilities. How did you compute confidence scores? (Platt Scaling)",
            "Hinglish: LinearSVC bas geometric distance deta hai. Isko probability banane ke liye humne Platt Scaling (CalibratedClassifierCV) use kiya. Ye sigmoid function lagakar distance margin ko calibrated probability (0 se 100%) me convert karta hai jisse Brier score 0.0180 achieve hua.<br/>"
            "English: LinearSVC outputs uncalibrated decision function margins. We wrapped the model in CalibratedClassifierCV using Platt Scaling (sigmoid link function). This fits a logistic regression over the decision margins, producing well-calibrated posterior probabilities with a near-zero Brier loss of 0.0180."
        ),
        (
            "Q8: What is Class-Based TF-IDF (c-TF-IDF) and how does it differ from standard TF-IDF?",
            "Hinglish: Normal TF-IDF har review ko alag document maanta hai. c-TF-IDF pure cluster ke saare reviews ko jodkar ek bada document bana deta hai. Fir formula W = TF × log(1 + Avg_Words / Freq) se us cluster ke sabse unique shabd extract karke human-readable topic name assign karta hai.<br/>"
            "English: Standard TF-IDF calculates term frequency per document. In c-TF-IDF, all documents belonging to a cluster are concatenated into a single class document. The term frequency within the cluster is weighted against global frequency across all clusters, extracting the most distinctive keywords characteristic of that topic."
        ),
        (
            "Q9: What is Topic Drift and how are topic trajectories categorized?",
            "Hinglish: Sem 1 se Sem 6 tak students ki baatein badal jaati hain. Shuru me 'Lecture Pace' hota hai, baad me 'Placement Prep'. Is shift ko Topic Drift kehte hain. Humne 4 categories banayi hain: Emerging (>25% growth), Declining (>25% drop), Persistent (stable presence), aur New (shuru me 0% tha, baad me introduce hua).<br/>"
            "English: Topic drift represents temporal shifts in student discussion patterns over consecutive semesters. By bucketing feedback by semester and calculating relative percentage shares, we categorize topics into Emerging (>25% growth), Declining (>25% drop), Persistent (sustained presence), and New (zero initial presence)."
        ),
        (
            "Q10: Why did you compare c-TF-IDF with LDA and NMF baselines?",
            "Hinglish: PRD aur scientific research standard ke hisaab se hume dikhana tha ki humara model purane algorithms se better hai. LDA probabilistic model hai aur NMF matrix factorization. c-TF-IDF ne 0.880 Topic Diversity aur 0.584 Coherence diya, jo LDA (0.850 diversity) aur NMF (0.865) dono se superior hai.<br/>"
            "English: Rigorous academic benchmarking requires comparative evaluation against classical generative models (LDA) and matrix factorization (NMF). c-TF-IDF achieved superior Topic Diversity (0.880) and Topic Coherence (0.584), while providing automated human-readable naming without manual cluster labeling."
        ),
        (
            "Q11: Explain your SQLite database schema and normalization.",
            "Hinglish: Database 3rd Normal Form (3NF) me hai with 4 tables: Feedback (main text & course info), Sentiment (1:1 relation), Aspect (1:Many relation jahan ek feedback ke 2-3 aspects alag rows bante hain), aur Topic (1:1 relation). Foreign keys pe index aur cascade deletion lagaya hai.<br/>"
            "English: We implemented a 3NF relational schema across four tables: Feedback, Sentiment (1:1), Aspect (1:N), and Topic (1:1). Foreign key cascade deletion ensures referential integrity when feedback records are deleted via CRUD, while B-tree indexes guarantee sub-10ms query execution."
        ),
        (
            "Q12: How does the Interactive Live AI Sandbox work in your dashboard?",
            "Hinglish: Sandbox tab me koi bhi naya review type kar sakta hai. Backend 4 steps me inference execute karta hai: (1) Language detect karta hai with confidence, (2) Normalized English preview dikhata hai, (3) Overall sentiment meter display karta hai, aur (4) 12 aspects me se specific aspect badges isolate karke highlight karta hai.<br/>"
            "English: The Live Sandbox allows real-time inference on arbitrary user feedback. The backend executes a 4-step NLP pipeline: language script identification, normalized English translation, calibrated sentiment meter, and clause-level aspect isolation with positive/negative attribution badges in real-time."
        ),
        (
            "Q13: Are your dashboard insights hardcoded? (Crucial Viva Trap Question!)",
            "Hinglish: Bilkul nahi sir! Insights 100% dynamically compute hote hain. InsightGenerator code dataset ke actual numbers (highest negative aspect variance, steepest declining topic, language sentiment gap) calculate karta hai aur dynamic sentences synthesize karta hai. Dataset change hote hi insights auto-update ho jaate hain.<br/>"
            "English: Absolutely not. Insights are strictly non-hardcoded and dynamically synthesized. The generator calculates mathematical aggregates—such as course satisfaction variance, top negative aspect drivers, and cross-language sentiment disparities—and dynamically formats them into plain-language executive reports."
        ),
        (
            "Q14: How is student privacy and evaluation anonymity guaranteed?",
            "Hinglish: Ingestion time pe student personal identifiers (naam, roll number, email) ko cryptographically hash kar diya jata hai (jaise STU_1042). Database ya dashboard me koi bhi PII (Personally Identifiable Information) store ya display nahi hota, taaki student freely feedback de sake.<br/>"
            "English: Student identifiers are decoupled upon ingestion and replaced with synthetic cryptographic hashes (e.g. STU_1042). No Personally Identifiable Information (PII) is stored or visualized, ensuring complete evaluation anonymity and unbiased student reporting."
        ),
        (
            "Q15: What is the real-world utility of this project for an institution like KES' Shroff College?",
            "Hinglish: Teen main stakeholders hain: (1) HOD / Vice Principal dekh sakte hain ki kis course me negative spike aaya aur kis aspect pe, (2) Faculty member apna teaching pace ya assignment length modify kar sakte hain, aur (3) Curriculum Committee topic drift dekh kar syllabus modernize kar sakti hai.<br/>"
            "English: The platform provides 3 distinct institutional utilities: (1) Department Heads and Deans gain objective diagnostic visibility into departmental bottlenecks, (2) Faculty members receive targeted aspect-level feedback to adjust pedagogy, and (3) Curriculum Committees track longitudinal topic drift to update course syllabi."
        ),
        (
            "Q16: What happens if a student submits a sarcastic review? (e.g. 'Wah sir kya baat hai zero marks diye')",
            "Hinglish: Sarcasm me positive words ('wah', 'kya baat hai') use hote hain negative intent ke sath. Current version me rating (1-5 stars) sentiment modifier ka kaam karti hai. Future roadmap me hum IndicBERT-based sarcasm classifiers integrate karenge.<br/>"
            "English: Sarcasm involves lexical-semantic conflict. In our current architecture, the explicit star rating (1-5) acts as an anchor weight. For future work, we have planned fine-tuned IndicBERT transformer models specifically trained on code-mixed rhetorical sarcasm."
        ),
        (
            "Q17: How did you validate your dataset of 2,200 feedback records?",
            "Hinglish: Humne stratified sampling follow ki: 8 courses (CS101 se WD102) across 6 semesters. Languages me 45% English, 35% Hinglish, aur 20% Hindi rakha gaya. Rating distribution realistic bell curve (mean 3.25) follow karti hai aur ground truth labels domain rules se cross-verify huye.<br/>"
            "English: The 2,200-record benchmark corpus was structured using stratified sampling across 8 academic courses and 6 sequential semesters. Linguistic proportions reflect urban Indian universities (45% EN, 35% Hinglish, 20% Hindi), with ground-truth validation across 12 aspect dimensions."
        ),
        (
            "Q18: What is Macro F1 and why is it preferred over simple Accuracy?",
            "Hinglish: Agar dataset me 90% positive reviews hon aur 10% negative, toh ek dumb model jo sabko positive bol dega wo bhi 90% accuracy dikhayega! Macro F1 har class (Positive, Negative, Neutral) ka F1 alag nikal kar unka average leta hai, isliye class imbalance me true performance dikhata hai.<br/>"
            "English: Accuracy is misleading under class imbalance because a majority-class baseline achieves high accuracy without predicting minority classes. Macro F1 calculates the harmonic mean of precision and recall independently per class and averages them unweighted, ensuring equal penalty across all sentiment classes."
        ),
        (
            "Q19: What is the role of FastAPI in your backend architecture?",
            "Hinglish: FastAPI ek modern asynchronous web framework hai jo Uvicorn ASGI server pe chalta hai. Ye sub-20 millisecond me prediction execute karta hai, auto-generated OpenAPI / Swagger docs deta hai, aur Pydantic schemas se input validate karke SQL injection rokta hai.<br/>"
            "English: FastAPI provides asynchronous ASGI microservices powered by Uvicorn. It executes ML inference in sub-20ms latency, enforces strict Pydantic payload validation preventing injection attacks, and provides auto-generated OpenAPI documentation for institutional LMS integration."
        ),
        (
            "Q20: What are the primary limitations of your current system?",
            "Hinglish: 3 limitations acknowledge karni hain: (1) Sarcasm detection deep colloquial slang me challenging hai, (2) Regional languages jaise Marathi ya Gujarati abhi add karni hain, aur (3) Real student slang daily evolve hota hai jiske liye active learning pipeline chahiye.<br/>"
            "English: Three recognized engineering constraints: (1) Nuanced colloquial sarcasm requires transformer-based context modeling, (2) Linguistic coverage currently focuses on English, Hindi, and Hinglish, and (3) Dynamic student slang orthography requires continuous active learning updates."
        ),
        (
            "Q21: How does your Course-Aspect Net Sentiment Heatmap calculate values?",
            "Hinglish: Heatmap me har cell Course $i$ aur Aspect $j$ ka Net Sentiment represent karta hai: Net Sentiment = (% Positive Reviews - % Negative Reviews). Agar value +1.0 hai toh full green (excellent), aur agar negative hai (-0.8) toh dark red (urgent problem).<br/>"
            "English: Each heatmap cell computes the Net Sentiment Metric for Course $i$ and Aspect $j$: Net Sentiment = (% Positive Clauses - % Negative Clauses) / 100. This maps scores into [-1.0, +1.0], rendering green for departmental strengths and red for critical curricular pain points."
        ),
        (
            "Q22: Why did you build both a Streamlit Dashboard and a Full-Stack Web SPA?",
            "Hinglish: Streamlit Data Science exploration aur analytics ke liye best hai (heatmaps, drift charts, Plotly filters). Full-stack web frontend (FastAPI + HTML/CSS/JS) lightweight, glassmorphic client-facing portal deta hai jahan student feedback submit kar sakte hain aur CRUD perform kar sakte hain.<br/>"
            "English: We established a dual-interface architecture: Streamlit provides interactive data science visualization for academic deans and HODs, while the FastAPI-powered Single Page Web Application provides a lightweight, responsive portal for student submission and real-time CRUD operations."
        ),
        (
            "Q23: How do you handle spelling mistakes in Hinglish? (e.g. 'bohot', 'boht', 'bahut')",
            "Hinglish: Humne normalizer.py me phonetic regex rules aur prefix clustering lagaya hai. 'b+h+t' aur 'b+h+u+t' jaise spelling variants standardize hokar single canonical token 'bahut' me map ho jaate hain.<br/>"
            "English: We implemented phonetic regular expression patterns and prefix clustering in normalizer.py. Common orthographic variants ('bohot', 'boht', 'bahut', 'bhut') are normalized into canonical semantic anchors before feature vectorization."
        ),
        (
            "Q24: What is Topic Coherence (c_v) and why does your model achieve 0.584?",
            "Hinglish: Coherence measure karta hai ki ek topic ke top keywords ek-dusre se kitne related hain. Agar topic ke words hain 'lab, pc, ram, crash' toh coherence high hoga. Humara c-TF-IDF 0.584 achieve karta hai, jabki LDA ka coherence 0.442 tha.<br/>"
            "English: Topic coherence ($c_v$) measures semantic similarity between top words in a topic using sliding-window normalized point-wise mutual information (NPMI). Our c-TF-IDF pipeline achieves $c_v = 0.584$, significantly outperforming LDA ($0.442$) and NMF ($0.479$)."
        ),
        (
            "Q25: If you had 6 more months, what would you add to this project? (Future Scope)",
            "Hinglish: 4 cheezein add karenge: (1) Multilingual Speech-to-Text audio feedback using Whisper, (2) IndicBERT / MuRIL fine-tuning for automated pedagogical action recommendations, (3) Automated email webhooks to faculty when negative sentiment spikes, aur (4) Moodle / Canvas LMS LTI integration.<br/>"
            "English: We would implement four strategic expansions: (1) Multilingual speech-to-text audio ingestion via Whisper, (2) Fine-tuned IndicBERT models for automated teaching action recommendations, (3) Webhook alerts to HODs upon negative aspect spikes, and (4) LTI plugins for Moodle and Canvas LMS integration."
        )
    ]

    for q, a in viva_qa_full:
        story.append(Paragraph(q, qa_q))
        story.append(Paragraph(a, qa_ans))

    story.append(PageBreak())

    # ================= SECTION 8: STEP-BY-STEP LIVE DEMO GUIDE =================
    story.append(Paragraph("8. Step-by-Step Live Demo Protocol (Examiner ke saamne live test kaise karna hai?)", h1_style))
    story.append(Paragraph(
        "Jab examiner bole: <i>'Prem, project chala ke dikhao'</i>, tab ghabrana mat! Exact ye 5 steps follow karna:", body_style
    ))

    demo_steps = [
        ("Step 1: Launch the Application", 
         "Desktop / workspace folder me jao aur <code>START_PROJECT.bat</code> ya <code>run_dashboard.bat</code> pe double click karo. "
         "Browser me dashboard open ho jayega (<code>http://localhost:8501</code> ya <code>http://localhost:8000</code>)."),
        ("Step 2: Overview & AI Intelligence View",
         "Examiner ko bolo: <i>'Sir, this is our Institutional Overview dashboard covering 2,200 student evaluation records across 8 courses and 6 semesters.'</i> "
         "Upar ke 4 KPI cards dikhao (Total Reviews: 2,200, Institutional Rating: 3.25/5.0, Positive: 63.5%, Negative: 24.1%). "
         "Fir <b>AI Executive Intelligence summary</b> dikhao aur bolo: <i>'Sir, ye plain-language insights dynamic statistical algorithms se generate huye hain, hardcoded nahi hain.'</i>"),
        ("Step 3: Aspect Breakdown (ABSA) Heatmap",
         "Aspect Breakdown view select karo. <b>Course vs. 12-Aspect Net Sentiment Heatmap</b> dikhao. "
         "Examiner ko bolo: <i>'Sir, yahan green blocks institutional strengths hain aur red blocks specific pain points hain. Jaise CS101 me Teaching Quality green hai (+0.75), lekin Infrastructure red hai (-0.60).'</i>"),
        ("Step 4: Longitudinal Topic Drift Analytics",
         "Topic Drift view select karo. Examiner ko semester trendlines dikhao aur bolo: "
         "<i>'Sir, yahan semester-wise topics track ho rahe hain. Jaise Placement Prep aur Capstone Projects Sem 5-6 me Emerging (⚡) classify huye hain, jabki Introductory Pacing complaints decline (📉) ho gayi hain.'</i>"),
        ("Step 5: Live AI Sandbox Inference (The Showstopper!)",
         "Sandbox tab pe jao. Text input box me ye exact Hinglish review type karo:<br/>"
         "<b>'Prof sir concepts bahut acche samjhate hain lekin lab PCs crash ho rahe hain aur assignments tough hain'</b><br/>"
         "Fir <b>Analyze Feedback Live</b> button click karo!<br/>"
         "Examiner ko dikhao ki system ne realtime me:<br/>"
         "• <b>Language:</b> Hinglish detect kiya with 98% confidence<br/>"
         "• <b>Teaching Quality:</b> Positive (+1.0) detect kiya<br/>"
         "• <b>Infrastructure:</b> Negative (-1.0) detect kiya<br/>"
         "• <b>Assignments:</b> Negative (-1.0) detect kiya<br/>"
         "Ye dekhkar external examiner 100% impress ho jayega!")
    ]

    for title, desc in demo_steps:
        story.append(Paragraph(f"<b>{title}</b>", h2_style))
        story.append(Paragraph(desc, body_style))
        story.append(Spacer(1, 3))

    # ================= SECTION 9: CHEAT SHEET =================
    story.append(Spacer(1, 6))
    story.append(Paragraph("9. Final 5 Golden Rules for Viva Day", h1_style))
    story.append(Paragraph(
        "1. <b>Confidence & Calm:</b> Examiner aapko fail karne nahi, aapka knowledge test karne aaya hai. Har answer smile ke sath aur clear voice me do.<br/>"
        "2. <b>If you don't know something:</b> Kabhi feko (guess) mat! Seedha bolo: <i>'Sir, currently this is not in my architecture, but in future scope I can implement it using XYZ algorithm.'</i><br/>"
        "3. <b>Always mention the 12 Aspects:</b> Jab bhi poochhe kyu banaya, bolo ki humne 12 standard dimensions me decompose kiya hai.<br/>"
        "4. <b>Highlight Negation & Trilingual NLP:</b> Ye aapka sabse bada unique feature hai jo commercial models me nahi hota.<br/>"
        "5. <b>Show the Live Sandbox:</b> Working demo hamesha 10 pages ki theory se 100 times zyada impactful hota hai!",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated Ultimate Viva Master Guide at {filename}")

if __name__ == "__main__":
    build_pdf()
