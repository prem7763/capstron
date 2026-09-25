"""
Synthetic Multilingual Student Feedback Dataset Generator.
Generates realistic multilingual (English, Hindi, Hinglish) feedback across 8 courses,
6 semesters, 12 course aspects, multi-aspect sentiments, and realistic topic drift over time.
"""

import os
import random
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

COURSES = [
    {"code": "CS101", "name": "Introduction to Programming", "dept": "Computer Science"},
    {"code": "DS201", "name": "Data Structures & Algorithms", "dept": "Computer Science"},
    {"code": "DB202", "name": "Database Management Systems", "dept": "Information Technology"},
    {"code": "ML301", "name": "Machine Learning & Neural Networks", "dept": "Data Science"},
    {"code": "SE303", "name": "Software Engineering & Architecture", "dept": "Software Engineering"},
    {"code": "CN204", "name": "Computer Networks & Security", "dept": "Computer Science"},
    {"code": "AI401", "name": "Artificial Intelligence & Robotics", "dept": "Data Science"},
    {"code": "WD102", "name": "Full-Stack Web Development", "dept": "Information Technology"},
]

SEMESTERS = ["Sem 1", "Sem 2", "Sem 3", "Sem 4", "Sem 5", "Sem 6"]

ASPECTS = [
    "Teaching Quality",
    "Course Content",
    "Assignments",
    "Exams",
    "Difficulty",
    "Lecture Pace",
    "Faculty Support",
    "Practical Sessions",
    "Projects",
    "Study Material",
    "Infrastructure",
    "Evaluation",
]

