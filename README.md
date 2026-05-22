# 🧠 Smart Pupillometry System

An AI-powered pupillometry and eye triage system developed using OpenCV, FastAPI, and Streamlit for preliminary pupil analysis and healthcare-oriented triage support.

---

# 📌 Project Overview

The Smart Pupillometry System is a computer vision-based healthcare prototype designed to:

- Detect pupil characteristics from uploaded eye images
- Perform pupil measurement and calibration
- Analyze image quality conditions
- Classify pupil conditions
- Provide preliminary triage interpretation

The system combines image processing techniques with an interactive dashboard interface to support real-time eye analysis.

---

# 🚀 Features

✅ Pupil Detection using OpenCV  
✅ Pupil Area Measurement  
✅ Radius Calculation  
✅ Pupil-to-Iris Ratio Calibration  
✅ Brightness Validation  
✅ Blur Detection  
✅ Triage Classification  
✅ Clinical Interpretation  
✅ Interactive Dashboard UI  
✅ FastAPI Backend  
✅ Streamlit Frontend  

---

# 🏗️ System Architecture

## Frontend
- Streamlit
- Interactive healthcare dashboard
- Image upload interface
- Real-time analysis display

## Backend
- FastAPI
- OpenCV image processing
- Calibration and classification logic

## Image Processing Pipeline

1. Image Upload
2. Grayscale Conversion
3. Gaussian Blur
4. Adaptive Thresholding
5. Contour Detection
6. Pupil Measurement
7. Calibration
8. Classification
9. Interpretation Output

---

# 📊 Calibration Method

The system uses a simplified pupil-to-iris ratio calibration approach:

Pupil-to-Iris Ratio = Pupil Radius / Iris Radius

This helps reduce variations caused by:
- image resolution
- camera distance
- image scaling

---
<img width="732" height="351" alt="image" src="https://github.com/user-attachments/assets/1c9b6c47-f91c-4da1-86e6-b70b63ff8f59" />

# 🩺 Classification Thresholds
<img width="618" height="335" alt="image" src="https://github.com/user-attachments/assets/f5d790ce-fa1c-4cf5-b3ed-a116bf7bdd12" />

| Pupil-to-Iris Ratio | Classification |
|---|---|
| < 0.20 | Constricted Pupil |
| 0.20 – 0.55 | Normal Pupil |
| > 0.55 | Dilated Pupil |
<img width="652" height="367" alt="image" src="https://github.com/user-attachments/assets/3d43c7dd-d2b2-49eb-a17c-f9448fe33102" />

---

# ⚠️ Environmental Considerations

System performance may be affected by:

- poor lighting conditions
- image blur
- reflections
- camera angle
- camera distance
- low-quality eye images

---

# 🛠️ Technologies Used

- Python
- OpenCV
- NumPy
- Streamlit
- FastAPI

---
▶️ Installation
Clone Repository
git clone https://github.com/Amakye94/Smart-pupillometry-system-final.git
Navigate Into Project
cd Smart-pupillometry-system-final
Install Dependencies
pip install -r requirements.txt
▶️ Run Streamlit Frontend
streamlit run App.py
▶️ Run FastAPI Backend
uvicorn api:app --reload
📸 Usage
Upload an eye image
Click “Analyze”
View:
pupil measurements
calibration metrics
classification
interpretation
image quality metrics
# 📂 Project Structure

```bash
Smart-pupillometry-system-final/
│
├── backend/
│   └── pupil.py
│
├── App.py
├── api.py
├── requirements.txt
└── README.md# Smart-pupillometry-system-final
