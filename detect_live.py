from flask import Flask, render_template, Response
import cv2
import torch
import pandas as pd
from ultralytics import YOLO
import os

app = Flask(__name__)

# Load YOLO model
yolo_model = YOLO("yolov8s.pt")  # Ensure correct path

# Load pill details CSV
csv_path = "pill_details.csv"  # Update with correct path
pill_data = pd.read_csv(csv_path) if os.path.exists(csv_path) else None

# Initialize camera
camera = cv2.VideoCapture(0)  # Use 0 for default webcam, change for external cameras


def get_pill_details(pill_name):
    """Fetch pill details from CSV based on detected pill name."""
    if pill_data is not None:
        details = pill_data[pill_data["Pill Name"] == pill_name].to_dict(orient='records')
        return details[0] if details else {}
    return {}


def generate_frames():
    """Generator function to process live camera frames."""
    while True:
        success, frame = camera.read()
        if not success:
            break

        # Perform YOLO detection
        results = yolo_model(frame)
        
        detected_pills = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                label = result.names[class_id]
                
                # Get pill details
                pill_info = get_pill_details(label)
                detected_pills.append(pill_info)
                
                # Draw bounding box & label
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                text = f"{label} {confidence:.2f}"
                cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/pill_details')
def pill_details():
    """Returns detected pill details in JSON format."""
    return {"detected_pills": detected_pills}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)