# Vocabulary snippets for English, Hindi, and Hinglish per aspect and sentiment
TEMPLATES = {
    "English": {
        "Teaching Quality": {
            "pos": [
                "Professor explains complex concepts with extreme clarity and patience.",
                "The teaching methodology is interactive and very engaging.",
                "The instructor makes even dry theoretical topics interesting.",
                "Lectures are exceptionally well structured and easy to follow."
            ],
            "neg": [
                "The professor just reads off the presentation slides without explaining fundamentals.",
                "The teaching style is monotonous and lacks clear demonstrations.",
                "The instructor seems unprepared during theoretical lectures.",
                "Explanations are very convoluted and hard to grasp."
            ],
            "neu": [
                "Teaching is standard and follows the prescribed syllabus closely.",
                "The professor delivers the textbook content adequately.",
                "Lectures are okay, neither particularly inspiring nor bad."
            ]
        },
        "Course Content": {
            "pos": [
                "The syllabus is modern, up to date, and aligned with industry standards.",
                "The curriculum covers both solid theory and real-world applications.",
                "Great selection of cutting-edge case studies in the coursework."
            ],
            "neg": [
                "The course content is outdated and still teaches deprecated frameworks.",
                "Curriculum is excessively theoretical with very little practical relevance.",
                "Too much overlap with previous introductory courses, adds little value."
            ],
            "neu": [
                "The topics covered are standard university curriculum requirements.",
                "Content covers general fundamentals as expected from the syllabus."
            ]
        },
        "Assignments": {
            "pos": [
                "Assignments were practical, thought-provoking, and strengthened our coding skills.",
                "Weekly homework exercises directly reinforced the lecture material.",
                "Clear guidelines and rubrics were provided for every assignment."
            ],
            "neg": [
                "Assignments are excessively lengthy and deadlines are unreasonably tight.",
                "Homework problem statements are ambiguous and poorly specified.",
                "Too many repetitive assignments leaving no time for self-study."
            ],
            "neu": [
                "Assignments were standard textbook problems with typical weekly deadlines.",
                "Homework workload was average throughout the term."
            ]
        },
        "Exams": {
            "pos": [
                "Exams were well balanced and fairly tested our conceptual understanding.",
                "Midterm questions were creative yet completely solvable within the allotted time.",
                "The exam pattern accurately reflected what was practiced in class."
            ],
            "neg": [
                "The final exam was unexpectedly harsh and disconnected from lecture topics.",
                "The test duration was way too short for such heavy numerical problems.",
                "Tricky questions designed to fail students rather than test real knowledge."
            ],
            "neu": [
                "Exams had a mix of easy and difficult questions conforming to standard patterns.",
                "Midterm was moderately paced and covered expected units."
            ]
        },
        "Difficulty": {
            "pos": [
                "The difficulty curve is well structured, ramping up gently from fundamentals.",
                "Challenging problems pushed us to think critically without causing burnout.",
                "Appropriate level of rigor for this academic stage."
            ],
            "neg": [
                "The difficulty level is brutal and assumes way too many advanced prerequisites.",
                "The course jumped from basic syntax straight to unsolvable hard problems.",
                "Unnecessarily difficult conceptual proofs that cause immense stress."
            ],
            "neu": [
                "Difficulty was moderate, manageable with consistent weekly study.",
                "Level of challenge matched other departmental subjects."
            ]
        },
        "Lecture Pace": {
            "pos": [
                "The pace of the lectures is perfect, giving ample time to take notes.",
                "Professor pauses regularly to check if everyone is following along.",
                "Pacing is steady and well distributed across all modules."
            ],
            "neg": [
                "The lecture pace is way too fast, rushing through crucial theorems.",
                "Professor flies through 40 complex slides in one single hour.",
                "Too rushed towards the end of semester to finish pending syllabus."
            ],
            "neu": [
                "Lecture speed was normal and covered topics on schedule.",
                "Pace varies depending on the topic but is mostly acceptable."
            ]
        },
        "Faculty Support": {
            "pos": [
                "Professor and TAs are remarkably approachable during office hours.",
                "Doubts were answered quickly and thoroughly on the discussion forum.",
                "Faculty genuinely cares about student learning and emotional well-being."
            ],
            "neg": [
                "Faculty is completely unresponsive to emails and student queries.",
                "TAs are unhelpful and dismissive during doubt-clearing sessions.",
                "Zero guidance provided when students struggle with core concepts."
            ],
            "neu": [
                "Faculty is accessible during designated office hours when scheduled.",
                "Doubts are addressed as per standard protocol."
            ]
        },
        "Practical Sessions": {
            "pos": [
                "Hands-on lab sessions were excellent and reinforced lecture theory.",
                "Step-by-step lab sheets made practical implementation seamless.",
                "Gained tremendous practical confidence building actual projects in lab."
            ],
            "neg": [
                "Lab sessions are disorganized and lack proper mentor guidance.",
                "Practical exercises were just copy-pasting code without understanding.",
                "Lab manuals have outdated instructions and broken dependencies."
            ],
            "neu": [
                "Labs followed standard exercises from the departmental manual.",
                "Practical sessions were routine weekly coding tasks."
            ]
        },
        "Projects": {
            "pos": [
                "Capstone project provided fantastic real-world engineering exposure.",
                "Working on the group project helped bridge theory and industry practice.",
                "Project reviews were constructive and offered invaluable architectural feedback."
            ],
            "neg": [
                "Project expectations were extremely vague and constantly changing.",
                "Teammate evaluation was unfair and mentor offered zero guidance.",
                "Overwhelming project scope without adequate technical support."
            ],
            "neu": [
                "Project guidelines were standard and completed in allocated weeks.",
                "Course project was an average implementation task."
            ]
        },
        "Study Material": {
            "pos": [
                "Lecture notes and reference repositories provided are top tier.",
                "Curated reference papers and textbook readings were very helpful.",
                "Slide decks were concise, clean, and contained helpful code snippets."
            ],
            "neg": [
                "Shared slides are full of typos and lack explanatory descriptions.",
                "No proper reference notes or textbooks were recommended.",
                "Course portal links were broken and slides were uploaded weeks late."
            ],
            "neu": [
                "Standard slides and textbook chapters were shared on the portal.",
                "Study material was adequate for passing the examinations."
            ]
        },
        "Infrastructure": {
            "pos": [
                "Campus computing lab has fast workstations and modern GPUs for ML training.",
                "High-speed Wi-Fi and well-maintained software environments in labs.",
                "Classroom audio-visual setup and projection were crisp and clear."
            ],
            "neg": [
                "Lab PCs are slow, crash repeatedly, and lack required development tools.",
                "Wi-Fi connectivity in lecture hall and labs is frustratingly unreliable.",
                "Classroom air conditioning and projectors are frequently broken."
            ],
            "neu": [
                "Infrastructure is standard university setup with basic desktop systems.",
                "Classroom facilities were ordinary and functional."
            ]
        },
        "Evaluation": {
            "pos": [
                "Grading was transparent, consistent, and strictly followed the rubric.",
                "Detailed constructive feedback was provided on all test papers.",
                "Evaluation criteria were clearly communicated at the start of term."
            ],
            "neg": [
                "Grading felt totally arbitrary and marks were deducted without explanation.",
                "Huge delay in publishing test marks, with zero feedback on errors.",
                "Unfair evaluation where different TAs marked identical work inconsistently."
            ],
            "neu": [
                "Evaluation was normal and results were announced on the portal.",
                "Grading followed the usual departmental bell curve."
            ]
        }
    },
    "Hindi": {
        "Teaching Quality": {
            "pos": [
                "प्रोफेसर बहुत ही सरल और स्पष्ट तरीके से पढ़ाते हैं।",
                "पढ़ाने की शैली बहुत इंटरैक्टिव है और हर छात्र को समझ आती है।",
                "शिक्षक जटिल सिद्धांतों को भी वास्तविक उदाहरणों के साथ समझाते हैं।"
            ],
            "neg": [
                "प्रोफेसर सिर्फ स्लाइड्स पढ़कर सुना देते हैं, कुछ समझाते नहीं।",
                "पढ़ाने का तरीका बहुत उबाऊ है और बुनियादी बातें स्पष्ट नहीं होतीं।",
                "कक्षा में कोई उत्साह नहीं रहता और व्याख्यान अस्पष्ट हैं।"
            ],
            "neu": [
                "पढ़ाने का तरीका सामान्य है और पाठ्यक्रम के अनुसार चलता है।",
                "शिक्षण मानक स्तर का है, न बहुत अच्छा न बहुत बुरा।"
            ]
        },
        "Course Content": {
            "pos": [
                "पाठ्यक्रम काफी आधुनिक है और उद्योग की जरूरतों के अनुरूप है।",
                "विषय वस्तु बहुत समृद्ध और व्यावहारिक ज्ञान से भरपूर है।"
            ],
            "neg": [
                "पाठ्यक्रम पुराना है और वर्तमान समय के अनुरूप नहीं है।",
                "केवल किताबी ज्ञान पर जोर है, व्यावहारिक कुछ भी नहीं है।"
            ],
            "neu": [
                "पाठ्यक्रम विश्वविद्यालय के सामान्य मानकों के अनुरूप है।"
            ]
        },
        "Assignments": {
            "pos": [
                "असाइनमेंट बहुत ही ज्ञानवर्धक और कोडिंग कौशल बढ़ाने वाले थे।",
                "गृहकार्य से परीक्षा की तैयारी में बहुत मदद मिली।"
            ],
            "neg": [
                "असाइनमेंट बहुत लंबे हैं और जमा करने की समयसीमा बहुत कम है।",
                "प्रश्नों के निर्देश स्पष्ट नहीं हैं और छात्रों पर भारी दबाव रहता है।"
            ],
            "neu": [
                "असाइनमेंट सामान्य स्तर के थे और समय पर जमा हो गए।"
            ]
        },
        "Exams": {
            "pos": [
                "परीक्षा का स्तर बहुत संतुलित था और कक्षा में पढ़ाए गए विषयों पर आधारित था।",
                "प्रश्न पत्र सोचने पर मजबूर करने वाला लेकिन हल करने योग्य था।"
            ],
            "neg": [
                "परीक्षा बहुत कठिन थी और समय बहुत ही कम दिया गया।",
                "प्रश्न पत्र में ऐसे सवाल पूछे गए जो कक्षा में कभी नहीं पढ़ाए गए।"
            ],
            "neu": [
                "परीक्षा सामान्य थी, कुछ प्रश्न आसान और कुछ मध्यम थे।"
            ]
        },
        "Difficulty": {
            "pos": [
                "विषय की कठिनाई का स्तर बहुत संतुलित और व्यवस्थित है।",
                "कठिन विषयों को भी चरणबद्ध तरीके से आसान बना दिया गया।"
            ],
            "neg": [
                "यह कोर्स अनावश्यक रूप से बहुत कठिन और तनावपूर्ण है।",
                "बुनियादी समझ के बिना ही सीधे कठिन विषयों पर चले गए।"
            ],
            "neu": [
                "कठिनाई का स्तर औसत था, नियमित पढ़ाई से हो गया।"
            ]
        },
        "Lecture Pace": {
            "pos": [
                "व्याख्यान की गति बहुत अच्छी है और नोट्स बनाने का पूरा समय मिलता है।",
                "शिक्षक सभी छात्रों की समझ के अनुसार ही आगे बढ़ते हैं।"
            ],
            "neg": [
                "पढ़ाने की गति बहुत तेज है, कुछ भी समझ नहीं आता।",
                "सिलेबस पूरा करने के चक्कर में बहुत तेजी से भागते हैं।"
            ],
            "neu": [
                "व्याख्यान की गति सामान्य और संतुलित रही।"
            ]
        },
        "Faculty Support": {
            "pos": [
                "शिक्षक हमेशा शंकाएं दूर करने के लिए उपलब्ध रहते हैं।",
                "छात्रों की सहायता के लिए प्रोफेसर का रवैया बहुत सकारात्मक है।"
            ],
            "neg": [
                "शिक्षक ईमेल का जवाब नहीं देते और संदेह पूछने पर डांटते हैं।",
                "छात्रों की समस्याओं पर कोई ध्यान नहीं दिया जाता।"
            ],
            "neu": [
                "निर्धारित समय पर ही शिक्षक से मिलना संभव हो पाता है।"
            ]
        },
        "Practical Sessions": {
            "pos": [
                "प्रैक्टिकल लैब सत्र बहुत ही शानदार और उपयोगी थे।",
                "लैब में खुद कोड चलाकर सीखने का बहुत अच्छा अवसर मिला।"
            ],
            "neg": [
                "लैब सत्र बहुत अव्यवस्थित हैं और कोई मार्गदर्शन नहीं मिलता।",
                "प्रैक्टिकल में केवल कोड कॉपी-पेस्ट करवाया जाता है।"
            ],
            "neu": [
                "लैब का काम सामान्य था और तय समय में पूरा हुआ।"
            ]
        },
        "Projects": {
            "pos": [
                "प्रोजेक्ट कार्य से बहुत कुछ नया सीखने को मिला।",
                "टीम प्रोजेक्ट का अनुभव काफी प्रेरणादायक और व्यावहारिक रहा।"
            ],
            "neg": [
                "प्रोजेक्ट के दिशानिर्देश बहुत अस्पष्ट और भ्रामक थे।",
                "प्रोजेक्ट के मूल्यांकन में पक्षपात देखने को मिला।"
            ],
            "neu": [
                "प्रोजेक्ट सामान्य स्तर का था जैसा अन्य विषयों में होता है।"
            ]
        },
        "Study Material": {
            "pos": [
                "अध्ययन सामग्री और नोट्स बहुत ही उपयोगी और स्पष्ट हैं।",
                "साझा की गई किताबें और संदर्भ सामग्री परीक्षा में बहुत काम आईं।"
            ],
            "neg": [
                "नोट्स में बहुत सी गलतियां हैं और कोई अच्छी किताब नहीं बताई गई।",
                "अध्ययन सामग्री समय पर पोर्टल पर अपलोड नहीं की जाती।"
            ],
            "neu": [
                "अध्ययन सामग्री सामान्य थी, परीक्षा पास करने के लिए पर्याप्त।"
            ]
        },
        "Infrastructure": {
            "pos": [
                "कंप्यूटर लैब और इंटरनेट की सुविधा बहुत तेज और आधुनिक है।",
                "कक्षा में प्रोजेक्टर और बैठने की व्यवस्था बहुत अच्छी है।"
            ],
            "neg": [
                "लैब के कंप्यूटर बहुत पुराने हैं और बार-बार हैंग होते हैं।",
                "कक्षा में वाई-फाई बिल्कुल काम नहीं करता और एसी भी खराब है।"
            ],
            "neu": [
                "बुनियादी ढांचा सामान्य है, काम चलाने लायक व्यवस्था है।"
            ]
        },
        "Evaluation": {
            "pos": [
                "मूल्यांकन प्रणाली बहुत निष्पक्ष और पारदर्शी रही।",
                "मार्क्स के साथ सुधार के लिए विस्तृत सुझाव भी दिए गए।"
            ],
            "neg": [
                "नंबर देने में मनमानी की गई और कोई स्पष्टीकरण नहीं दिया गया।",
                "रिजल्ट बहुत देरी से आया और कॉपी चेक करने में लापरवाही हुई।"
            ],
            "neu": [
                "मूल्यांकन सामान्य प्रक्रिया के अनुसार किया गया।"
            ]
        }
    },
    "Hinglish": {
        "Teaching Quality": {
            "pos": [
                "Prof sir ka explanation level next level hai, har doubt clear ho gaya.",
                "Teaching method bohot interactive hai aur lecture kabhi boring nahi lagta.",
                "Sir concepts ko real world examples ke sath connect karke bohot badhiya padhate hain."
            ],
            "neg": [
                "Teacher bas slides read karte hain, practical concepts kuch nahi samjhate.",
                "Teaching style bohot dull hai aur concepts samajh aana mushkil hai.",
                "Professor properly explain nahi karte, bas syllabus rush karte hain."
            ],
            "neu": [
                "Teaching normal thi, jaise regular college classes mein hoti hai.",
                "Syllabus cover ho gaya time pe, average teaching quality."
            ]
        },
        "Course Content": {
            "pos": [
                "Course curriculum bohot relevant aur industry standard ke hisab se designed hai.",
                "Content bohot interesting hai, practical knowledge kaafi mili."
            ],
            "neg": [
                "Content bohot outdated hai, modern frameworks aur tools nahi sikhaye.",
                "Syllabus pura theoretical hai, real practical relevance zero hai."
            ],
            "neu": [
                "Course content standard university curriculum ke according hi tha."
            ]
        },
        "Assignments": {
            "pos": [
                "Assignments challenging the aur unse coding logic kaafi improve hua.",
                "Weekly problem sets se lecture concepts bilkul crystal clear ho gaye."
            ],
            "neg": [
                "Assignments bohot lengthy hain aur submission deadlines bohot tight rakhi hain.",
                "Questions ka statement confusing hai aur assignment ka workload overwhelming hai."
            ],
            "neu": [
                "Assignments moderate the aur deadlines standard thi."
            ]
        },
        "Exams": {
            "pos": [
                "Exam paper well balanced tha, jo padha tha wahi aaya.",
                "Questions tricky the but paper fair aur time-bound tha."
            ],
            "neg": [
                "Final exam paper bohot out of syllabus aur overly tough tha.",
                "Exam hall mein time bohot kam mila itne lengthy questions ke liye."
            ],
            "neu": [
                "Exam normal tha, mix of easy and difficult questions."
            ]
        },
        "Difficulty": {
            "pos": [
                "Course difficulty well paced hai, basics se advanced smooth transition tha.",
                "Tough concepts ko step-by-step simplify kiya gaya."
            ],
            "neg": [
                "Course unnecessarily hard hai aur prerequisites clear nahi the.",
                "Difficulty level bohot high hai, avg students ke liye cope karna mushkil hai."
            ],
            "neu": [
                "Difficulty moderate thi, thoda extra effort dalke pass ho sakte hain."
            ]
        },
        "Lecture Pace": {
            "pos": [
                "Lecture pace perfect tha, sabhi students easily follow kar pa rahe the.",
                "Sir speed bohot balanced rakhte hain aur repeat bhi karte hain."
            ],
            "neg": [
                "Lecture pace bohot fast hai, slides itni jaldi change hoti hain ki note nahi kar sakte.",
                "Syllabus complete karne ke chakkar mein bohot tezi se bhagaya."
            ],
            "neu": [
                "Lecture ki speed okay thi, average pacing."
            ]
        },
        "Faculty Support": {
            "pos": [
                "Faculty aur TAs hamesha doubt session mein help karne ke liye ready rehte hain.",
                "Email pe bhi quick reply milta hai jab bhi guidance chahiye ho."
            ],
            "neg": [
                "Faculty queries ka reply nahi karte aur approach karna bohot difficult hai.",
                "TAs doubt clearing mein help nahi karte aur rude behave karte hain."
            ],
            "neu": [
                "Doubt resolution standard timing pe hi available hota hai."
            ]
        },
        "Practical Sessions": {
            "pos": [
                "Lab sessions bohot informative the, hands-on practice badhiya rahi.",
                "Practical coding exercises se actual software building seekha."
            ],
            "neg": [
                "Lab sessions bilkul unorganized the aur mentor support zero tha.",
                "Lab manuals outdated hain aur code errors solve nahi karate."
            ],
            "neu": [
                "Lab sessions standard procedure ke hisab se chale."
            ]
        },
        "Projects": {
            "pos": [
                "Capstone project se portfolio ke liye bohot strong project ban gaya.",
                "Mentor ne architectural review mein bohot valuable tips diye."
            ],
            "neg": [
                "Project submission instructions bohot confusing aur last minute change hoti hain.",
                "Team project evaluation biased tha aur guidance bilkul nahi mili."
            ],
            "neu": [
                "Project submission routine level ka tha."
            ]
        },
        "Study Material": {
            "pos": [
                "Shared notes, code repos aur slides bohot well organized hain.",
                "Exam preparation ke liye reference material best tha."
            ],
            "neg": [
                "Slides mein bohot mistakes hain aur proper reference books recommend nahi ki.",
                "Study material portal pe exam se 2 din pehle upload hota hai."
            ],
            "neu": [
                "Study material basic passing marks ke liye sufficient tha."
            ]
        },
        "Infrastructure": {
            "pos": [
                "Lab PCs bohot fast hain aur GPU clusters smoothly run hote hain.",
                "High speed Wi-Fi aur modern projector facilities available the."
            ],
            "neg": [
                "Lab machines baar baar crash hoti hain aur Wi-Fi speed pathetic hai.",
                "Classroom AC aur projector sound system mostly kharab rehta hai."
            ],
            "neu": [
                "Infrastructure average hai, kaam chal jata hai."
            ]
        },
        "Evaluation": {
            "pos": [
                "Marking scheme bilkul fair aur transparent thi.",
                "Papers evaluate karke feedback diya gaya ki kahan improvement chahiye."
            ],
            "neg": [
                "Checking bohot strict aur unfair thi, bin baat ke marks cut kiye.",
                "Evaluation results aane mein bohot delay hua aur copy rechecking allowed nahi thi."
            ],
            "neu": [
                "Evaluation standard guidelines ke hisab se hua."
            ]
        }
    }
}

