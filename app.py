from voice import welcome, ask_question
from camera import (
    show_camera,
    get_attention_score,
    get_status
)
from state import interview_state
from gemini import (
    generate_questions,
    evaluate_interview,
    interview_advisor
)
from speech import listen


from login import login_page
from signup import signup_page

import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Interview Simulator",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:

    if st.session_state.logged_in:
        st.session_state.page = "home"
    else:
        st.session_state.page = "login"

# ============================================================
# DARK THEME
# ============================================================

st.markdown("""
<style>

/* ===============================
   IMPORT FONT
================================*/

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ===============================
   ROOT COLORS
================================*/

:root{

    --bg:#050814;
    --panel:#0A1020;
    --panel2:#0E1529;

    --border:rgba(95,145,255,.18);
    --border-hover:rgba(95,145,255,.45);

    --primary:#5B8CFF;
    --secondary:#7C6CFF;

    --text:#F8FAFC;
    --muted:#94A3B8;

}

/* ===============================
   GLOBAL
================================*/

*{

    font-family:'Inter',sans-serif;

    box-sizing:border-box;

}

#MainMenu{

    visibility:hidden;

}

header{

    visibility:hidden;

}

footer{

    visibility:hidden;

}

section.main{

    padding-top:1rem;

}

.block-container{

    max-width:1450px;

    padding-top:1.5rem;

    padding-bottom:2rem;

}

/* ===============================
   BACKGROUND
================================*/

.stApp{

    background:

    radial-gradient(
        circle at 0% 0%,
        rgba(91,140,255,.10),
        transparent 28%
    ),

    radial-gradient(
        circle at 100% 0%,
        rgba(91,140,255,.08),
        transparent 25%
    ),

    radial-gradient(
        circle at 50% 100%,
        rgba(124,108,255,.06),
        transparent 35%
    ),

    linear-gradient(
        180deg,
        #050814,
        #070C18,
        #08101D
    );

    color:var(--text);

}

/* ===============================
   TYPOGRAPHY
================================*/

h1{

    font-size:56px !important;

    font-weight:800 !important;

    letter-spacing:1px;

    color:var(--text) !important;

    margin-bottom:.25rem !important;

}

h2{

    font-size:34px !important;

    font-weight:700 !important;

    color:var(--text) !important;

}

h3{

    font-size:28px !important;

    font-weight:700 !important;

    color:var(--text) !important;

}

h4,h5,h6{

    color:var(--text) !important;

    font-weight:600;

}

label{

    color:#CBD5E1 !important;

    font-weight:600;

    letter-spacing:.4px;

}

p{

    color:var(--muted);

    line-height:1.7;

    font-size:16px;

}

small{

    color:#7F8DAA;

}

/* ===============================
   HORIZONTAL LINE
================================*/

hr{

    border:none;

    height:1px;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(91,140,255,.25),
            transparent
        );

    margin:18px 0 28px 0;

}

/* ===============================
   STREAMLIT CONTAINERS
================================*/

div[data-testid="stVerticalBlockBorderWrapper"]{

    position:relative;

    border-radius:24px;

    padding:22px;

    background:
        linear-gradient(
            180deg,
            #0B1222,
            #09101D
        );

    border:1px solid rgba(70,130,255,.18);

    box-shadow:
        0 10px 35px rgba(0,0,0,.45);

    transition:all .3s ease;

}

/* LEFT CYBER BAR */

div[data-testid="stVerticalBlockBorderWrapper"]::before{

    content:"";

    position:absolute;

    left:0;

    top:26px;

    width:3px;

    height:70%;

    border-radius:30px;

    background:
        linear-gradient(
            180deg,
            #38BDF8,
            #2563EB,
            transparent
        );

    box-shadow:
        0 0 12px #38BDF8,
        0 0 24px rgba(56,189,248,.5);

}

/* HOVER */

div[data-testid="stVerticalBlockBorderWrapper"]:hover{

    transform:translateY(-3px);

    border-color:#3B82F6;

    box-shadow:
        0 0 25px rgba(59,130,246,.20),
        0 18px 45px rgba(0,0,0,.50);

}

/* ===============================
   TEXT INPUT
================================*/

.stTextInput input{

    background:rgba(15,22,40,.92);

    color:white;

    border:1px solid rgba(91,140,255,.18);

    border-radius:16px;

    padding:14px 18px;

    transition:.25s;

}

.stTextInput input:hover{

    border-color:
    rgba(91,140,255,.35);

}

.stTextInput input:focus{

    border-color:#5B8CFF;

    box-shadow:
        0 0 18px rgba(91,140,255,.20);

}

/* ===============================
   SELECTBOX
================================*/

div[data-baseweb="select"]{

    background:rgba(15,22,40,.92);

    border-radius:16px;

    border:1px solid rgba(91,140,255,.18);

    transition:.25s;

}

div[data-baseweb="select"]:hover{

    border-color:
    rgba(91,140,255,.35);

}

/* ===============================
   FILE UPLOADER
================================*/

div[data-testid="stFileUploader"]{

    background:
        linear-gradient(
            180deg,
            rgba(12,19,36,.90),
            rgba(9,14,28,.96)
        );

    border:1.5px dashed rgba(91,140,255,.30);

    border-radius:20px;

    padding:22px;

    transition:.25s;

}

div[data-testid="stFileUploader"]:hover{

    border-color:#5B8CFF;

    box-shadow:
        0 0 24px rgba(91,140,255,.18);

}

/* ===============================
   BUTTON
================================*/

.stButton > button{

    width:100%;
    height:58px;

    border:none;
    border-radius:18px;

    background:
        linear-gradient(
            135deg,
            #2563EB,
            #4F46E5,
            #6366F1
        );

    color:white;

    font-size:17px;
    font-weight:700;
    letter-spacing:1px;

    cursor:pointer;

    transition:
        all .25s ease;

    box-shadow:
        0 8px 25px rgba(37,99,235,.28),
        0 0 20px rgba(79,70,229,.18);

}

.stButton > button:hover{

    transform:
        translateY(-3px);

    background:
        linear-gradient(
            135deg,
            #3B82F6,
            #5B6DFF,
            #6D5DF6
        );

    box-shadow:
        0 14px 35px rgba(37,99,235,.40),
        0 0 28px rgba(91,140,255,.28);

}

.stButton > button:active{

    transform:scale(.98);

}

/* ===============================
   SLIDER
================================*/

.stSlider{

    padding-top:12px;

}

/* Slider Track */

.stSlider [data-baseweb="slider"]{

    padding-top:10px;

}

/* Active Track */

.stSlider [role="slider"]{

    width:20px !important;

    height:20px !important;

    border-radius:50% !important;

    background:#5B8CFF !important;

    border:3px solid #EAF2FF !important;

    box-shadow:
        0 0 8px rgba(91,140,255,.55),
        0 0 18px rgba(91,140,255,.45),
        0 0 35px rgba(91,140,255,.30);

    transition:all .25s ease;

}

/* Hover */

.stSlider [role="slider"]:hover{

    transform:scale(1.15);

    box-shadow:
        0 0 12px rgba(91,140,255,.70),
        0 0 28px rgba(91,140,255,.55),
        0 0 45px rgba(91,140,255,.40);

}

/* ===============================
   EXPANDERS
================================*/

details{

    background:
    rgba(15,23,42,.68);

    border-radius:18px;

    border:1px solid
    rgba(91,140,255,.18);

    overflow:hidden;

}

summary{

    padding:15px;

    color:white;

    font-weight:600;

}

/* ===============================
   CHAT
================================*/

div[data-testid="stChatMessage"]{

    background:
    rgba(15,23,42,.65);

    border-radius:18px;

    border:1px solid
    rgba(91,140,255,.14);

    padding:12px;

    margin-bottom:10px;

}

/* ===============================
   PROGRESS BAR
================================*/

div[data-testid="stProgressBar"] div{

    border-radius:100px;

}

/* ===============================
   SUCCESS
================================*/

div[data-testid="stAlert"]{

    border-radius:16px;

}

/* ===============================
   METRICS
================================*/

div[data-testid="metric-container"]{

    background:
    rgba(15,23,42,.72);

    border-radius:18px;

    border:1px solid
    rgba(91,140,255,.18);

    padding:15px;

}

/* ===============================
   CONTAINERS
================================*/

div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stTextInput"]),
div[data-testid="stVerticalBlock"] > div:has(> div[data-baseweb="select"]),
div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stFileUploader"]),
div[data-testid="stVerticalBlock"] > div:has(.stSlider),
div[data-testid="stVerticalBlock"] > div:has(.stButton){

    background:
        linear-gradient(
            180deg,
            rgba(10,16,30,.94),
            rgba(8,12,22,.98)
        );

    border:1px solid rgba(91,140,255,.14);

    border-radius:22px;

    padding:20px;

    transition:.25s ease;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,.02),
        0 0 0 1px rgba(91,140,255,.05),
        0 8px 18px rgba(0,0,0,.30);

}

div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stTextInput"]):hover,
div[data-testid="stVerticalBlock"] > div:has(> div[data-baseweb="select"]):hover,
div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stFileUploader"]):hover,
div[data-testid="stVerticalBlock"] > div:has(.stSlider):hover,
div[data-testid="stVerticalBlock"] > div:has(.stButton):hover{

    border-color:rgba(91,140,255,.35);

    box-shadow:
        0 0 10px rgba(91,140,255,.12),
        0 0 20px rgba(91,140,255,.08),
        0 12px 28px rgba(0,0,0,.35);

}

/* ===============================
   SCROLLBAR
================================*/

::-webkit-scrollbar{

    width:10px;

}

::-webkit-scrollbar-thumb{

    background:#3B82F6;

    border-radius:20px;

}

::-webkit-scrollbar-track{

    background:#070B16;

}

</style>
""", unsafe_allow_html=True)

