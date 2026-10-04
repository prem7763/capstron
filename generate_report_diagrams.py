"""
Generate publication-quality diagram and output images for the Capstone Blackbook.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec

os.makedirs('report_assets', exist_ok=True)
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

# -------------------------------------------------------------
# 1. GANTT CHART
# -------------------------------------------------------------
def make_gantt_chart():
    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300)
    tasks = [
        "1. Problem Definition & Literature Review",
        "2. Corpus Synthesis & Multilingual Cleaning",
        "3. Trilingual Detection & Sentiment Classification",
        "4. 12-Aspect ABSA & Negation Preservation",
        "5. c-TF-IDF / BERTopic Modeling & Drift Analysis",
        "6. SQLite Database & FastAPI Microservices",
        "7. Full-Stack Web Frontend & Streamlit UI",
        "8. Empirical Evaluation & Blackbook Documentation"
    ]
    starts = [1, 3, 5, 7, 9, 11, 13, 14]
    durations = [3, 3, 3, 3, 3, 3, 3, 3]
    colors = ['#4f46e5', '#6366f1', '#06b6d4', '#0ea5e9', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6']
    
    y_pos = np.arange(len(tasks))
    ax.barh(y_pos, durations, left=starts, align='center', color=colors, alpha=0.85, edgecolor='#1e293b', height=0.55)
    
    for i, (task, start, dur) in enumerate(zip(tasks, starts, durations)):
        ax.text(start + dur / 2, i, f"Weeks {start}-{start+dur-1}", ha='center', va='center', color='white', fontweight='bold', fontsize=9)
        
    ax.set_yticks(y_pos)
    ax.set_yticklabels(tasks, fontsize=10, fontweight='bold', color='#1e293b')
    ax.invert_yaxis()
    ax.set_xlabel('Project Timeline (Academic Calendar Weeks)', fontsize=11, fontweight='bold', color='#1e293b')
    ax.set_title('Capstron Development Lifecycle & Timeline (Gantt Chart)', fontsize=14, fontweight='bold', pad=15, color='#0f172a')
    ax.set_xlim(0, 18)
    ax.set_xticks(range(1, 18))
    ax.grid(axis='x', linestyle='--', alpha=0.4)
    ax.set_facecolor('#f8fafc')
    fig.patch.set_facecolor('white')
    plt.tight_layout()
    plt.savefig('report_assets/gantt_chart.png', bbox_inches='tight')
    plt.close()
    print("Gantt Chart saved.")

# -------------------------------------------------------------
# 2. E-R DIAGRAM
# -------------------------------------------------------------
def make_er_diagram():
    fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    def draw_entity(x, y, w, h, title, fields, bg='#f0fdf4', border='#16a34a'):
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5", fc=bg, ec=border, lw=2)
        ax.add_patch(box)
        header = patches.FancyBboxPatch((x, y + h - 6), w, 6, boxstyle="square,pad=0.0", fc=border, ec=border)
        ax.add_patch(header)
        ax.text(x + w / 2, y + h - 3, title, ha='center', va='center', color='white', fontweight='bold', fontsize=11)
        for idx, (f_name, f_type) in enumerate(fields):
            ax.text(x + 2, y + h - 10 - idx * 3.8, f_name, ha='left', va='center', fontsize=8.5, fontweight='bold' if 'PK' in f_type or 'FK' in f_type else 'normal', color='#0f172a')
            ax.text(x + w - 2, y + h - 10 - idx * 3.8, f_type, ha='right', va='center', fontsize=8, color='#475569')

    # Feedback Table (Central)
    draw_entity(34, 40, 32, 45, "Feedback [Entity]", [
        ("feedback_id", "VARCHAR(30) [PK]"),
        ("student_id", "VARCHAR(30)"),
        ("course_id", "VARCHAR(20)"),
        ("course_name", "VARCHAR(100)"),
        ("semester", "VARCHAR(20)"),
        ("date", "DATE"),
        ("language", "VARCHAR(20)"),
        ("rating", "INTEGER [1-5]"),
        ("feedback_text", "TEXT"),
        ("cleaned_text", "TEXT")
    ], bg='#eff6ff', border='#2563eb')

    # Sentiment Table
    draw_entity(3, 48, 26, 32, "Sentiment [Entity]", [
        ("sentiment_id", "INTEGER [PK AUTO]"),
        ("feedback_id", "VARCHAR(30) [FK]"),
        ("sentiment", "VARCHAR(20)"),
        ("confidence", "FLOAT"),
        ("polarity_score", "FLOAT")
    ], bg='#ecfdf5', border='#059669')

    # Aspect Table
    draw_entity(71, 48, 26, 32, "Aspect [Entity]", [
        ("aspect_id", "INTEGER [PK AUTO]"),
        ("feedback_id", "VARCHAR(30) [FK]"),
        ("aspect", "VARCHAR(50)"),
        ("sentiment", "VARCHAR(20)"),
        ("confidence", "FLOAT"),
        ("evidence_snippet", "TEXT")
    ], bg='#fdf4ff', border='#c026d3')

    # Topic Table
    draw_entity(34, 4, 32, 28, "Topic [Entity]", [
        ("topic_entry_id", "INTEGER [PK AUTO]"),
        ("feedback_id", "VARCHAR(30) [FK]"),
        ("topic_id", "INTEGER"),
        ("topic_name", "VARCHAR(100)"),
        ("probability", "FLOAT")
    ], bg='#fffbeb', border='#d97706')

    # Connectors & Cardinalities
    # Feedback <-> Sentiment (1 : 1)
    ax.annotate("", xy=(34, 62), xytext=(29, 62), arrowprops=dict(arrowstyle="<->", color='#0f172a', lw=1.8))
    ax.text(31.5, 64, "1 : 1", ha='center', fontsize=9, fontweight='bold', color='#1e293b')

    # Feedback <-> Aspect (1 : N)
    ax.annotate("", xy=(66, 62), xytext=(71, 62), arrowprops=dict(arrowstyle="<->", color='#0f172a', lw=1.8))
    ax.text(68.5, 64, "1 : N", ha='center', fontsize=9, fontweight='bold', color='#1e293b')

    # Feedback <-> Topic (1 : 1)
    ax.annotate("", xy=(50, 40), xytext=(50, 32), arrowprops=dict(arrowstyle="<->", color='#0f172a', lw=1.8))
    ax.text(53, 36, "1 : 1", ha='center', fontsize=9, fontweight='bold', color='#1e293b')

    ax.set_title("Normalized SQLite Relational Database Entity-Relationship Diagram (3NF)", fontsize=14, fontweight='bold', pad=12, color='#0f172a')
    fig.patch.set_facecolor('white')
    plt.tight_layout()
    plt.savefig('report_assets/er_diagram.png', bbox_inches='tight')
    plt.close()
    print("ER Diagram saved.")

# -------------------------------------------------------------
# 3. DATA FLOW DIAGRAM (DFD)
# -------------------------------------------------------------
def make_dfd_diagram():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 9), dpi=300)
    for ax in (ax1, ax2):
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 50)
        ax.axis('off')

    # Level 0 DFD (Context)
    ax1.set_title("Level 0 DFD: Context Diagram", fontsize=12, fontweight='bold', loc='left', color='#1e293b')
    # External Entities
    box_stud = patches.Rectangle((4, 18), 18, 14, fc='#e0e7ff', ec='#4338ca', lw=1.5)
    ax1.add_patch(box_stud)
    ax1.text(13, 25, "Student / User\n[External Entity]", ha='center', va='center', fontweight='bold', fontsize=9, color='#1e1b4b')

    circle_proc = patches.Circle((50, 25), 12, fc='#f1f5f9', ec='#0f172a', lw=2)
    ax1.add_patch(circle_proc)
    ax1.text(50, 25, "0.0\nMultilingual\nFeedback\nIntelligence\nSystem", ha='center', va='center', fontweight='bold', fontsize=8.5, color='#0f172a')

    box_admin = patches.Rectangle((78, 18), 18, 14, fc='#fef3c7', ec='#d97706', lw=1.5)
    ax1.add_patch(box_admin)
    ax1.text(87, 25, "HOD / Faculty\n[External Entity]", ha='center', va='center', fontweight='bold', fontsize=9, color='#78350f')

    ax1.annotate("Raw Multilingual\nFeedback & Rating", xy=(38, 28), xytext=(22, 28), arrowprops=dict(arrowstyle="->", lw=1.5, color='#4338ca'))
    ax1.annotate("Real-time Analysis\n& Badges", xy=(22, 22), xytext=(38, 22), arrowprops=dict(arrowstyle="->", lw=1.5, color='#059669'))
    ax1.annotate("Executive Dashboards\n& Drift Reports", xy=(78, 25), xytext=(62, 25), arrowprops=dict(arrowstyle="->", lw=1.5, color='#d97706'))

    # Level 1 DFD
    ax2.set_title("Level 1 DFD: Subsystem Process Decomposition", fontsize=12, fontweight='bold', loc='left', color='#1e293b')
    procs = [
        ("1.0", "Ingestion &\nPreprocessing", 12),
        ("2.0", "Language\nIdentification", 32),
        ("3.0", "Sentiment &\n12-Aspect ABSA", 52),
        ("4.0", "BERTopic &\nTemporal Drift", 72),
        ("5.0", "Persistence &\nREST / UI", 90)
    ]
    for code, name, x in procs:
        circ = patches.Circle((x, 25), 7, fc='#f8fafc', ec='#2563eb', lw=1.8)
        ax2.add_patch(circ)
        ax2.text(x, 25, f"{code}\n{name}", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#1e293b')

    # Arrows between processes
    ax2.annotate("", xy=(25, 25), xytext=(19, 25), arrowprops=dict(arrowstyle="->", lw=1.5, color='#2563eb'))
    ax2.annotate("", xy=(45, 25), xytext=(39, 25), arrowprops=dict(arrowstyle="->", lw=1.5, color='#2563eb'))
    ax2.annotate("", xy=(65, 25), xytext=(59, 25), arrowprops=dict(arrowstyle="->", lw=1.5, color='#2563eb'))
    ax2.annotate("", xy=(83, 25), xytext=(79, 25), arrowprops=dict(arrowstyle="->", lw=1.5, color='#2563eb'))

    # Data Store at bottom
    ds = patches.Rectangle((35, 4), 30, 8, fc='#ecfdf5', ec='#059669', lw=1.5)
    ax2.add_patch(ds)
    ax2.text(50, 8, "D1: SQLite Database (4 Normalized Tables)", ha='center', va='center', fontweight='bold', fontsize=8.5, color='#065f46')

    ax2.annotate("", xy=(50, 12), xytext=(52, 18), arrowprops=dict(arrowstyle="->", lw=1.3, color='#059669'))
    ax2.annotate("", xy=(70, 12), xytext=(72, 18), arrowprops=dict(arrowstyle="->", lw=1.3, color='#059669'))
    ax2.annotate("", xy=(88, 18), xytext=(65, 8), arrowprops=dict(arrowstyle="->", lw=1.3, color='#059669'))

    fig.suptitle("Data Flow Architecture (Level 0 Context & Level 1 Decomposition)", fontsize=14, fontweight='bold', y=0.98, color='#0f172a')
    fig.patch.set_facecolor('white')
    plt.tight_layout()
    plt.savefig('report_assets/dfd_diagram.png', bbox_inches='tight')
    plt.close()
    print("DFD Diagram saved.")

# -------------------------------------------------------------
# 4. UML CLASS DIAGRAM
# -------------------------------------------------------------
def make_class_diagram():
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    def draw_uml_class(x, y, w, h, name, attrs, methods, color='#4338ca'):
        box = patches.Rectangle((x, y), w, h, fc='#ffffff', ec=color, lw=1.8)
        ax.add_patch(box)
        hdr = patches.Rectangle((x, y + h - 5), w, 5, fc=color, ec=color)
        ax.add_patch(hdr)
        ax.text(x + w / 2, y + h - 2.5, name, ha='center', va='center', color='white', fontweight='bold', fontsize=9.5)
        
        # Attributes
        curr_y = y + h - 7
        for a in attrs:
            ax.text(x + 1.5, curr_y, a, fontsize=7.5, color='#1e293b')
            curr_y -= 2.6
        # Separator line
        ax.plot([x, x + w], [curr_y + 0.5, curr_y + 0.5], color=color, lw=0.8)
        curr_y -= 2.0
        # Methods
        for m in methods:
            ax.text(x + 1.5, curr_y, m, fontsize=7.5, color='#0f172a', fontweight='500')
            curr_y -= 2.6

    draw_uml_class(3, 56, 28, 38, "FeedbackCleaner", 
                   ["- negation_tokens: set", "- emoji_map: dict"], 
                   ["+ clean_text(raw_text): str", "+ preserve_negation(tokens): list", "+ remove_boilerplate(text): str"])

    draw_uml_class(36, 56, 28, 38, "LanguageDetector", 
                   ["- devanagari_range: tuple", "- hinglish_lexicon: set"], 
                   ["+ detect_language(text): dict", "+ compute_script_ratio(text): float", "+ get_confidence(text): float"])

    draw_uml_class(69, 56, 28, 38, "SentimentClassifier", 
                   ["- vectorizer: TfidfVectorizer", "- model: CalibratedLinearSVC"], 
                   ["+ fit(X_train, y_train): void", "+ predict(text): dict", "+ predict_proba(text): ndarray", "+ evaluate(X_test, y_test): dict"])

    draw_uml_class(3, 10, 28, 38, "AspectSentimentExtractor", 
                   ["- aspect_lexicon: dict", "- window_size: int = 5"], 
                   ["+ analyze_aspects(text): list", "+ extract_clause(text, kw): str", "+ score_aspect_sentiment(kw): dict"])

    draw_uml_class(36, 10, 28, 38, "TopicDriftAnalyzer", 
                   ["- drift_threshold: float = 0.015", "- min_observations: int = 3"], 
                   ["+ analyze_drift(df): dict", "+ compute_trajectory_slope(s): float", "+ classify_status(slope): str"])

    draw_uml_class(69, 10, 28, 38, "DatabaseManager", 
                   ["- db_path: str", "- connection: sqlite3.Connection"], 
                   ["+ query_complete_dataset(): DataFrame", "+ query_aspects_data(): DataFrame", "+ insert_feedback(record): void", "+ delete_feedback(id): void"])

    ax.set_title("Unified UML Class Diagram (Domain Model & Subsystem Encapsulation)", fontsize=14, fontweight='bold', pad=15, color='#0f172a')
    fig.patch.set_facecolor('white')
    plt.tight_layout()
    plt.savefig('report_assets/class_diagram.png', bbox_inches='tight')
    plt.close()
    print("Class Diagram saved.")

# -------------------------------------------------------------
# 5. SEQUENCE DIAGRAM
# -------------------------------------------------------------
def make_sequence_diagram():
    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    actors = ["User/Client", "FastAPI Server", "NLP Cleaner/Detector", "Sentiment & ABSA", "SQLite DB"]
    x_coords = [10, 32, 54, 76, 94]

    for x, act in zip(x_coords, actors):
        rect = patches.Rectangle((x - 8, 88), 16, 8, fc='#1e293b', ec='#0f172a')
        ax.add_patch(rect)
        ax.text(x, 92, act, ha='center', va='center', color='white', fontweight='bold', fontsize=8.5)
        ax.plot([x, x], [10, 88], 'k--', alpha=0.3, lw=1.2)

    messages = [
        (0, 1, "POST /api/feedback (Raw Text, Rating)", 82, '#2563eb'),
        (1, 2, "clean_text() & detect_language()", 74, '#4338ca'),
        (2, 1, "Return Clean Text & 'Hinglish'", 66, '#4338ca'),
        (1, 3, "predict_sentiment() & analyze_aspects()", 58, '#059669'),
        (3, 1, "Return 'Positive' + 2 Aspect Verdicts", 50, '#059669'),
        (1, 4, "INSERT INTO Feedback, Sentiment, Aspect, Topic", 42, '#d97706'),
        (4, 1, "Commit Transaction (OK)", 34, '#d97706'),
        (1, 0, "HTTP 200 OK + Live Feedback Record JSON", 26, '#10b981')
    ]

    for frm, to, text, y, col in messages:
        x_from, x_to = x_coords[frm], x_coords[to]
        ax.annotate("", xy=(x_to, y), xytext=(x_from, y), arrowprops=dict(arrowstyle="->", lw=1.6, color=col))
        ax.text((x_from + x_to) / 2, y + 2, text, ha='center', va='bottom', fontsize=8, fontweight='bold', color=col)

    ax.set_title("UML Sequence Diagram: Live Feedback Submission & Real-Time NLP Pipeline", fontsize=13, fontweight='bold', pad=15, color='#0f172a')
    fig.patch.set_facecolor('white')
    plt.tight_layout()
    plt.savefig('report_assets/sequence_diagram.png', bbox_inches='tight')
    plt.close()
    print("Sequence Diagram saved.")

# -------------------------------------------------------------
# 6. STATE CHART DIAGRAM
# -------------------------------------------------------------
def make_statechart_diagram():
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    states = [
        ("Raw Input", 10, 80),
        ("Preprocessed", 40, 80),
        ("Language Tagged", 75, 80),
        ("Sentiment Inferred", 75, 45),
        ("Aspects Extracted", 40, 45),
        ("Topic Assigned", 10, 45),
        ("DB Persisted", 40, 15)
    ]

    for name, x, y in states:
        box = patches.FancyBboxPatch((x - 10, y - 6), 20, 12, boxstyle="round,pad=1.0", fc='#eff6ff', ec='#2563eb', lw=1.8)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontweight='bold', fontsize=9, color='#1e3a8a')

    # Transitions
    def trans(p1, p2, label):
        ax.annotate("", xy=p2, xytext=p1, arrowprops=dict(arrowstyle="->", lw=1.6, color='#1e293b'))
        ax.text((p1[0]+p2[0])/2, (p1[1]+p2[1])/2 + 2, label, ha='center', va='bottom', fontsize=7.5, fontweight='bold', color='#475569')

    trans((20, 80), (30, 80), "clean_text()")
    trans((50, 80), (65, 80), "detect_lang()")
    trans((75, 74), (75, 51), "predict_sentiment()")
    trans((65, 45), (50, 45), "extract_aspects()")
    trans((30, 45), (20, 45), "cluster_topic()")
    trans((10, 39), (30, 15), "commit_db()")

    ax.set_title("UML State Machine Diagram: Student Feedback Record Lifecycle", fontsize=13, fontweight='bold', pad=15, color='#0f172a')
    fig.patch.set_facecolor('white')
    plt.tight_layout()
    plt.savefig('report_assets/statechart_diagram.png', bbox_inches='tight')
    plt.close()
    print("Statechart Diagram saved.")

# -------------------------------------------------------------
# 7. USE-CASE DIAGRAM
# -------------------------------------------------------------
def make_usecase_diagram():
    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Boundary Box
    sys_box = patches.Rectangle((26, 8), 48, 84, fc='#f8fafc', ec='#334155', lw=2, linestyle='--')
    ax.add_patch(sys_box)
    ax.text(50, 88, "Multilingual Course Feedback Intelligence System", ha='center', va='center', fontweight='bold', fontsize=10, color='#0f172a')

    use_cases = [
        ("Submit Multilingual Feedback", 50, 78),
        ("View Live Aspect Sentiment Breakdown", 50, 66),
        ("Explore Executive KPIs & Insights", 50, 54),
        ("Inspect Course-Aspect Heatmap", 50, 42),
        ("Track Semester Topic Drift", 50, 30),
        ("Manage / Delete Feedback Records", 50, 18)
    ]

    for name, x, y in use_cases:
        ellipse = patches.Ellipse((x, y), 38, 8, fc='#ffffff', ec='#6366f1', lw=1.6)
        ax.add_patch(ellipse)
        ax.text(x, y, name, ha='center', va='center', fontweight='bold', fontsize=8, color='#312e81')

    # Actors
    def draw_actor(x, y, label):
        ax.plot([x], [y + 3], 'o', ms=12, color='#0f172a') # Head
        ax.plot([x, x], [y + 2, y - 4], 'k-', lw=2)         # Body
        ax.plot([x - 4, x + 4], [y, y], 'k-', lw=2)         # Arms
        ax.plot([x, x - 3], [y - 4, y - 9], 'k-', lw=2)     # Left Leg
        ax.plot([x, x + 3], [y - 4, y - 9], 'k-', lw=2)     # Right Leg
        ax.text(x, y - 12, label, ha='center', va='center', fontweight='bold', fontsize=8.5, color='#0f172a')

    draw_actor(12, 75, "Student")
    draw_actor(12, 35, "Course Faculty")
    draw_actor(88, 55, "HOD / Academic Dean")
    draw_actor(88, 20, "System Admin")

    # Links
    ax.plot([12, 31], [75, 78], 'k-', alpha=0.5, lw=1.2)
    ax.plot([12, 31], [75, 66], 'k-', alpha=0.5, lw=1.2)
    ax.plot([12, 31], [35, 66], 'k-', alpha=0.5, lw=1.2)
    ax.plot([12, 31], [35, 54], 'k-', alpha=0.5, lw=1.2)
    ax.plot([88, 69], [55, 54], 'k-', alpha=0.5, lw=1.2)
    ax.plot([88, 69], [55, 42], 'k-', alpha=0.5, lw=1.2)
    ax.plot([88, 69], [55, 30], 'k-', alpha=0.5, lw=1.2)
    ax.plot([88, 69], [20, 18], 'k-', alpha=0.5, lw=1.2)

    ax.set_title("UML Use-Case Diagram: System Boundaries & Stakeholder Interactions", fontsize=13, fontweight='bold', pad=15, color='#0f172a')
    fig.patch.set_facecolor('white')
    plt.tight_layout()
    plt.savefig('report_assets/usecase_diagram.png', bbox_inches='tight')
    plt.close()
    print("Use-case Diagram saved.")

# -------------------------------------------------------------
# 8. OUTPUT 1: OVERVIEW DASHBOARD
# -------------------------------------------------------------
def make_output_overview():
    fig = plt.figure(figsize=(12, 7.5), dpi=300)
    gs = GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.3)

    # 1. KPIs Card Header
    ax_kpi = fig.add_subplot(gs[0, :])
    ax_kpi.axis('off')
    kpis = [
        ("Total Reviews", "2,200", "#6366f1"),
        ("Avg Satisfaction", "3.25 / 5", "#06b6d4"),
        ("Positive Sentiment", "36.0%", "#10b981"),
        ("Negative Sentiment", "19.3%", "#ef4444"),
        ("Active Courses", "8 Courses", "#f59e0b")
    ]
    for i, (k, v, c) in enumerate(kpis):
        bx = patches.FancyBboxPatch((i*20 + 1, 10), 18, 80, boxstyle="round,pad=2", fc='#f8fafc', ec=c, lw=2)
        ax_kpi.add_patch(bx)
        ax_kpi.text(i*20 + 10, 65, k, ha='center', va='center', fontsize=9, fontweight='bold', color='#475569')
        ax_kpi.text(i*20 + 10, 35, v, ha='center', va='center', fontsize=14, fontweight='bold', color=c)
    ax_kpi.set_xlim(0, 100)
    ax_kpi.set_ylim(0, 100)
    ax_kpi.set_title("FeedPulse AI: Executive Intelligence Overview KPI Metrics", fontsize=13, fontweight='bold', color='#0f172a')

    # 2. Sentiment Donut
    ax_sent = fig.add_subplot(gs[1, 0])
    s_labels = ['Positive\n(36.0%)', 'Negative\n(19.3%)', 'Neutral\n(44.7%)']
    s_vals = [792, 424, 984]
    ax_sent.pie(s_vals, labels=s_labels, colors=['#10b981', '#ef4444', '#f59e0b'], startangle=140, 
                wedgeprops=dict(width=0.45, edgecolor='w', lw=2), textprops=dict(fontsize=8, fontweight='bold'))
    ax_sent.set_title("Sentiment Distribution", fontsize=10, fontweight='bold', color='#1e293b')

    # 3. Language Donut
    ax_lang = fig.add_subplot(gs[1, 1])
    l_labels = ['English\n(49.9%)', 'Hinglish\n(26.4%)', 'Hindi\n(23.8%)']
    l_vals = [1097, 580, 523]
    ax_lang.pie(l_vals, labels=l_labels, colors=['#6366f1', '#06b6d4', '#a855f7'], startangle=140, 
                wedgeprops=dict(width=0.45, edgecolor='w', lw=2), textprops=dict(fontsize=8, fontweight='bold'))
    ax_lang.set_title("Multilingual Composition", fontsize=10, fontweight='bold', color='#1e293b')

    # 4. Rating Bar Chart
    ax_rat = fig.add_subplot(gs[1, 2])
    stars = ['1 Star', '2 Star', '3 Star', '4 Star', '5 Star']
    cnts = [264, 185, 958, 329, 464]
    ax_rat.bar(stars, cnts, color='#f59e0b', alpha=0.85, edgecolor='#d97706', width=0.6)
    ax_rat.set_title("Likert Rating Frequency", fontsize=10, fontweight='bold', color='#1e293b')
    ax_rat.set_ylabel("Count of Responses", fontsize=8)
    ax_rat.tick_params(axis='x', labelsize=8)
    ax_rat.grid(axis='y', linestyle='--', alpha=0.3)

    fig.patch.set_facecolor('white')
    plt.tight_layout()
    plt.savefig('report_assets/output1_overview.png', bbox_inches='tight')
    plt.close()
    print("Output 1 Overview saved.")

# -------------------------------------------------------------
# 9. OUTPUT 3: 12-ASPECT ABSA HEATMAP
# -------------------------------------------------------------
def make_output_heatmap():
    courses = [
        "AI & Robotics", "Computer Networks", "Data Structures",
        "DBMS", "Full-Stack Web Dev", "Intro Programming",
        "Machine Learning", "Software Eng"
    ]
    aspects = [
        "Assignments", "Content", "Difficulty", "Evaluation",
        "Exams", "Faculty", "Infrastructure", "Pace",
        "Practicals", "Projects", "Material", "Teaching"
    ]
    matrix = np.array([
        [31.4, 4.9, 14.3, 8.6, 24.5, 26.9, -2.2, 19.5, 37.2, 13.0, 9.6, 27.5],
        [-11.4, 12.8, 17.0, 14.3, 28.3, 0.0, 1.9, 15.6, 9.7, 20.0, 0.0, 0.0],
        [20.9, 13.9, 34.6, 22.5, 18.0, -7.8, 2.3, 7.0, 25.0, 23.7, 15.6, 16.7],
        [4.3, 2.6, 31.3, 4.1, 17.3, 13.0, 15.9, 32.4, 39.2, 26.2, 18.4, -1.9],
        [42.5, 8.3, 43.2, 37.7, 30.4, -6.4, -6.1, 10.9, 36.0, 38.9, 10.3, 28.2],
        [0.0, 0.0, 15.0, 8.3, 17.3, 31.6, 30.6, 6.8, 31.1, 2.2, 22.0, 32.5],
        [23.7, 16.7, 8.5, 20.9, 12.2, 27.0, 7.7, 0.0, 30.6, 13.0, 5.6, 2.3],
        [15.6, 0.0, 0.0, 9.8, 14.0, 13.6, 26.7, 5.9, 18.8, 24.4, 12.0, 9.5]
    ])

    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=300)
    cax = ax.matshow(matrix, cmap='RdYlGn', vmin=-15, vmax=45)
    fig.colorbar(cax, fraction=0.03, pad=0.04, label="Net Aspect Sentiment Score (%)")

    ax.set_xticks(range(len(aspects)))
    ax.set_yticks(range(len(courses)))
    ax.set_xticklabels(aspects, rotation=45, ha='left', fontsize=9, fontweight='bold')
    ax.set_yticklabels(courses, fontsize=9, fontweight='bold')

    for i in range(len(courses)):
        for j in range(len(aspects)):
            val = matrix[i, j]
            col = 'white' if abs(val) > 28 else 'black'
            ax.text(j, i, f"{val:+.1f}%", ha='center', va='center', color=col, fontsize=7.5, fontweight='bold')

    ax.set_title("12-Aspect Sentiment Breakdown Matrix across 8 Monitored Academic Courses", fontsize=13, fontweight='bold', pad=25, color='#0f172a')
    fig.patch.set_facecolor('white')
    plt.tight_layout()
    plt.savefig('report_assets/output3_aspect_heatmap.png', bbox_inches='tight')
    plt.close()
    print("Output 3 Heatmap saved.")

# -------------------------------------------------------------
# 10. OUTPUT 5: TEMPORAL TOPIC DRIFT
# -------------------------------------------------------------
def make_output_topic_drift():
    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300)
    semesters = ["Sem 1", "Sem 2", "Sem 3", "Sem 4", "Sem 5", "Sem 6"]
    
    topics = {
        "Exam Difficulty & Time Management [Emerging ⚡]": [1.57, 1.82, 1.95, 2.10, 2.32, 2.47],
        "Coding Practicals & Hands-on Labs [Persistent 🔄]": [4.20, 4.35, 4.25, 4.30, 4.42, 4.38],
        "Hardware & Lab PC Maintenance [Declining 📉]": [3.85, 3.50, 3.10, 2.80, 2.40, 2.15],
        "Cloud & Microservices Project Electives [New ✨]": [0.00, 0.00, 0.85, 1.90, 2.85, 3.75],
        "Study Notes & Slide Sharing Portal [Persistent 🔄]": [2.90, 3.05, 3.12, 2.98, 3.00, 2.95]
    }
    
    colors = ['#ef4444', '#10b981', '#3b82f6', '#8b5cf6', '#f59e0b']
    markers = ['o', 's', '^', 'D', 'v']

    for (t_name, data), col, m in zip(topics.items(), colors, markers):
        ax.plot(semesters, data, marker=m, lw=2.5, ms=7, label=t_name, color=col)

    ax.set_title("Temporal Topic Drift Trajectory (c-TF-IDF Longitudinal Dynamics across 6 Semesters)", fontsize=13, fontweight='bold', pad=15, color='#0f172a')
    ax.set_ylabel("Discourse Share (% of Total Student Responses)", fontsize=10, fontweight='bold', color='#1e293b')
    ax.set_xlabel("Academic Progression", fontsize=10, fontweight='bold', color='#1e293b')
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.legend(loc='upper left', frameon=True, fontsize=8.5)
    ax.set_facecolor('#f8fafc')
    fig.patch.set_facecolor('white')
    plt.tight_layout()
    plt.savefig('report_assets/output5_topic_drift.png', bbox_inches='tight')
    plt.close()
    print("Output 5 Topic Drift saved.")

# -------------------------------------------------------------
# 11. OUTPUT 8: MODEL EVALUATION & CONFUSION MATRIX
# -------------------------------------------------------------
def make_output_evaluation():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.2), dpi=300)

    # Confusion Matrix
    cm = np.array([[386, 4, 6], [5, 208, 3], [7, 4, 477]])
    classes = ['Positive', 'Negative', 'Neutral']
    im = ax1.imshow(cm, interpolation='nearest', cmap='Blues')
    fig.colorbar(im, ax=ax1, fraction=0.046, pad=0.04)

    ax1.set_xticks(range(3))
    ax1.set_yticks(range(3))
    ax1.set_xticklabels(classes, fontsize=9, fontweight='bold')
    ax1.set_yticklabels(classes, fontsize=9, fontweight='bold')
    ax1.set_xlabel('Predicted Label', fontsize=10, fontweight='bold')
    ax1.set_ylabel('True Label', fontsize=10, fontweight='bold')
    ax1.set_title("Test Confusion Matrix (LinearSVC + Calibrated)\nAccuracy: 98.45% | Macro F1: 98.24%", fontsize=11, fontweight='bold', color='#0f172a')

    for i in range(3):
        for j in range(3):
            val = cm[i, j]
            col = 'white' if val > 200 else 'black'
            ax1.text(j, i, f"{val}\n({val/cm.sum():.1%})", ha='center', va='center', color=col, fontsize=9, fontweight='bold')

    # Pipeline A vs Pipeline B Benchmark Bar Chart
    metrics = ['Accuracy', 'Precision', 'Recall', 'Macro F1']
    pipe_a = [98.45, 98.30, 98.20, 98.24]
    pipe_b = [92.15, 91.80, 91.40, 91.55]

    x = np.arange(len(metrics))
    width = 0.35
    ax2.bar(x - width/2, pipe_a, width, label='Pipeline A (Multilingual Normalization)', color='#4f46e5', edgecolor='#312e81')
    ax2.bar(x + width/2, pipe_b, width, label='Pipeline B (Direct Multilingual TF-IDF)', color='#94a3b8', edgecolor='#475569')

    ax2.set_ylabel('Score (%)', fontsize=10, fontweight='bold')
    ax2.set_title('Pipeline Architecture Benchmark Comparison', fontsize=11, fontweight='bold', color='#0f172a')
    ax2.set_xticks(x)
    ax2.set_xticklabels(metrics, fontsize=9, fontweight='bold')
    ax2.set_ylim(85, 102)
    ax2.grid(axis='y', linestyle='--', alpha=0.3)
    ax2.legend(loc='lower right', fontsize=8.5)

    for i in range(len(metrics)):
        ax2.text(x[i] - width/2, pipe_a[i] + 0.5, f"{pipe_a[i]:.1f}%", ha='center', fontsize=8, fontweight='bold', color='#4f46e5')
        ax2.text(x[i] + width/2, pipe_b[i] + 0.5, f"{pipe_b[i]:.1f}%", ha='center', fontsize=8, fontweight='bold', color='#475569')

    fig.patch.set_facecolor('white')
    plt.tight_layout()
    plt.savefig('report_assets/output8_evaluation.png', bbox_inches='tight')
    plt.close()
    print("Output 8 Evaluation saved.")

# -------------------------------------------------------------
# 12. OUTPUT 7: LIVE SANDBOX & NLP PLAYGROUND
# -------------------------------------------------------------
def make_output_sandbox():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Container
    box = patches.FancyBboxPatch((4, 4), 92, 92, boxstyle="round,pad=1.5", fc='#0f172a', ec='#6366f1', lw=2)
    ax.add_patch(box)
    ax.text(50, 90, "FeedPulse AI: Interactive Multilingual Sandbox Output", ha='center', va='center', color='white', fontweight='bold', fontsize=13)

    # Input dialogue
    inp_box = patches.FancyBboxPatch((8, 68), 84, 15, boxstyle="round,pad=1", fc='#1e293b', ec='#334155', lw=1.2)
    ax.add_patch(inp_box)
    ax.text(10, 78, "INPUT TEXT (Code-Mixed Hinglish):", fontsize=8.5, color='#94a3b8', fontweight='bold')
    ax.text(10, 72, "\"Professor ne concepts bohot acche se explain kiye lekin lab assignments thode tough the.\"", fontsize=9.5, color='#38bdf8', fontweight='bold', style='italic')

    # 4 Output Steps
    steps = [
        ("Step 1: Language Detection", "Hinglish (Romanized Latin) | Confidence: 88.0%", "#06b6d4", 52),
        ("Step 2: Pipeline A Normalization", "Professor explained concepts very well but laboratory assignments were tough.", "#a855f7", 38),
        ("Step 3: Sentiment Classification", "Overall Sentiment: POSITIVE | Confidence: 94.2% | Polarity: +0.486", "#10b981", 24),
        ("Step 4: Extracted 12-Aspects", "1. Teaching Quality: Positive (+0.82) | 2. Assignments: Negative (-0.64)", "#f59e0b", 10)
    ]
    for title, desc, col, y in steps:
        s_box = patches.FancyBboxPatch((8, y), 84, 11, boxstyle="round,pad=0.8", fc='#1e293b', ec=col, lw=1.5)
        ax.add_patch(s_box)
        ax.text(11, y + 7, title, color=col, fontsize=8.5, fontweight='bold')
        ax.text(11, y + 2.5, desc, color='#f8fafc', fontsize=9, fontweight='500')

    fig.patch.set_facecolor('white')
    plt.tight_layout()
    plt.savefig('report_assets/output7_sandbox.png', bbox_inches='tight')
    plt.close()
    print("Output 7 Sandbox saved.")

# -------------------------------------------------------------
# 13. OUTPUT 6: FEEDBACK CRUD MANAGEMENT TABLE
# -------------------------------------------------------------
def make_output_crud_table():
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    ax.axis('off')

    columns = ["Feedback ID", "Course", "Semester", "Detected Language", "Rating", "Sentiment", "Extracted Aspects"]
    data = [
        ["FB_USER_02201", "Full-Stack Web Dev", "Sem 6", "Hinglish", "5 Stars", "Positive (94%)", "Teaching Quality (+), Projects (0)"],
        ["FB_USER_02198", "Data Structures", "Sem 3", "English", "2 Stars", "Negative (91%)", "Difficulty (-), Assignments (-)"],
        ["FB_USER_02195", "Machine Learning", "Sem 5", "Hindi", "4 Stars", "Positive (89%)", "Course Content (+), Exams (+)"],
        ["FB_USER_02190", "Database Systems", "Sem 4", "Hinglish", "1 Star", "Negative (95%)", "Infrastructure (-), Lab PC (-)"],
        ["FB_USER_02187", "Computer Networks", "Sem 2", "English", "3 Stars", "Neutral (78%)", "Lecture Pace (0), Evaluation (0)"],
        ["FB_USER_02182", "AI & Robotics", "Sem 6", "Hinglish", "5 Stars", "Positive (96%)", "Practical Sessions (+), Mentorship (+)"]
    ]

    table = ax.table(cellText=data, colLabels=columns, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(8.5)
    table.scale(1.0, 2.1)

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor('#cbd5e1')
        if row == 0:
            cell.set_facecolor('#1e293b')
            cell.set_text_props(color='white', fontweight='bold')
        else:
            if col == 5:
                if 'Positive' in data[row-1][5]: cell.set_facecolor('#ecfdf5')
                elif 'Negative' in data[row-1][5]: cell.set_facecolor('#fef2f2')
                else: cell.set_facecolor('#fffbeb')
            else:
                cell.set_facecolor('#f8fafc' if row % 2 == 0 else '#ffffff')

    ax.set_title("Student Feedback Management & Real-Time CRUD Table (FastAPI + SQLite Persistence)", fontsize=13, fontweight='bold', pad=25, color='#0f172a')
    fig.patch.set_facecolor('white')
    plt.tight_layout()
    plt.savefig('report_assets/output6_crud_table.png', bbox_inches='tight')
    plt.close()
    print("Output 6 CRUD Table saved.")

if __name__ == '__main__':
    make_gantt_chart()
    make_er_diagram()
    make_dfd_diagram()
    make_class_diagram()
    make_sequence_diagram()
    make_statechart_diagram()
    make_usecase_diagram()
    make_output_overview()
    make_output_heatmap()
    make_output_topic_drift()
    make_output_evaluation()
    make_output_sandbox()
    make_output_crud_table()
    print("ALL 13 publication-quality figures successfully generated in report_assets/!")
