from streamlit_webrtc import webrtc_streamer
import streamlit as st
import av

from face import detect_faces
from attention import analyze_attention
from state import interview_state


# ============================================================
# Camera Statistics
# ============================================================

focused_frames = 0
total_frames = 0


# ============================================================
# Camera Callback
# ============================================================

def video_frame_callback(frame):
    global focused_frames
    global total_frames

    # Convert WebRTC frame to OpenCV image
    img = frame.to_ndarray(format="bgr24")

    # Face Detection
    img, face = detect_faces(img)

    # Attention Detection
    img, attention = analyze_attention(img, face)

    # Count Frames
    total_frames += 1

    if attention["focused"]:
        focused_frames += 1
        interview_state["status"] = "Focused"
    else:
        interview_state["status"] = "Distracted"

    # Calculate Average Attention
    if total_frames > 0:
        interview_state["attention"] = int(
            (focused_frames / total_frames) * 100
        )

    return av.VideoFrame.from_ndarray(img, format="bgr24")


# ============================================================
# Getters
# ============================================================

def get_attention_score():
    return interview_state["attention"]


def get_status():
    return interview_state["status"]


# ============================================================
# Camera
# ============================================================

def show_camera():

    st.markdown(
        """
        <style>
        video{
            width:100% !important;
            max-width:600px !important;
            height:auto !important;
            display:block;
            margin:auto;
            border-radius:15px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    webrtc_streamer(
        key="camera_test",
        video_frame_callback=video_frame_callback,
        media_stream_constraints={
            "video": True,
            "audio": False,
        },
        async_processing=True,
    )