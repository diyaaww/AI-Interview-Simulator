"""
====================================================
AI Interview Simulator
Speech Recognition Module
====================================================
"""

import speech_recognition as sr
import time


# ====================================================
# Filler Words
# ====================================================

FILLER_WORDS = [
    "um",
    "uh",
    "like",
    "actually",
    "basically",
    "you know",
    "hmm"
]


# ====================================================
# Listen to Candidate
# ====================================================

def listen():

    recognizer = sr.Recognizer()

    # Better interview settings
    recognizer.pause_threshold = 2.0
    recognizer.non_speaking_duration = 0.8
    recognizer.phrase_threshold = 0.3
    recognizer.dynamic_energy_threshold = True

    with sr.Microphone() as source:

        print("Listening...")

        # Faster microphone calibration
        recognizer.adjust_for_ambient_noise(source, duration=0.2)

        start_time = time.time()

        try:

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=90
            )

            end_time = time.time()

            print("Recognizing speech...")

            text = recognizer.recognize_google(audio)

            print("Recognized:", text)

        except sr.WaitTimeoutError:

            end_time = time.time()

            print("ERROR: Wait timeout - No speech detected.")

            text = ""

        except sr.UnknownValueError:

            end_time = time.time()

            print("ERROR: Google could not understand the audio.")

            text = ""

        except sr.RequestError as e:

            end_time = time.time()

            print(f"ERROR: Google Speech API request failed: {e}")

            text = ""

        except Exception as e:

            end_time = time.time()

            print(f"ERROR: {type(e).__name__}: {e}")

            text = ""

    duration = end_time - start_time

    words = text.split()

    word_count = len(words)

    if duration > 0:
        words_per_minute = (word_count / duration) * 60
    else:
        words_per_minute = 0

    filler_count = 0

    for word in words:

        if word.lower() in FILLER_WORDS:
            filler_count += 1

    return {
        "text": text,
        "duration": round(duration, 2),
        "word_count": word_count,
        "words_per_minute": round(words_per_minute, 2),
        "filler_words": filler_count
    }