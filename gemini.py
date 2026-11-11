"""
====================================================
AI Interview Simulator
Optimized Local AI Module (Ollama)
Version 2
====================================================
"""

import json
import time
import ollama


# ====================================================
# Ollama Configuration
# ====================================================

MODEL_NAME = "qwen2.5:3b"


# ====================================================
# Safe Ollama Request
# ====================================================

def generate(
    prompt,
    task="general"
):

    """
    Sends a prompt to Ollama.
    Optimized for different AI tasks.
    """

    system_prompt = """
You are an experienced HR interviewer.

Follow instructions exactly.

Be concise.

Never explain your reasoning.

If JSON is requested,
return ONLY valid JSON.

If questions are requested,
return ONLY the questions.

If report text is requested,
write professional HR-style paragraphs.
"""

    # ------------------------------------------------
    # Task-specific generation settings
    # ------------------------------------------------

    settings = {

        "questions": {
            "temperature": 0.2,
            "num_predict": 350,
            "num_ctx": 2048
        },

        "json": {
            "temperature": 0.0,
            "num_predict": 220,
            "num_ctx": 2048
        },

        "report": {
            "temperature": 0.1,
            "num_predict": 700,
            "num_ctx": 2048
        },

        "advisor": {
            "temperature": 0.3,
            "num_predict": 350,
            "num_ctx": 2048
        },

        "general": {
            "temperature": 0.1,
            "num_predict": 500,
            "num_ctx": 2048
        }

    }

    options = settings.get(task, settings["general"])

    for attempt in range(3):

        try:

            response = ollama.chat(

                model=MODEL_NAME,

                messages=[

                    {
                        "role": "system",
                        "content": system_prompt
                    },

                    {
                        "role": "user",
                        "content": prompt
                    }

                ],

                options=options,

                keep_alive="15m"

            )

            return response.message.content.strip()

        except Exception as e:

            print(f"Ollama Error ({attempt + 1}/3): {e}")

            if attempt == 2:
                raise

            time.sleep(1)


# ====================================================
# Generate Interview Questions
# ====================================================

def generate_questions(role, experience, difficulty, num_questions):

    prompt = f"""
Generate exactly {num_questions} interview questions.

Role:
{role}

Experience:
{experience}

Difficulty:
{difficulty}

Rules

One question per line.

No numbering.

No headings.

No explanations.

Do not repeat questions.

Mix HR, technical and scenario-based questions.

Output only the questions.
"""

    response = generate(prompt, "questions")

    questions = []

    for line in response.splitlines():

        q = line.strip()

        if not q:
            continue

        if len(q) < 8:
            continue

        while q and (
            q[0].isdigit()
            or q[0] in ".-) "
        ):
            q = q[1:].strip()

        if q and q not in questions:
            questions.append(q)

    fallback = [

        f"Tell me about yourself and why you are interested in becoming a {role}.",

        f"What skills are most important for a {role}?",

        f"Describe a challenge you may face as a {role}.",

        "Tell me about one project you are proud of.",

        "How do you handle pressure?",

        "Describe a difficult situation and how you solved it.",

        "What are your strengths?",

        "What is one weakness you are working on?",

        "Why should we hire you?",

        "Where do you see yourself in five years?"

    ]

    i = 0

    while len(questions) < num_questions:

        if i >= len(fallback):
            break

        if fallback[i] not in questions:
            questions.append(fallback[i])

        i += 1

    return questions[:num_questions]


# ====================================================
# Evaluate Candidate Answer
# ====================================================