# ============================================================
# LOGIN PAGE
# ============================================================

if st.session_state.page == "login":

    login_page()

# ============================================================
# SIGNUP PAGE
# ============================================================

elif st.session_state.page == "signup":

    signup_page()

# ============================================================
# HOME PAGE
# ============================================================

elif st.session_state.page == "home":

    # --------------------------------------------------------
    # Hero
    # --------------------------------------------------------

    st.title("AI INTERVIEW SIMULATOR")
    st.divider()

    # --------------------------------------------------------
    # Layout
    # --------------------------------------------------------

    left, right = st.columns(
        [7, 3],
        gap="large"
    )

    # ======================================================
    # LEFT PANEL
    # ======================================================

    with left:

        # -------------------------------
        # Interview Role
        # -------------------------------

        st.markdown("""
        <div class="section-title">
            <span class="section-icon">💼</span>
            <span>INTERVIEW ROLE</span>
        </div>
        """, unsafe_allow_html=True)

        with st.container():

            interview_role = st.text_input(
                "",
                placeholder="Python Developer, Data Analyst, Primary School Teacher..."
            )

        st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)

        # -------------------------------
        # Experience + Difficulty
        # -------------------------------

        col1, col2 = st.columns(2, gap="large")

        with col1:

            st.markdown("""
            <div class="section-title small">
                <span class="section-icon">👤</span>
                <span>EXPERIENCE</span>
            </div>
            """, unsafe_allow_html=True)

            with st.container():

                experience = st.selectbox(
                    "",
                    [
                        "Fresher",
                        "0 - 1 Years",
                        "1 - 3 Years",
                        "3 - 5 Years",
                        "5+ Years"
                    ]
                )

        with col2:

            st.markdown("""
            <div class="section-title small">
                <span class="section-icon">📊</span>
                <span>DIFFICULTY</span>
            </div>
            """, unsafe_allow_html=True)

            with st.container():

                difficulty = st.selectbox(
                    "",
                    [
                        "Easy",
                        "Medium",
                        "Hard"
                    ]
                )

        st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)

        # -------------------------------
        # Questions
        # -------------------------------

        st.markdown("""
        <div class="section-title">
            <span class="section-icon">❓</span>
            <span>NUMBER OF QUESTIONS</span>
        </div>
        """, unsafe_allow_html=True)

        with st.container():

            questions = st.slider(
                "",
                min_value=5,
                max_value=15,
                value=10
            )

    # ======================================================
    # RIGHT PANEL
    # ======================================================

    with right:

        with st.container():

            st.markdown("### Resume (Optional)")

            resume = st.file_uploader(
                "",
                type=["pdf", "docx"]
            )

            st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

            start = st.button(
                "🚀 START INTERVIEW",
                use_container_width=True
            )

    # ======================================================
    # START BUTTON
    # ======================================================

    if start:

        if interview_role.strip() == "":

            st.warning(
                "Please enter the interview role."
            )

        else:

            keys_to_clear = [
                "questions",
                "answers",
                "current_question",
                "current_answer",
                "answer_recorded",
                "last_spoken_question",
                "final_report",
                "advisor_messages",
                "interview_started"
            ]

            for key in keys_to_clear:

                if key in st.session_state:
                    del st.session_state[key]

            st.session_state.role = interview_role
            st.session_state.experience = experience
            st.session_state.difficulty = difficulty
            st.session_state.question_count = questions
            st.session_state.resume = resume

            st.session_state.page = "loading"

            st.rerun()

