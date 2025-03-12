import os
import cv2
import torch
import numpy as np
import pandas as pd
from flask import Flask, render_template, Response, request, jsonify
from werkzeug.utils import secure_filename
from ultralytics import YOLO

app = Flask(__name__)

# ✅ Ensure model exists before loading
MODEL_PATH = os.path.join(os.getcwd(), "best.pt")
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

# ✅ Load YOLO model from the correct path
model = YOLO(MODEL_PATH)
camera = cv2.VideoCapture(0)  # Default to laptop webcam

# ✅ Load pill details CSV safely
csv_file = "pill_details.csv"
pill_data = pd.read_csv(csv_file) if os.path.exists(csv_file) else None


### === ROUTE FOR HOME PAGE (UPLOAD IMAGE) === ###
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
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


### === ROUTE FOR LIVE DETECTION PAGE === ###
@app.route("/live")
def live():
    return render_template("live.html")


### === ROUTE FOR VIDEO STREAMING (LAPTOP USERS ONLY) === ###
@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


### === FUNCTION TO PROCESS VIDEO FRAMES (LAPTOP ONLY) === ###
def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            results = model(frame)
            frame = results[0].plot()  # Ensure correct rendering of bounding boxes

            _, buffer = cv2.imencode(".jpg", frame)
            frame_bytes = buffer.tobytes()
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")


### === FUNCTION TO DETECT PILLS IN UPLOADED IMAGE === ###
def detect_pills(image_path):
    img = cv2.imread(image_path)
    results = model(img)
    detected_img = results[0].plot()  # Correct way to visualize bounding boxes

    output_path = os.path.join("static/detected", os.path.basename(image_path))
    cv2.imwrite(output_path, detected_img)

    # Get detected class names
    detected_classes = []
    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])  # Class index
            detected_classes.append(model.names[cls])  # Get class label

    print("Detected Pills:", detected_classes)  # Debug print

    return output_path, detected_classes


### === FUNCTION TO EXTRACT PILL DETAILS FROM CSV === ###
def extract_pill_details(detected_classes):
    details = []
    
    if pill_data is not None:
        for pill in detected_classes:
            # Strip spaces and make an exact match
            pill_info = pill_data[pill_data["Pill Name"].str.strip().str.lower() == pill.strip().lower()]
            if not pill_info.empty:
                details.append(pill_info.to_dict(orient="records")[0])
            else:
                print(f"Warning: No exact match found for detected pill '{pill}' in CSV.")

    return details


### === ROUTE TO SERVE UPLOADED IMAGES === ###
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return f"/static/uploads/{filename}"


### === ROUTE TO SERVE DETECTED OUTPUT IMAGES === ###
@app.route("/detected/<filename>")
def output_file(filename):
    return f"/static/detected/{filename}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