def evaluate_answer(question, answer):

    prompt = f"""
Evaluate this interview answer.

Question:
{question}

Answer:
{answer}

Return ONLY valid JSON.

{{
"technical":8,
"communication":8,
"grammar":8,
"confidence":8,
"professionalism":8,
"strengths":["..."],
"weaknesses":["..."],
"feedback":"..."
}}
"""

    response = generate(prompt, "json")

    try:

        response = (
            response
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(response)

    except Exception:

        return {

            "technical": 0,

            "communication": 0,

            "grammar": 0,

            "confidence": 0,

            "professionalism": 0,

            "strengths": [],

            "weaknesses": [],

            "feedback": response

        }


# ====================================================
# Generate Final Report
# ====================================================

def generate_final_report(results):

    prompt = f"""
You are an experienced HR interviewer.

Write a professional interview report.

Interview Data:

{results}

Rules

Write naturally.

Do not use bullet points.

Do not use markdown.

Do not use scores.

Keep the report concise.

Sections:

Interview Summary

Answer Evaluation

Speech Analysis

Camera Analysis

Overall Assessment

Recommendation
"""

    return generate(prompt)


# ====================================================
# Evaluate Complete Interview
# ====================================================

def evaluate_interview(interview_data,
                       attention=None,
                       status=None):

    formatted_interview = ""

    total_words = 0
    total_duration = 0
    total_wpm = 0
    total_fillers = 0

    count = len(interview_data)

    for i, item in enumerate(interview_data, start=1):

        speech = item.get("speech", {})

        total_words += speech.get("word_count", 0)
        total_duration += speech.get("duration", 0)
        total_wpm += speech.get("words_per_minute", 0)
        total_fillers += speech.get("filler_words", 0)

        formatted_interview += f"""

Question {i}

Question:
{item['question']}

Candidate Answer:
{item['answer']}
"""

    if count == 0:
        count = 1

    avg_words = int(total_words / count)
    avg_duration = round(total_duration / count, 1)
    avg_wpm = int(total_wpm / count)

    prompt = f"""
You are a Senior HR Manager.

Evaluate the following interview.

Interview Responses

{formatted_interview}

Speech Information

Average words per answer: {avg_words}
Average speaking duration: {avg_duration} seconds
Average speaking speed: {avg_wpm} WPM
Total filler words: {total_fillers}

Body Language

Attention: {attention}
Status: {status}

Rules

Professional HR language.

Do NOT use markdown.

Do NOT use scores.

Do NOT use ratings.

Do NOT mention percentages.

Do NOT mention WPM.

Do NOT mention filler counts.

Do NOT mention attention numbers.

Use ONLY these headings.

AI INTERVIEW REPORT

Overall Impression

Technical Assessment

Communication Skills

Behavioral Assessment

Body Language

Key Strengths

Areas for Improvement

Final Verdict

Overall Impression
Write exactly 3 short sentences.

Technical Assessment
Write exactly 3 short sentences.

Communication Skills
Write exactly 3 short sentences.

Behavioral Assessment
Write exactly 3 short sentences.

Body Language
Write exactly 2 short sentences.

Key Strengths
Exactly 3 bullet points starting with "-".

Areas for Improvement
Exactly 3 bullet points starting with "-".

Final Verdict

First line must be exactly one of:

Strongly Recommended
Recommended
Recommended with Training
Needs Further Development

Then write exactly 2 short sentences.
"""

    return generate(prompt, "report")


# ====================================================
# Interview Advisor
# ====================================================

def interview_advisor(
    role,
    interview_data,
    attention,
    status,
    report,
    chat_history,
    user_question
):

    interview_text = ""

    # Keep only the last 5 interview answers
    recent_interview = interview_data[-5:]

    for i, item in enumerate(recent_interview, start=1):

        interview_text += f"""

Question {i}

Question:
{item['question']}

Candidate Answer:
{item['answer']}
"""

    # Keep only the last 6 messages
    conversation = ""

    for message in chat_history[-6:]:

        if message["role"] == "user":
            conversation += f"\nUser: {message['content']}\n"
        else:
            conversation += f"Advisor: {message['content']}\n"

    prompt = f"""
You are the Interview Advisor.

You ONLY answer questions about this interview.

Role:
{role}

Interview:
{interview_text}

Body Language

Attention:
{attention}

Status:
{status}

Report

{report}

Conversation

{conversation}

Question

{user_question}

Rules

Answer only from the interview.

Do not invent information.

If unrelated, politely explain that you only answer interview questions.

Be concise.

Give practical advice.
"""

    return generate(prompt, "advisor")