import cv2
import numpy as np


def detect_pupil(image_path):

    # -----------------------------------
    # LOAD IMAGE
    # -----------------------------------
    frame = cv2.imread(image_path)

    if frame is None:
        return {"error": "Image not found"}

    # -----------------------------------
    # IMAGE DIMENSIONS
    # -----------------------------------
    h, w = frame.shape[:2]

    # -----------------------------------
    # GRAYSCALE
    # -----------------------------------
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # -----------------------------------
    # BLUR
    # -----------------------------------
    blur = cv2.GaussianBlur(gray, (7, 7), 0)

    # -----------------------------------
    # BRIGHTNESS VALIDATION
    # -----------------------------------
    brightness = np.mean(gray)

    if brightness < 40:
        return {
            "error": "Image too dark"
        }

    if brightness > 220:
        return {
            "error": "Image too bright"
        }

    # -----------------------------------
    # BLUR VALIDATION
    # -----------------------------------
    blur_score = cv2.Laplacian(
        gray,
        cv2.CV_64F
    ).var()

    if blur_score < 50:
        return {
            "error": "Image is blurry"
        }

    # -----------------------------------
    # THRESHOLDING
    # -----------------------------------
    thresh = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11,
        2
    )

    # -----------------------------------
    # FIND CONTOURS
    # -----------------------------------
    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        return {
            "error": "No pupil detected"
        }

    # -----------------------------------
    # SELECT LARGEST CONTOUR
    # -----------------------------------
    try:

        largest = max(
            contours,
            key=cv2.contourArea
        )

    except Exception:

        return {
            "error": "Unable to detect valid pupil contour"
        }

    area = cv2.contourArea(largest)

    if area < 50:
        return {
            "error": "Invalid pupil detection"
        }

    # -----------------------------------
    # PUPIL CIRCLE
    # -----------------------------------
    (x, y), radius = cv2.minEnclosingCircle(
        largest
    )

    # -----------------------------------
    # ESTIMATED IRIS CALIBRATION
    # -----------------------------------
    iris_radius = radius * 2

    # -----------------------------------
    # BASIC NORMALIZATION
    # -----------------------------------
    normalized_radius = radius / min(w, h)

    # -----------------------------------
    # PUPIL-TO-IRIS RATIO
    # -----------------------------------
    pupil_to_iris_ratio = radius / iris_radius

    # -----------------------------------
    # CLASSIFICATION
    # -----------------------------------
    if pupil_to_iris_ratio > 0.55:

        status = "Dilated pupil"
        priority = "HIGH"

    elif pupil_to_iris_ratio < 0.20:

        status = "Constricted pupil"
        priority = "MEDIUM"

    else:

        status = "Normal pupil"
        priority = "LOW"

    # -----------------------------------
    # INTERPRETATION
    # -----------------------------------
    if pupil_to_iris_ratio < 0.20:

        interpretation = (
            "Pupil appears constricted "
            "compared to iris size."
        )

    elif pupil_to_iris_ratio > 0.55:

        interpretation = (
            "Pupil appears dilated "
            "compared to iris size."
        )

    else:

        interpretation = (
            "Pupil-to-iris ratio falls "
            "within normal range."
        )

    # -----------------------------------
    # RETURN RESULTS
    # -----------------------------------
    return {

        "pupil_area": int(area),

        "center_x": int(x),
        "center_y": int(y),

        "radius": round(
            float(radius), 2
        ),

        "normalized_radius": round(
            float(normalized_radius), 3
        ),

        "iris_radius": round(
            float(iris_radius), 2
        ),

        "pupil_to_iris_ratio": round(
            float(pupil_to_iris_ratio), 3
        ),

        "brightness_score": round(
            float(brightness), 2
        ),

        "blur_score": round(
            float(blur_score), 2
        ),

        "status": status,
        "priority": priority,
        "interpretation": interpretation
    }