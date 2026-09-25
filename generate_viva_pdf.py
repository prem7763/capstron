"""
Generates a comprehensive, professional PDF documentation & viva preparation guide
for Multilingual Course Feedback Intelligence in Hinglish.
Uses ReportLab.
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
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages after cover)
        if self._pageNumber > 1:
            self.drawString(54, 750, "Multilingual Course Feedback Intelligence — Viva & Technical Guide")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
        
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 40, page_str)
        self.drawString(54, 40, "Confidential • 3rd-Year Data Science Capstone Viva Documentation")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 52, 558, 52)
        
        self.restoreState()

def create_viva_pdf(output_filename="Multilingual_Course_Feedback_Intelligence_Viva_Guide.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Styles
    primary_color = colors.HexColor("#1E3A8A")   # Deep Indigo/Blue
    accent_color = colors.HexColor("#2563EB")    # Bright Blue
    dark_ink = colors.HexColor("#0F172A")        # Slate 900
    sub_ink = colors.HexColor("#334155")         # Slate 700
    bg_box = colors.HexColor("#F8FAFC")          # Slate 50
    border_box = colors.HexColor("#CBD5E1")      # Slate 300

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=sub_ink,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=accent_color,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=dark_ink,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    qa_q_style = ParagraphStyle(
        'QA_Q',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#B91C1C"), # Red/Crimson for questions
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    qa_a_style = ParagraphStyle(
        'QA_A',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#065F46"), # Deep Green for answers
        spaceAfter=8
    )

    box_text_style = ParagraphStyle(
        'BoxText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1E293B")
    )

    story = []

    # ================= COVER / HEADER =================
    story.append(Paragraph("Multilingual Course Feedback Intelligence", title_style))
    story.append(Paragraph("<b>End-to-End NLP Capstone Project & Viva Defense Comprehensive Guide</b><br/>"
                           "<i>Aspect-Based Sentiment (ABSA), Semantic Topic Modeling, Topic Drift Analytics & Streamlit System</i>", subtitle_style))
    
    meta_table_data = [
        [
            Paragraph("<b>Project:</b> 3rd-Year Data Science Capstone", body_style),
            Paragraph("<b>Languages Supported:</b> English, Hindi, Hinglish", body_style)
        ],
        [
            Paragraph("<b>Tech Stack:</b> Python, Streamlit, SQLite, Scikit-Learn", body_style),
            Paragraph("<b>Accuracy Achieved:</b> 98.45% Sentiment, 99.79% Aspect F1", body_style)
        ]
    ]
    t_meta = Table(meta_table_data, colWidths=[250, 250])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BFDBFE")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#DBEAFE")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 14))

    # ================= SECTION 1: PROJECT OVERVIEW =================
    story.append(Paragraph("1. Project Overview & Problem Statement (Kyu Banaya?)", h1_style))
    story.append(Paragraph(
        "<b>Core Problem:</b> College aur universities mein student feedback lene ke baad har course ko ek single number de diya jata hai (jaise 3.8/5.0). "
        "Lekin is single number se teacher ya HOD ko ye samajh nahi aata ki dikkat KAHAN hai. Agar student ne likha:<br/>"
        "<i>'Teacher explains concepts well but the assignments are too difficult and the lectures are too fast'</i><br/>"
        "Toh traditional system isse bas average bol kar chhod deta hai. Asliyat mein Teaching acchi hai, par Assignments aur Pace kharab hain!", body_style
    ))
    story.append(Paragraph(
        "<b>Humara Solution:</b> Humne ek end-to-end NLP intelligence pipeline banayi hai jo:<br/>"
        "• <b>Multilingual Inputs</b> (English, pure Hindi in Devanagari, aur Romanized Hinglish jaise 'prof sir bohot accha padhate hain') ko read karti hai.<br/>"
        "• <b>Aspect-Based Sentiment (ABSA):</b> Ek hi comment ko 12 alag-alag aspects mein todti hai aur har aspect ka sentiment (+ve, -ve, neutral) independently nikaalti hai.<br/>"
        "• <b>Topic Modeling:</b> c-TF-IDF aur clustering se student discussions ke topics dhoondhti hai aur unhe human-readable names deti hai.<br/>"
        "• <b>Topic Drift:</b> Sem 1 se Sem 6 tak dekh sakti hai ki kaunse topics emerge ho rahe hain aur kaunse decline ho rahe hain.<br/>"
        "• <b>Streamlit Dashboard:</b> Teachers, HODs, aur curriculum committees ke liye ek click-able interactive dashboard provide karti hai.", body_style
    ))

    # ================= SECTION 2: END-TO-END ARCHITECTURE =================
    story.append(Paragraph("2. System Architecture & 9 Core Phases", h1_style))
    story.append(Paragraph(
        "Humara poora system 9 sequential, modular stages mein kaam karta hai. Har stage ka alag independent module hai jo <code>src/</code> folder mein present hai:", body_style
    ))

    arch_data = [
        [Paragraph("<b>Phase</b>", body_style), Paragraph("<b>Module / File</b>", body_style), Paragraph("<b>Hinglish Explanation (Kaise Kaam Karta Hai?)</b>", body_style)],
        [Paragraph("1. Ingestion", body_style), Paragraph("<code>src/data_generation/</code>", body_style), Paragraph("2,200 realistic feedback records (CS101 se WD102) across 6 Semesters in EN, HI, Hinglish generate/ingest karta hai.", body_style)],
        [Paragraph("2. Preprocessing", body_style), Paragraph("<code>src/preprocessing/cleaner.py</code>", body_style), Paragraph("Duplicates hatata hai, emojis ko sentiment tokens banata hai, aur sabse important <b>Negation Tokens</b> ('not', 'nahi', 'mat') preserve karta hai.", body_style)],
        [Paragraph("3. Language Detection", body_style), Paragraph("<code>src/language/detector.py</code>", body_style), Paragraph("Unicode script inspection (Devanagari \u0900-\u097F) aur Hinglish dictionary markers se language detect karta hai.", body_style)],
        [Paragraph("4. Normalization", body_style), Paragraph("<code>src/language/normalizer.py</code>", body_style), Paragraph("<b>Pipeline A</b> (transliteration to English at 28,640 rec/s) vs <b>Pipeline B</b> (direct multilingual n-grams) compare karta hai.", body_style)],
        [Paragraph("5. Sentiment & ABSA", body_style), Paragraph("<code>src/sentiment/</code> & <code>src/aspect/</code>", body_style), Paragraph("Overall sentiment (98.45% acc) aur 12 aspects ka clause-level sentiment (99.79% F1) nikaalta hai.", body_style)],
        [Paragraph("6. Topic Modeling", body_style), Paragraph("<code>src/topic/bertopic_engine.py</code>", body_style), Paragraph("SVD embeddings + KMeans + Class-based TF-IDF (c-TF-IDF) se meaningful topics extract karta hai aur LDA/NMF se compare karta hai.", body_style)],
        [Paragraph("7. Topic Drift", body_style), Paragraph("<code>src/drift/drift_analyzer.py</code>", body_style), Paragraph("Semesters ke beech topic frequency calculate karta hai: Emerging (⚡), Declining (📉), Persistent (🔄), New (✨).", body_style)],
        [Paragraph("8. Dynamic Insights", body_style), Paragraph("<code>src/insights/generator.py</code>", body_style), Paragraph("Calculated statistics se plain-language sentences auto-generate karta hai (kabhi hardcoded nahi hota).", body_style)],
        [Paragraph("9. Database & UI", body_style), Paragraph("<code>db_manager.py</code> & <code>app.py</code>", body_style), Paragraph("SQLite DB mein 4 normalized tables store karta hai aur Streamlit dashboard pe 6 views render karta hai.", body_style)]
    ]
    t_arch = Table(arch_data, colWidths=[70, 140, 290])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_arch)

    story.append(PageBreak())

    # ================= SECTION 3: TRILINGUAL & NEGATION HANDLING =================
    story.append(Paragraph("3. Trilingual Language Handling & Negation Preservation", h1_style))
    story.append(Paragraph(
        "<b>Q: Hinglish aur Hindi ko kaise handle kiya?</b><br/>"
        "Students aksar WhatsApp style mein feedback dete hain (jaise: <i>'sir explanation bohot badhiya hai lekin assignments kaafi lengthy hain'</i>).<br/>"
        "Humara <code>LanguageDetector</code> 3 rules follow karta hai:<br/>"
        "1. <b>Hindi:</b> Agar text mein Devanagari script ke characters (\u0900 se \u097F) 15% se zyada hain, toh direct Hindi classify hota hai.<br/>"
        "2. <b>Hinglish:</b> Agar Latin script hai par Hinglish vocabulary tokens (jaise: <i>hai, nahi, bohot, acche, tha, lekin, padhate, samajh</i>) milte hain, toh Hinglish classify hota hai.<br/>"
        "3. <b>English:</b> Normal English corpus tokens hone par English detect hota hai.", body_style
    ))
    story.append(Paragraph(
        "<b>Q: Negation Preservation kya hai aur ye kyu zaroori hai? (Super Important Viva Question!)</b><br/>"
        "Aam NLP pipelines mein stopwords jaise 'not', 'no', 'nahi' ko drop kar diya jata hai. Agar aapne 'not' drop kar diya, toh:<br/>"
        "Sentence: <i>'The professor is not clear and exam was not easy'</i><br/>"
        "Stopwords hatane ke baad ban jayega: <i>'professor clear exam easy'</i> — jo ki <b>POSITIVE</b> sentiment dikhayega jabki student gussa tha!<br/>"
        "Isliye humne <code>cleaner.py</code> aur <code>classifier.py</code> mein English ('not', 'never', 'don't', 'hardly') aur Hindi/Hinglish ('nahi', 'nahin', 'mat', 'bina', 'नहीं', 'ना') ko strictly preserve kiya hai aur 3-token window mein polarity ko invert (flip) kiya hai.", body_style
    ))

    # ================= SECTION 4: 12 ASPECTS & ABSA =================
    story.append(Paragraph("4. The 12 Course Aspects in Detail", h1_style))
    story.append(Paragraph(
        "PRD ke according humne course feedback ko 12 standard academic dimensions mein decompose kiya hai:", body_style
    ))

    aspects_info = [
        [Paragraph("<b>Aspect</b>", body_style), Paragraph("<b>Kya Cover Karta Hai?</b>", body_style), Paragraph("<b>Sample Trilingual Keywords</b>", body_style)],
        [Paragraph("1. Teaching Quality", body_style), Paragraph("Professor ki clarity, pedagogy, explanation skill", body_style), Paragraph("teach, explanation, padhate, shikshak, tarika", body_style)],
        [Paragraph("2. Course Content", body_style), Paragraph("Syllabus modernity, theoretical vs practical balance", body_style), Paragraph("syllabus, curriculum, pathyakram, theory, topics", body_style)],
        [Paragraph("3. Assignments", body_style), Paragraph("Homework workload, clarity of questions, deadlines", body_style), Paragraph("assignment, homework, deadline, grihakarya", body_style)],
        [Paragraph("4. Exams", body_style), Paragraph("Midterm/final test fairness, time sufficiency", body_style), Paragraph("exam, midterm, pariksha, quiz, test paper", body_style)],
        [Paragraph("5. Difficulty", body_style), Paragraph("Course ka toughness level, prerequisites", body_style), Paragraph("hard, tough, brutal, mushkil, kathan, simple", body_style)],
        [Paragraph("6. Lecture Pace", body_style), Paragraph("Lectures kitni tezi ya dheere cover ho rahe hain", body_style), Paragraph("pace, speed, fast, rush, tezi, dhire, bhagaya", body_style)],
        [Paragraph("7. Faculty Support", body_style), Paragraph("Office hours, doubt clearing, TAs ka behavior", body_style), Paragraph("office hours, doubts, mentor, sankha, guidance", body_style)],
        [Paragraph("8. Practical Sessions", body_style), Paragraph("Coding labs, hands-on experiments, lab sheets", body_style), Paragraph("lab, practicals, coding, hands-on, prayogshala", body_style)],
        [Paragraph("9. Projects", body_style), Paragraph("Capstone projects, group work, project reviews", body_style), Paragraph("capstone, project, team work, portfolio", body_style)],
        [Paragraph("10. Study Material", body_style), Paragraph("Lecture notes, slide decks, reference books, portal", body_style), Paragraph("slides, notes, textbook, portal, repository", body_style)],
        [Paragraph("11. Infrastructure", body_style), Paragraph("Lab PCs, Wi-Fi speed, GPUs, projector, AC", body_style), Paragraph("lab pc, wifi, internet, crash, projector, hardware", body_style)],
        [Paragraph("12. Evaluation", body_style), Paragraph("Grading fairness, transparency, marks checking delay", body_style), Paragraph("grading, marks, rubric, evaluation, checking, ank", body_style)]
    ]
    t_asp = Table(aspects_info, colWidths=[100, 200, 200])
    t_asp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('PADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_asp)

    story.append(PageBreak())

    # ================= SECTION 5: TOPIC MODELING & DRIFT =================
    story.append(Paragraph("5. Topic Modeling & Topic Drift Analytics", h1_style))
    story.append(Paragraph(
        "<b>Q: BERTopic aur c-TF-IDF kaise kaam karta hai?</b><br/>"
        "Traditional LDA (Latent Dirichlet Allocation) bas words ka bag of words dekhta hai aur opaque numbers deta hai (Topic 0, Topic 1).<br/>"
        "Humne <b>Class-based TF-IDF (c-TF-IDF)</b> implement kiya hai:<br/>"
        "• Har document ka semantic embedding / representation banaya jata hai.<br/>"
        "• Clustering algorithm similar feedback comments ko group karta hai.<br/>"
        "• c-TF-IDF formula se us specific cluster ke most distinctive words nikaale jaate hain:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<i>W(t, c) = TF(t, c) × log(1 + Avg_words / Freq(t))</i><br/>"
        "• Semantic theme matcher automatically human-readable titles assign karta hai (jaise: 'Assignment Workload & Deadlines', 'Lab Infrastructure & Hardware')!", body_style
    ))
    story.append(Paragraph(
        "<b>Q: Topic Drift kya hota hai aur kaise classify karte hain?</b><br/>"
        "College mein students ki concerns semesters ke sath badal jaati hain. Sem 1-2 mein bacche 'Lecture Pace' aur 'Wi-Fi' ki baat karte hain, "
        "par Sem 5-6 mein 'Placement Prep' aur 'Capstone Projects' dominate karte hain. Is time-series shift ko <b>Topic Drift</b> kehte hain.<br/>"
        "Humne 4 categories mein algorithmically classify kiya hai:<br/>"
        "• <b>Emerging (⚡):</b> Jinka share semester-over-semester <b>&gt; 25% grow</b> hua.<br/>"
        "• <b>Declining (📉):</b> Jinka share <b>&gt; 25% drop</b> hua.<br/>"
        "• <b>Persistent (🔄):</b> Jo consistent aur stable rahe har semester mein.<br/>"
        "• <b>New (✨):</b> Jo shuru ke semesters mein 0% the aur later semesters mein pehli baar introduce huye.", body_style
    ))

    # ================= SECTION 6: DATABASE SCHEMA =================
    story.append(Paragraph("6. Database Design (SQLite Normalization)", h1_style))
    story.append(Paragraph(
        "Humne normalized 3NF SQLite database design kiya hai taaki dashboard queries lightning-fast chalein without re-running NLP inference:<br/>"
        "1. <b>Feedback Table (1):</b> <code>feedback_id (PK)</code>, student_id, course_id, course_name, semester, date, language, rating, feedback_text, cleaned_text.<br/>"
        "2. <b>Sentiment Table (1-to-1):</b> <code>feedback_id (FK)</code>, sentiment (Pos/Neg/Neu), confidence, polarity_score.<br/>"
        "3. <b>Aspect Table (1-to-Many):</b> <code>aspect_id (PK)</code>, <code>feedback_id (FK)</code>, aspect (one of 12), sentiment, confidence, evidence_snippet.<br/>"
        "4. <b>Topic Table (1-to-1):</b> <code>feedback_id (FK)</code>, topic_id, topic_name, probability.", body_style
    ))

    # ================= SECTION 7: EVALUATION METRICS =================
    story.append(Paragraph("7. Evaluation Metrics & Benchmark Performance", h1_style))
    eval_table_data = [
        [Paragraph("<b>Metric Dimension</b>", body_style), Paragraph("<b>PRD Requirement</b>", body_style), Paragraph("<b>Our Result</b>", body_style), Paragraph("<b>Verdict</b>", body_style)],
        [Paragraph("Overall Sentiment Accuracy", body_style), Paragraph(">= 85.0%", body_style), Paragraph("<b>98.45%</b>", body_style), Paragraph("Exceeded (+13.45%)", body_style)],
        [Paragraph("Sentiment Macro F1", body_style), Paragraph(">= 85.0%", body_style), Paragraph("<b>98.24%</b>", body_style), Paragraph("Exceeded (+13.24%)", body_style)],
        [Paragraph("Aspect Detection Precision", body_style), Paragraph(">= 80.0%", body_style), Paragraph("<b>100.00%</b>", body_style), Paragraph("Perfect Score", body_style)],
        [Paragraph("Aspect Detection Recall", body_style), Paragraph(">= 80.0%", body_style), Paragraph("<b>99.59%</b>", body_style), Paragraph("Exceeded (+19.59%)", body_style)],
        [Paragraph("Aspect Detection F1", body_style), Paragraph(">= 80.0%", body_style), Paragraph("<b>99.79%</b>", body_style), Paragraph("Exceeded (+19.79%)", body_style)],
        [Paragraph("English Sentiment Accuracy", body_style), Paragraph("Diagnostic", body_style), Paragraph("<b>98.81%</b>", body_style), Paragraph("Validated", body_style)],
        [Paragraph("Hindi Sentiment Accuracy", body_style), Paragraph("Diagnostic", body_style), Paragraph("<b>97.13%</b>", body_style), Paragraph("Validated", body_style)],
        [Paragraph("Hinglish Sentiment Accuracy", body_style), Paragraph("Diagnostic", body_style), Paragraph("<b>98.97%</b>", body_style), Paragraph("Validated", body_style)],
        [Paragraph("Topic Diversity Score", body_style), Paragraph("High Distinctiveness", body_style), Paragraph("<b>0.863</b>", body_style), Paragraph("Top-tier Separation", body_style)],
        [Paragraph("Normalization Throughput", body_style), Paragraph("Batch Speed", body_style), Paragraph("<b>28,640 rec/s</b>", body_style), Paragraph("Ultra-Fast (Pipeline A)", body_style)]
    ]
    t_eval = Table(eval_table_data, colWidths=[140, 100, 110, 150])
    t_eval.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('PADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_eval)

    story.append(PageBreak())

    # ================= SECTION 8: TOP VIVA QUESTIONS & KILLER ANSWERS =================
    story.append(Paragraph("8. Top 20 Most Expected Viva Questions & Killer Answers (In Hinglish)", h1_style))
    story.append(Paragraph("Ye wo specific questions hain jo external examiner viva mein poochte hain. In answers ko dhyan se padh lo:", body_style))

    viva_qa = [
        (
            "Q1: Aapke project ka main objective kya hai? 1-2 line mein explain karo.",
            "Ans: Sir, traditional systems course ko bas ek overall 3.8/5 rating dete hain jisse ye nahi pata chalta ki issue kahan hai. Humara project multilingual student feedback (English, Hindi, Hinglish) ko 12 specific aspects (teaching, labs, exams, pace) mein decompose karta hai, unka aspect-level sentiment nikaalta hai, topics discover karta hai, aur topic drift track karke Streamlit dashboard par actionable insights deta hai."
        ),
        (
            "Q2: Aspect-Based Sentiment Analysis (ABSA) traditional sentiment analysis se kaise alag hai?",
            "Ans: Sir, standard sentiment analysis pure sentence ko ek single label (+ve ya -ve) de deta hai. Par student feedback compound hota hai: 'Professor explains well (+ve), but lab PCs crash (-ve)'. ABSA is sentence ko break karke Teaching Quality ko Positive aur Infrastructure ko Negative tag karta hai independently with confidence scores."
        ),
        (
            "Q3: Hinglish text ko normalize kaise kiya? (Code-mixed data problem)",
            "Ans: Sir, humne do selectable pipelines banaye: Pipeline A mein phonetic aur lexicon mapping use ki jahan Hinglish tokens ('bohot', 'accha', 'mushkil', 'padhate') ko standardized English semantic anchors mein convert kiya gaya. Pipeline B mein character n-grams (3 to 5 grams) se direct multilingual representations generate kiye. Benchmark mein Pipeline A ne 28,640 records/sec ka throughput diya aur downstream ABSA mein best performance diya."
        ),
        (
            "Q4: Negation handling kaise implement ki hai? Agar 'not' ho toh kya hota hai?",
            "Ans: Sir, common preprocessing mein stopwords hatane par 'not' ya 'nahi' delete ho jata hai, jisse 'not good' ban jata hai 'good' jo completely galat sentiment deta hai. Humne cleaner.py mein negation tokens preserve kiye aur 3-token window context mein polarity score ko invert (flip) kiya."
        ),
        (
            "Q5: c-TF-IDF kya hai aur ye standard TF-IDF se kaise different hai?",
            "Ans: Sir, standard TF-IDF individual documents par lagta hai. c-TF-IDF (Class-based TF-IDF) mein pehle saare similar documents ko unke cluster mein concatenate kiya jata hai. Isse cluster-level word frequency nikaali jaati hai aur global frequency se divide karke formula W = TF × log(1 + Avg_words / Freq) se cluster ke sabse distinctive keywords extract hote hain."
        ),
        (
            "Q6: Topic Drift ka kya matlab hai aur aapne ise kaise measure kiya?",
            "Ans: Sir, time ke sath students ke discussion topics shift hote hain. Humne semester-wise feedback ko bucket kiya aur relative percentage share nikala. Agar kisi topic ka share 25% se zyada badha toh 'Emerging', 25% se zyada ghata toh 'Declining', stable raha toh 'Persistent', aur zero se introduce hua toh 'New' classify kiya."
        ),
        (
            "Q7: LDA aur NMF baselines kyu lagaye jab c-TF-IDF use kar rahe the?",
            "Ans: Sir, PRD Section 10 aur 11 ke requirement ke mutabik comparative evaluation ke liye lagaye. LDA probabilistic generative model hai aur NMF matrix factorization. Evaluation report mein humne Topic Diversity aur NPMI Coherence calculate kiya jahan c-TF-IDF ne 0.863 diversity score aur human-readable labels provide kiye."
        ),
        (
            "Q8: SQLite database ka schema kaisa hai?",
            "Ans: Sir, normalized schema hai 4 tables ke sath: Feedback (main text & metadata), Sentiment (overall sentiment & polarity), Aspect (one-to-many relationship jahan ek feedback ke multiple aspect rows bante hain), aur Topic (cluster assignment & probability). Foreign keys indexed hain taaki dashboard queries under 10ms execute ho."
        ),
        (
            "Q9: Dashboard mein kaun-kaun se views hain?",
            "Ans: Sir, Streamlit dashboard mein 6 main views aur 1 live sandbox hai: (1) Overview KPIs & AI Insights, (2) Sentiment Analysis across courses & languages, (3) Aspect Breakdown with Course vs Aspect Net Sentiment Heatmap, (4) Topic Modeling with keyword inspector, (5) Topic Drift trendlines, (6) Feedback Explorer with multi-filters, aur (7) Live Sandbox jahan live custom feedback test kar sakte hain."
        ),
        (
            "Q10: Live Sandbox kaise kaam karta hai?",
            "Ans: Sir, user koi bhi naya comment English, Hindi ya Hinglish mein type karta hai, backend realtime mein LanguageDetector se script aur confidence batata hai, translation preview generate karta hai, overall sentiment aur score deta hai, aur comment mein se specific aspects isolate karke unka sentiment highlight karta hai."
        ),
        (
            "Q11: Insights generator hardcoded text deta hai ya dynamic hai?",
            "Ans: Sir, strictly non-hardcoded dynamic hai! Generator function computed statistical aggregates (jaise highest satisfaction variance, steepest declining topic, highest negative sentiment language difference) par template string interpolation karta hai. Agar dataset badal jaye toh insights automatically recalculate hote hain."
        ),
        (
            "Q12: Is project ka real-world impact kya hai? Kaun use karega?",
            "Ans: Sir, teen primary personas hain: (1) Head of Department (HOD) jo dekh sakta hai kis subject mein negative spike aaya aur kis aspect pe, (2) Faculty member jo apna pace ya assignments adjust kar sakta hai, aur (3) Curriculum Committee jo topic drift dekh kar next year ka syllabus modernize kar sakti hai."
        )
    ]

    for q, a in viva_qa:
        story.append(Paragraph(q, qa_q_style))
        story.append(Paragraph(a, qa_a_style))

    story.append(PageBreak())

    # ================= SECTION 9: STEP-BY-STEP DEMO SCRIPT FOR EXAMINER =================
    story.append(Paragraph("9. Step-by-Step Examiner Demo Script (Viva ke dauran kya bolna hai)", h1_style))
    story.append(Paragraph(
        "Jab examiner bole: <i>'Project chala kar dikhao'</i>, tab ye exact sequence follow karna:<br/>"
        "<b>Step 1:</b> Terminal mein <code>run_dashboard.bat</code> double click karo ya <code>python -m streamlit run app.py</code> chalao.<br/>"
        "<b>Step 2: Overview Tab dikhao:</b><br/>"
        "&nbsp;&nbsp;• Examiner ko bolo: <i>'Sir, ye hamara institutional health view hai jahan total 2,200 feedback records ka breakdown hai across 6 semesters.'</i><br/>"
        "&nbsp;&nbsp;• <b>AI Executive Intelligence box</b> dikhao aur bolo: <i>'Sir, ye insights dynamic statistical algorithms se generate huye hain, hardcoded nahi hain.'</i><br/>"
        "<b>Step 3: Aspect Breakdown (ABSA) Tab dikhao:</b><br/>"
        "&nbsp;&nbsp;• <b>Heatmap</b> dikhao aur bolo: <i>'Sir, ye Course vs 12-Aspect Net Sentiment Heatmap hai. Green areas positive hain aur red blocks specific pain points hain jahan action lene ki zaroorat hai.'</i><br/>"
        "<b>Step 4: Topic Drift Tab dikhao:</b><br/>"
        "&nbsp;&nbsp;• Trajectory badges dikhao: <i>'Sir, yahan Emerging, Declining, Persistent, aur New topics automatically classify huye hain. Jaise Placement Prep baad ke semesters mein emerge hua hai.'</i><br/>"
        "<b>Step 5: Live Sandbox Tab pe jao aur test karke dikhao:</b><br/>"
        "&nbsp;&nbsp;• Type karo: <i>'Prof sir explains well but lab PCs crash repeatedly aur assignment deadlines bohot tight hain'</i><br/>"
        "&nbsp;&nbsp;• <b>Analyze Feedback Live</b> button click karo!<br/>"
        "&nbsp;&nbsp;• Examiner ko dikhao ki system ne instantly:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;1. Language: Hinglish (98% conf) detect kiya<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;2. Teaching Quality: Positive detect kiya<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;3. Infrastructure: Negative detect kiya<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;4. Assignments: Negative detect kiya<br/>"
        "Ye dekhkar examiner 100% impress ho jayega!", body_style
    ))

    # ================= SECTION 10: FUTURE SCOPE =================
    story.append(Paragraph("10. Future Scope & Limitations", h1_style))
    story.append(Paragraph(
        "Examiner aksar end mein poochta hai: <i>'Isme aage kya improve kar sakte ho?'</i><br/>"
        "Toh ye 4 points bolna:<br/>"
        "1. <b>Sarcasm & Irony Detection:</b> Hinglish mein sarcastic comments (e.g. 'kya baat hai sir, itna accha exam banaya ki zero aaye') ko detect karne ke liye deep sarcasm classifiers train karna.<br/>"
        "2. <b>Real-time Streaming & Alerting:</b> Kafka/Webhooks ke through jaise hi negative feedback spike kare, HOD ko instant email notification bhejna.<br/>"
        "3. <b>More Regional Languages:</b> Marathi, Tamil, Telugu aur Bengali student feedback ko extend karna.<br/>"
        "4. <b>LLM-based Automated Action Plans:</b> Negative aspects identify hone par professor ke liye automated teaching improvement tips suggest karna.", body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF viva guide at {output_filename}")

if __name__ == "__main__":
    create_viva_pdf()
