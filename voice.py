
"""
AI Interview Simulator - Voice Assistant

Uses offline Windows TTS through pyttsx3.
No internet connection or Edge TTS required.
"""

import threading
import pyttsx3

VOICE_RATE = 175

# Prevent overlapping speech calls.
_voice_lock = threading.RLock()


def speak(text):
    """Speak text using the offline Windows voice."""

    if not text:
        return

    with _voice_lock:
        engine = None

        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", VOICE_RATE)
            engine.say(str(text))
            engine.runAndWait()

        except Exception as error:
            # Voice errors must not crash the interview.
            print(f"Voice output failed: {error}")
            print("Continuing the interview without audio.")

        finally:
            if engine is not None:
                try:
                    engine.stop()
                except Exception:
                    pass


def welcome(role):
    speak(
        f"Hello and welcome to the AI Interview Simulator. "
        f"Today I will interview you for the position of {role}. "
        f"Please answer each question honestly and clearly. "
        f"Relax and treat this as a real interview. "
        f"Let's begin."
    )


def ask_question(question):
    speak(question)


def encourage():
    speak("Take your time. Whenever you are ready, continue.")


def follow_up():
    speak("Could you explain your answer in a little more detail?")


def answer_too_short():
    speak(
        "Your answer seems a little short. "
        "Could you provide more details?"
    )


def interview_finished():
    speak(
        "Congratulations. You have completed the interview. "
        "I am now preparing your performance report."
    )


def goodbye():
    speak(
        "Thank you for using the AI Interview Simulator. "
        "Best of luck with your future interviews."
    )
