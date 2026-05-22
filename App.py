import streamlit as st
from backend.pupil import detect_pupil
import tempfile
import sys
import os

sys.path.append(os.path.abspath("."))

# -----------------------------------
# VALIDATION FUNCTION
# -----------------------------------
def is_valid_pupil(data):

    if data is None:
        return False

    if "error" in data:
        return False

    if data.get("pupil_area", 0) <= 0:
        return False

    if data.get("radius", 0) <= 0:
        return False

    normalized = data.get("normalized_radius", None)

    if normalized is None:
        return False

    if normalized <= 0 or normalized > 1:
        return False

    return True


# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Smart Pupillometry",
    layout="centered"
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------
st.markdown("""
<style>

body {
    background-color: #0E1117;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #4FC3F7;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #BBBBBB;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# TITLE
# -----------------------------------
st.markdown(
    '<div class="title">🧠 Smart Pupillometry</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-powered eye triage system</div>',
    unsafe_allow_html=True
)

# -----------------------------------
# IMAGE GUIDE
# -----------------------------------
st.info("""
📸 IMAGE CAPTURE GUIDELINES

• Use clear lighting

• Avoid blurry images

• Keep camera close to the eye

• Avoid reflections or flash glare

• Ensure the pupil is clearly visible
""")

# -----------------------------------
# FILE UPLOAD
# -----------------------------------
uploaded_file = st.file_uploader(
    "📸 Upload an eye image",
    type=["jpg", "jpeg", "png"]
)

# -----------------------------------
# ANALYSIS
# -----------------------------------
if uploaded_file:

    st.image(
        uploaded_file,
        caption="Uploaded Image",
        width=300
    )

    if st.button("🔍 Analyze"):

        # Save temporary image
        with tempfile.NamedTemporaryFile(delete=False) as tmp:

            tmp.write(uploaded_file.getvalue())
            temp_path = tmp.name

        # Run pupil detection
        data = detect_pupil(temp_path)

        # -----------------------------------
        # ERROR HANDLING
        # -----------------------------------
        if "error" in data:

            st.error(f"❌ {data['error']}")
            st.stop()

        # -----------------------------------
        # VALIDATION
        # -----------------------------------
        if not is_valid_pupil(data):

            st.error(
                "❌ No valid pupil detected. "
                "Please upload a clearer eye image."
            )

            st.stop()

        # -----------------------------------
        # ANALYSIS RESULT
        # -----------------------------------

        st.markdown("## 🧠 Analysis Dashboard")

        # -----------------------------------
        # METRIC CARDS
        # -----------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "📏 Pupil Area",
                f"{data['pupil_area']} px²"
            )

            st.metric(
                "📐 Radius",
                f"{data['radius']} px"
            )

        with col2:

            st.metric(
                "👁️ Iris Radius",
                f"{data['iris_radius']} px"
            )

            st.metric(
                "📊 PIR Ratio",
                f"{data['pupil_to_iris_ratio']}"
            )

        st.divider()

        # -----------------------------------
        # CLASSIFICATION PANEL
        # -----------------------------------

        st.subheader("🩺 Classification")

        if data["priority"] == "HIGH":

            st.error(
                f"🔴 {data['status']} — HIGH PRIORITY"
            )

        elif data["priority"] == "MEDIUM":

            st.warning(
                f"🟠 {data['status']} — MEDIUM PRIORITY"
            )

        else:

            st.success(
                f"🟢 {data['status']} — LOW PRIORITY"
            )

        # -----------------------------------
        # INTERPRETATION
        # -----------------------------------

        st.subheader("📖 Interpretation")

        st.info(data["interpretation"])

        st.divider()

        # -----------------------------------
        # IMAGE QUALITY
        # -----------------------------------

        st.subheader("💡 Image Quality Metrics")

        st.write(
            f"Brightness Score: {data['brightness_score']}"
        )

        st.progress(
            min(int(data["brightness_score"]), 100)
        )

        st.write(
            f"Blur Score: {data['blur_score']}"
        )

        blur_percentage = min(
            int(data["blur_score"] / 50),
            100
        )

        st.progress(blur_percentage)

        st.divider()

        # -----------------------------------
        # CALIBRATION GUIDE
        # -----------------------------------

        with st.expander("📘 Calibration & Measurement Guide"):

            st.markdown("""

### 📏 Pupil Area
Represents the detected pupil region in pixels.

### 📐 Radius
Distance from pupil center to pupil edge.

### 👁️ Iris Radius
Estimated iris radius used for calibration.

### 📊 Pupil-to-Iris Ratio
Calibration-adjusted ratio used to standardize measurements across image sizes.

### 🩺 Classification Thresholds

- Less than 0.20 → Constricted pupil
- 0.20 to 0.55 → Normal pupil
- Greater than 0.55 → Dilated pupil

### ⚠️ Environmental Factors

Lighting conditions, reflections, image blur,
camera angle, and camera distance may affect measurement accuracy.

""")