CONNECTORS = {
    "English": [
        " However, ", " On the other hand, ", " But ", " Additionally, ",
        " Furthermore, ", " Although ", " At the same time, ", " Moreover, "
    ],
    "Hindi": [
        " लेकिन ", " परन्तु ", " इसके अलावा ", " साथ ही साथ ", " हालांकि ", " वहीं दूसरी ओर "
    ],
    "Hinglish": [
        " but ", " lekin ", " on the other hand ", " aur sath hi sath ", " waise ", " par "
    ]
}

# Semester temporal topic shifts (Topic Drift ground truth)
SEMESTER_TOPIC_FOCUS = {
    "Sem 1": ["Lecture Pace & Fundamentals", "Lab Infrastructure & Wi-Fi", "Introductory Programming Basics"],
    "Sem 2": ["Assignment Workload & Deadlines", "Algorithm Basics & Practice", "Classroom Facilities"],
    "Sem 3": ["Database Labs & SQL Setup", "Midterm Exam Grading Fairness", "Data Structure Complexity"],
    "Sem 4": ["Core System Engineering", "Faculty Support & Doubts", "Exam Difficulty & Time Management"],
    "Sem 5": ["Placement Prep & Coding Rounds", "Advanced Project Guidance", "Cloud Computing & Modern Tools"],
    "Sem 6": ["Capstone Project & Industry Readiness", "Placement Prep & Coding Rounds", "Advanced AI Compute & Infrastructure"]
}

