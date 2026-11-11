"""
====================================================
AI Interview Simulator
Interview Evaluation Module
====================================================
"""

from config import client, MODEL_NAME


# ====================================================
# Evaluate Complete Interview
# ====================================================

def evaluate_interview(interview_data):

    formatted_interview = ""

    for i, item in enumerate(interview_data, start=1):
        formatted_interview += f"""
Question {i}
Question:
{item['question']}

Answer:
{item['answer']}

"""

    prompt = f"""
You are an experienced HR and Technical Interviewer.

Evaluate the complete interview below.

{formatted_interview}

Instructions:

1. Evaluate EACH question separately.

For every question provide:

Question X
Score: x/10

Strengths:
- ...

Weaknesses:
- ...

Suggestions:
- ...

---------------------------------------

After evaluating every question, provide:

Overall Interview Score: x/10

Communication Skills: x/10

Technical Knowledge: x/10

Confidence: x/10

Problem Solving: x/10

Overall Strengths:
- ...
- ...

Overall Weaknesses:
- ...
- ...

Final Recommendation:
(Hire / Consider / Needs Improvement)

Keep the evaluation professional and concise.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text