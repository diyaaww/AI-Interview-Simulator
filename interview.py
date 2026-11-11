"""
====================================================
AI Interview Simulator
Interview Engine
====================================================
"""

from voice import ask_question
from speech import listen
from gemini import evaluate_answer


class InterviewEngine:

    def __init__(self, questions):

        self.questions = questions
        self.current_question = 0
        self.results = []

    def has_next_question(self):

        return self.current_question < len(self.questions)

    def get_current_question(self):

        return self.questions[self.current_question]

    def ask(self):

        question = self.get_current_question()

        ask_question(question)

        return question

    def listen_answer(self):

        return listen()

    def evaluate(self, answer):

        question = self.get_current_question()

        result = evaluate_answer(
            question,
            answer["text"]
        )

        self.results.append({

            "question": question,

            "answer": answer,

            "evaluation": result

        })

        self.current_question += 1

        return result

    def interview_complete(self):

        return self.current_question >= len(self.questions)