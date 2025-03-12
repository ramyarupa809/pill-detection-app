import os
import cv2
import torch
import numpy as np
import pandas as pd
from flask import Flask, render_template, Response, request, jsonify
from werkzeug.utils import secure_filename
from ultralytics import YOLO

app = Flask(__name__)

# ✅ Load YOLO model from the root directory
MODEL_PATH = os.path.join(os.getcwd(), "best.pt")  # Ensure correct path
model = YOLO(MODEL_PATH)

# ✅ Load pill details from CSV
csv_file = "pill_details.csv"
pill_data = pd.read_csv(csv_file) if os.path.exists(csv_file) else None

# ✅ Check if running locally (for laptop camera)
running_locally = os.environ.get("RENDER") is None
if running_locally:
    camera = cv2.VideoCapture(0)  # Only works locally


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


### === ROUTE FOR LIVE DETECTION PAGE === ###
@app.route("/live")
def live():
    return render_template("live.html")


### === ROUTE FOR VIDEO STREAMING (LAPTOP ONLY) === ###
@app.route("/video_feed")
def video_feed():
    if running_locally:
        return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")
    else:
        return "Live video is only available on local devices."


### === FUNCTION TO PROCESS VIDEO FRAMES (LAPTOP ONLY) === ###
def generate_frames():
    while running_locally:
        success, frame = camera.read()
        if not success:
            break
        else:
            results = model(frame)
            frame = results[0].plot()

            _, buffer = cv2.imencode(".jpg", frame)
            frame_bytes = buffer.tobytes()
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")


### === ROUTE FOR MOBILE CAMERA IMAGE UPLOAD === ###
@app.route("/upload_live", methods=["POST"])
def upload_live():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join("static/uploads", filename)
    file.save(file_path)

    # Run detection
    result_image, detected_pills = detect_pills(file_path)

    return jsonify({"filename": os.path.basename(result_image)})


### === FUNCTION TO DETECT PILLS IN UPLOADED IMAGE === ###
def detect_pills(image_path):
    img = cv2.imread(image_path)
    results = model(img)
    detected_img = results[0].plot()

    output_path = os.path.join("static/detected", os.path.basename(image_path))
    cv2.imwrite(output_path, detected_img)

    # Get detected class names
    detected_classes = []
    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])  # Class index
            detected_classes.append(model.names[cls])  # Get class label

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


### === ROUTE TO SERVE DETECTED OUTPUT IMAGES === ###
@app.route("/detected/<filename>")
def output_file(filename):
    return f"/static/detected/{filename}"


### === ROUTE FOR VIDEO UPLOAD DETECTION === ###
@app.route("/upload_video", methods=["POST"])
def upload_video():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join("static/uploads", filename)
    file.save(file_path)

    output_video = process_video(file_path)

    return jsonify({"filename": os.path.basename(output_video)})


### === FUNCTION TO PROCESS VIDEO UPLOADS === ###
def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    output_path = os.path.join("static/detected", os.path.basename(video_path))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (640, 480))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        frame = results[0].plot()
        out.write(frame)

    cap.release()
    out.release()
    return output_path


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