# ============================================================
# LOADING PAGE
# ============================================================

elif st.session_state.page == "loading":

    import time

    st.title("🤖 Preparing Your Interview")

    progress = st.progress(0)

    status = st.empty()

    loading_steps = [

        "🤖 Initializing AI Interviewer...",
        "🧠 Generating Interview Questions...",
        "🎤 Loading Speech Recognition...",
        "📊 Preparing Evaluation Engine...",
        "✅ Finalizing Interview Setup..."

    ]

    for i, step in enumerate(loading_steps):

        status.info(step)

        progress.progress((i + 1) / len(loading_steps))

        time.sleep(0.8)

    st.success("✅ Everything is Ready!")

    time.sleep(1)

    countdown = st.empty()

    for i in [3, 2, 1]:

        countdown.markdown(
            f"""
            <h1 style='text-align:center;
                       color:#A78BFA;
                       font-size:90px;'>
                {i}
            </h1>
            """,
            unsafe_allow_html=True
        )

        time.sleep(1)

    countdown.empty()

    st.session_state.interview_started = True

    st.session_state.page = "interview"

    welcome(st.session_state.role)

    st.rerun()

# ============================================================
# INTERVIEW PAGE
# ============================================================

elif st.session_state.page == "interview":

    import time

    st.title("🎤 AI Interview Simulator")
    st.divider()

