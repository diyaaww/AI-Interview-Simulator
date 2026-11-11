import cv2


def analyze_attention(frame, face):

    height, width = frame.shape[:2]

    # =====================================
    # Target Box Settings
    # =====================================
    box_width = 250
    box_height = 280

    left = (width - box_width) // 2
    top = (height - box_height) // 2 - 20

    right = left + box_width
    bottom = top + box_height

    GREEN = (50, 205, 50)
    RED = (0, 0, 255)

    # =====================================
    # No Face
    # =====================================
    if face is None:

        cv2.rectangle(
            frame,
            (left, top),
            (right, bottom),
            RED,
            2
        )

        return frame, {
            "focused": False
        }

    # =====================================
    # Face Center
    # =====================================
    face_center_x = face["cx"]
    face_center_y = face["cy"]

    focused = (
        left <= face_center_x <= right and
        top <= face_center_y <= bottom
    )

    box_color = GREEN if focused else RED

    # =====================================
    # Draw Target Box
    # =====================================
    cv2.rectangle(
        frame,
        (left, top),
        (right, bottom),
        box_color,
        2
    )

    # =====================================
    # Face Center Dot
    # =====================================
    cv2.circle(
        frame,
        (face_center_x, face_center_y),
        5,
        RED,
        -1
    )

    # =====================================
    # Return Frame + Attention Data
    # =====================================
    return frame, {
        "focused": focused
    }