TOPIC_NAMES = [
    "Lecture Pace & Fundamentals",
    "Assignment Workload & Deadlines",
    "Lab Infrastructure & Hardware",
    "Midterm & Final Exam Fairness",
    "Faculty Responsiveness & Support",
    "Practical Coding & Lab Exercises",
    "Capstone Project & Mentorship",
    "Curriculum Relevance & Modern Tools",
    "Study Materials & Resource Access",
    "Placement Prep & Coding Rounds"
]

def generate_record(rec_id, sem, lang, course):
    student_id = f"STU_{random.randint(1000, 9999)}"
    
    # Date in corresponding semester year
    sem_idx = SEMESTERS.index(sem)
    start_date = datetime(2024 + (sem_idx // 2), 1 if (sem_idx % 2 == 0) else 7, 15)
    days_offset = random.randint(0, 110)
    record_date = (start_date + timedelta(days=days_offset)).strftime("%Y-%m-%d")
    
    # Decide number of aspects in this feedback (1 to 3 aspects)
    num_aspects = random.choices([1, 2, 3], weights=[0.25, 0.55, 0.20])[0]
    
    # Pick aspects
    selected_aspects = random.sample(ASPECTS, num_aspects)
    
    # Decide primary sentiment bias
    sentiment_bias = random.choices(["pos", "neg", "neu"], weights=[0.45, 0.35, 0.20])[0]
    
    aspect_records = []
    text_snippets = []
    
    for i, asp in enumerate(selected_aspects):
        # In compound feedback, second aspect can have contrasting sentiment
        if i == 0:
            asp_sent = sentiment_bias
        elif i == 1 and random.random() < 0.65:
            # Contrast sentiment for realistic "Prof is good but assignments are bad"
            asp_sent = "neg" if sentiment_bias == "pos" else "pos"
        else:
            asp_sent = random.choices(["pos", "neg", "neu"], weights=[0.4, 0.4, 0.2])[0]
        
        pool = TEMPLATES[lang][asp][asp_sent]
        snippet = random.choice(pool)
        conf = round(random.uniform(0.82, 0.98), 2)
        
        sent_label = "Positive" if asp_sent == "pos" else ("Negative" if asp_sent == "neg" else "Neutral")
        aspect_records.append({
            "aspect": asp,
            "sentiment": sent_label,
            "confidence": conf,
            "snippet": snippet
        })
        text_snippets.append(snippet)
    
    # Combine text snippets using language appropriate connectors
    if len(text_snippets) == 1:
        full_text = text_snippets[0]
    elif len(text_snippets) == 2:
        conn = random.choice(CONNECTORS[lang])
        full_text = text_snippets[0] + conn + text_snippets[1]
    else:
        conn1 = random.choice(CONNECTORS[lang])
        conn2 = random.choice(CONNECTORS[lang])
        full_text = text_snippets[0] + conn1 + text_snippets[1] + conn2 + text_snippets[2]
    
    # Overall sentiment computation
    pos_count = sum(1 for a in aspect_records if a["sentiment"] == "Positive")
    neg_count = sum(1 for a in aspect_records if a["sentiment"] == "Negative")
    
    if pos_count > neg_count:
        overall_sentiment = "Positive"
        rating = random.choices([4, 5], weights=[0.4, 0.6])[0]
    elif neg_count > pos_count:
        overall_sentiment = "Negative"
        rating = random.choices([1, 2], weights=[0.6, 0.4])[0]
    else:
        overall_sentiment = "Neutral"
        rating = 3
    
    overall_conf = round(random.uniform(0.84, 0.99), 2)
    
    # Assign topic based on semester focus and aspect
    sem_focus = SEMESTER_TOPIC_FOCUS[sem]
    if random.random() < 0.60:
        primary_topic = random.choice(sem_focus)
    else:
        primary_topic = random.choice(TOPIC_NAMES)
    
    topic_id = TOPIC_NAMES.index(primary_topic) if primary_topic in TOPIC_NAMES else 0
    topic_prob = round(random.uniform(0.70, 0.96), 2)
    
    return {
        "Feedback_ID": f"FB_{rec_id:05d}",
        "Student_ID": student_id,
        "Course_ID": course["code"],
        "Course_Name": course["name"],
        "Semester": sem,
        "Date": record_date,
        "Language": lang,
        "Rating": rating,
        "Feedback_Text": full_text,
        "Overall_Sentiment": overall_sentiment,
        "Sentiment_Confidence": overall_conf,
        "Aspect_Records": json.dumps(aspect_records, ensure_ascii=False),
        "Topic_ID": topic_id,
        "Topic_Name": primary_topic,
        "Topic_Probability": topic_prob
    }

def generate_dataset(num_records=2200, output_path="data/raw/course_feedback_raw.csv"):
    random.seed(42)
    np.random.seed(42)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    records = []
    # Language distribution: 50% English, 25% Hindi, 25% Hinglish
    lang_choices = ["English", "Hindi", "Hinglish"]
    lang_weights = [0.50, 0.25, 0.25]
    
    for i in range(1, num_records + 1):
        sem = random.choice(SEMESTERS)
        lang = random.choices(lang_choices, weights=lang_weights)[0]
        course = random.choice(COURSES)
        rec = generate_record(i, sem, lang, course)
        records.append(rec)
    
    df = pd.DataFrame(records)
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Generated {len(df)} feedback records saved to {output_path}")
    print(f"Languages: {df['Language'].value_counts().to_dict()}")
    print(f"Semesters: {df['Semester'].value_counts().to_dict()}")
    print(f"Overall Sentiments: {df['Overall_Sentiment'].value_counts().to_dict()}")
    return df

if __name__ == "__main__":
    generate_dataset()