# ========================================================
# Generate Questions (Only Once)
# ========================================================

    if "questions" not in st.session_state:

        with st.spinner("🤖 Generating Interview Questions..."):

            try:

                st.session_state.questions = generate_questions(
                    st.session_state.role,
                    st.session_state.experience,
                    st.session_state.difficulty,
                    st.session_state.question_count
                )

            except Exception as e:

                st.warning(
                    f"AI question generation failed.\n\nUsing default questions.\n\n{e}"
                )

                st.session_state.questions = [
                    "Tell me about yourself.",
                    "Why do you want this job?",
                    "What are your strengths?",
                    "What are your weaknesses?",
                    "Explain Object-Oriented Programming.",
                    "What is Python?",
                    "What is Machine Learning?",
                    "What is Deep Learning?",
                    "Tell me about one project you have worked on.",
                    "Where do you see yourself in five years?"
                ]

        st.session_state.current_question = 0
        st.session_state.answers = []
        st.session_state.interview_started = True
        st.session_state.last_spoken_question = -1
        st.session_state.answer_recorded = False
        st.session_state.current_answer = None

    # Safety check (prevents missing session keys after reruns)

    if "current_answer" not in st.session_state:
        st.session_state.current_answer = None

    if "answer_recorded" not in st.session_state:
        st.session_state.answer_recorded = False

    if "answers" not in st.session_state:
        st.session_state.answers = []

