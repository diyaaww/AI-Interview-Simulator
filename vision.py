import av
import cv2

from streamlit_webrtc import VideoProcessorBase

from camera import process_frame


class VideoProcessor(VideoProcessorBase):

    def recv(self, frame):

        img = frame.to_ndarray(format="bgr24")

        img, face_found = process_frame(img)

        return av.VideoFrame.from_ndarray(
            img,
            format="bgr24"
        )