import os
import cv2
import torch
import numpy as np
import pandas as pd
from flask import Flask, render_template, Response, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from ultralytics import YOLO

app = Flask(__name__)

# ✅ Ensure directories exist
os.makedirs("static/uploads", exist_ok=True)
os.makedirs("static/detected", exist_ok=True)

# ✅ Load YOLO model
MODEL_PATH = os.path.join(os.getcwd(), "best.pt")  
model = YOLO(MODEL_PATH)

# ✅ Load pill details from CSV
csv_file = "pill_details.csv"
pill_data = pd.read_csv(csv_file) if os.path.exists(csv_file) else None


### === ROUTE FOR HOME PAGE (UPLOAD IMAGE) === ###
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded", 400
        file = request.files["file"]
        if file.filename == "":
            return "No selected file", 400
        
        filename = secure_filename(file.filename)
        file_path = os.path.join("static/uploads", filename)
        file.save(file_path)

        # Run detection
        result_image, detected_pills = detect_pills(file_path)

        # Extract pill details
        pill_metadata = extract_pill_details(detected_pills)

        return render_template("result.html", filename=os.path.basename(result_image), pill_info=pill_metadata)

    return render_template("index.html")


### === ROUTE FOR IMAGE UPLOAD REDIRECT === ###
@app.route("/upload", methods=["GET", "POST"])
def upload():
    return index()  # Calls the existing upload logic


### === ROUTE TO SERVE UPLOADED IMAGES === ###
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory("static/uploads", filename)


### === ROUTE TO SERVE DETECTED OUTPUT IMAGES === ###
@app.route("/detected/<filename>")
def output_file(filename):
    return send_from_directory("static/detected", filename)


### === FUNCTION TO DETECT PILLS IN UPLOADED IMAGE === ###
def detect_pills(image_path):
    img = cv2.imread(image_path)
    results = model(img)
    detected_img = results[0].plot()  

    output_path = os.path.join("static/detected", os.path.basename(image_path))
    cv2.imwrite(output_path, detected_img)

    detected_classes = []
    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])  
            detected_classes.append(model.names[cls])  

    return output_path, detected_classes


### === FUNCTION TO EXTRACT PILL DETAILS FROM CSV === ###
def extract_pill_details(detected_classes):
    details = []
    if pill_data is not None:
        for pill in detected_classes:
            pill_info = pill_data[pill_data["Pill Name"].str.strip().str.lower() == pill.strip().lower()]
            if not pill_info.empty:
                details.append(pill_info.to_dict(orient="records")[0])
    return details


### === START THE FLASK APP === ###
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