# ========================================================
# Interview Finished
# ========================================================

    if st.session_state.current_question >= len(st.session_state.questions):

        st.markdown("""
        <div style="
            background:linear-gradient(90deg,#30479d,#7b3fe4,#e72c83);
            padding:30px;
            border-radius:20px;
            text-align:center;
            margin-bottom:30px;
        ">
            <h1 style="
                color:white;
                margin:0;
                font-size:42px;
                font-weight:bold;
            ">
                🎉 Interview Completed
            </h1>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("📋 Questions & Your Answers")

        for i, ans in enumerate(st.session_state.answers, start=1):

            with st.expander(f"Question {i}"):

                st.markdown("#### ❓ Question")
                st.write(ans["question"])

                st.markdown("#### 💬 Your Answer")
                st.write(ans["text"])

        st.divider()

        st.subheader("🤖 AI Interview Report")

        with st.spinner("🧠 Preparing your professional interview report..."):

            if "final_report" not in st.session_state:

                st.session_state.final_report = evaluate_interview(
                    st.session_state.answers,
                    get_attention_score(),
                    get_status()
                )

            final_report = st.session_state.final_report

        st.success("✅ Report Generated")

        headings = [
            "Overall Impression",
            "Technical Assessment",
            "Communication Skills",
            "Behavioral Assessment",
            "Body Language",
            "Key Strengths",
            "Areas for Improvement",
            "Final Verdict"
        ]

        icons = {
            "Overall Impression": "🌟",
            "Technical Assessment": "💻",
            "Communication Skills": "💬",
            "Behavioral Assessment": "🧠",
            "Body Language": "🧍",
            "Key Strengths": "✅",
            "Areas for Improvement": "📈",
            "Final Verdict": "🏆"
        }

        sections = {}
        current = None

        for line in final_report.splitlines():

            line = line.strip()

            if not line:
                continue

            clean_line = (
                line.replace("*", "")
                    .replace("#", "")
                    .strip()
            )

            matched = False

            for heading in headings:

                if clean_line.startswith(heading):

                    current = heading
                    sections[current] = ""

                    content = clean_line[len(heading):].lstrip(":").strip()

                    if content:
                        sections[current] += content + "\n"

                    matched = True
                    break

            if matched:
                continue

            if current:
                sections[current] += line + "\n"

        for heading in headings:

            if heading not in sections:
                continue

            with st.container():

                st.markdown(f"### {icons[heading]} {heading}")
                st.write(sections[heading].strip())

        # ========================================================
        # Interview Advisor
        # ========================================================

        st.divider()

        st.subheader("💬 Interview Advisor")

        st.caption(
            "Ask follow-up questions about your interview, "
            "performance, communication, body language, or ways to improve."
        )

        if "advisor_messages" not in st.session_state:
            st.session_state.advisor_messages = []

        for message in st.session_state.advisor_messages:

            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        prompt = st.chat_input(
            "Ask anything about your interview..."
        )

        if prompt:

            st.session_state.advisor_messages.append(
                {
                    "role": "user",
                    "content": prompt
                }
            )

            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):

                with st.spinner("Thinking..."):

                    reply = interview_advisor(
                        role=st.session_state.role,
                        interview_data=st.session_state.answers,
                        attention=get_attention_score(),
                        status=get_status(),
                        report=st.session_state.final_report,
                        chat_history=st.session_state.advisor_messages,
                        user_question=prompt
                    )

                    st.markdown(reply)

            st.session_state.advisor_messages.append(
                {
                    "role": "assistant",
                    "content": reply
                }
            )

            st.rerun()

        st.stop()

# ========================================================
# Current Question
# ========================================================

    question = st.session_state.questions[
        st.session_state.current_question
    ]

    st.markdown(
        f"""<h3 style='text-align:center;color:#C084FC;'>
Question {st.session_state.current_question + 1}
/ {len(st.session_state.questions)}
</h3>""",
        unsafe_allow_html=True
    )

    st.progress(
        (st.session_state.current_question + 1)
        / len(st.session_state.questions)
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="
            background:#111827;
            border-left:6px solid #A855F7;
            padding:18px;
            border-radius:15px;
            margin-bottom:20px;
        ">
            <h3 style="color:white;">❓ Interview Question</h3>
            <p style="font-size:22px;color:#E5E7EB;">
                {question}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # Candidate Camera
    # ========================================================

    st.markdown(
        "<h3 style='text-align:center;'>📷 Candidate Camera</h3>",
        unsafe_allow_html=True
    )

    show_camera()

    st.markdown("<br>", unsafe_allow_html=True)

    # ========================================================
    # End Interview Button
    # ========================================================

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        if st.button(
            "🟥 End Interview",
            use_container_width=True,
            type="primary"
        ):

            st.session_state.current_question = len(
                st.session_state.questions
            )

            st.rerun()

    # ========================================================
    # Speak Question Only Once
    # ========================================================

    if (
        st.session_state.last_spoken_question
        != st.session_state.current_question
    ):

        ask_question(question)

        st.session_state.last_spoken_question = (
            st.session_state.current_question
        )

     # ========================================================
    # Listen to Candidate
    # ========================================================

    if not st.session_state.answer_recorded:

        with st.spinner("🎤 Listening... Please answer the question..."):

            answer = listen()

        st.session_state.current_answer = answer
        st.session_state.answer_recorded = True

        st.success("✅ Answer Recorded")

      

        st.session_state.answers.append({

            "question": question,
            "answer": answer["text"],
            "text": answer["text"],
            "speech": answer

        })

        if (
            st.session_state.current_question
            < len(st.session_state.questions) - 1
        ):

            st.session_state.current_question += 1
            st.session_state.answer_recorded = False
            st.session_state.current_answer = None

            time.sleep(1)

            st.rerun()

        else:

            st.session_state.current_question += 1

            st.rerun()

    # ========================================================
    # Show Candidate Answer
    # ========================================================

#     st.chat_message("user").write(answer["text"])

#     # ========================================================
#     # AI Evaluation
#     # ========================================================

#     with st.spinner("🧠 Evaluating your answer..."):

#         evaluation = """
# Overall: Good answer.

# Strengths:
# • Answered the question clearly.
# • Maintained a reasonable response length.
# • Demonstrated basic understanding.

# Suggestions:
# • Add more technical details where possible.
# • Give real-life examples.
# • Speak confidently and avoid filler words.

# Rating: 8/10
# """

#     # ========================================================
#     # Speech Analysis
#     # ========================================================

#     st.subheader("📊 Speech Analysis")

#     col1, col2 = st.columns(2)

#     with col1:
#         st.metric("📝 Words", answer["word_count"])
#         st.metric("⏱ Duration", f"{answer['duration']} sec")

#     with col2:
#         st.metric("⚡ WPM", answer["words_per_minute"])
#         st.metric("🗣 Fillers", answer["filler_words"])

#     # ========================================================
#     # AI Interview Evaluation
#     # ========================================================

#     st.subheader("🤖 AI Interview Evaluation")
#     st.info(evaluation)

#     # ========================================================
#     # Save Complete Result
#     # ========================================================

#     st.session_state.answers.append({
#         "question": question,
#         "text": answer["text"],
#         "speech": answer,
#         "evaluation": evaluation
#     })

#     # ========================================================
#     # Next Question
#     # ========================================================

#     st.success("✅ Answer Recorded")

#     time.sleep(2)

#     st.session_state.current_question += 1

#     st.rerun()