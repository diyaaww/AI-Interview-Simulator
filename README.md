# AI Interview Simulator 🤖

An AI-powered interview preparation platform built using Python and Streamlit. It helps users practice technical and general interviews through AI-generated questions, voice interaction, webcam-based attention monitoring, and automated feedback.

## ✨ Features

- **AI-Generated Interview Questions:** Generates interview questions based on the selected role and interview settings.
- **Voice Interaction:** Supports spoken questions and voice-based answers.
- **Webcam Monitoring:** Uses computer vision to detect face position and display an attention indicator.
- **AI Feedback:** Evaluates interview responses and provides feedback to help improve performance.
- **AI Assistant:** Provides additional interview-related guidance.
- **User Authentication:** Includes login and signup functionality.

## 🛠️ Technologies Used

- Python
- Streamlit
- Ollama
- Qwen 2.5 (3B)
- OpenCV
- NumPy
- Streamlit WebRTC
- SpeechRecognition
- pyttsx3
- SQLite / CSV-based data handling (as implemented)

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/diyaaww/AI-Interview-Simulator.git
cd AI-Interview-Simulator
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama

Download Ollama from:

https://ollama.com/

Pull the required AI model:

```bash
ollama pull qwen2.5:3b
```

Make sure Ollama is running before launching the application.

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🧠 AI Model

This project uses **Qwen 2.5 (3B)** through Ollama for local AI-powered interview question generation and response evaluation.

## 🎯 Project Objective

The objective of this project is to make interview preparation more interactive and accessible by combining artificial intelligence, speech recognition, text-to-speech, and computer vision.

## 👩‍💻 Developer

**Diya**  
Diploma in Computer Science Engineering  
Thapar Polytechnic College, Patiala

---

*Developed as an AI-based student project.*