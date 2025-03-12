from ultralytics import YOLO
import cv2
import sys
import os

# Load the trained YOLO model
model = YOLO("runs/detect/train/weights/best.pt")

# Define the image path (replace with your test image)
image_path = "C:/Users/jandh/OneDrive/Desktop/WhatsApp Image 2025-03-11 at 18.15.44_7e980f5b.jpg"
# Run the model on the image
results = model.predict(image_path, save=True, conf=0.4)

# Save the output image with detections
output_folder = "runs/detect/predict/"
output_image_path = os.path.join(output_folder, os.path.basename(image_path))

# Load and save the image with bounding boxes
for result in results:
    img = result.plot()  # Draw bounding boxes
    cv2.imwrite(output_image_path, img)  # Save the output image

print(f"✅ Detection complete! Check the saved image here: {output_image_path}")

