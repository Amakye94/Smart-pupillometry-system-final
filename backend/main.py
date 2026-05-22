from fastapi import FastAPI, UploadFile, File
import shutil
import os
from backend.pupil import detect_pupil

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Smart Pupillometry API Running 🚀"}


@app.post("/analyze/")
async def analyze(file: UploadFile = File(...)):
    
    # Save uploaded file
    file_location = f"temp_{file.filename}"
    
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run detection
    result = detect_pupil(file_location)

    # Delete temp file (clean system)
    os.remove(file_location)

    return result