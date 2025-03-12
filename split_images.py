import os
import shutil

# Define paths
images_path = r"C:/Users/jandh/OneDrive/Desktop/pill_1000/images"
labels_path = r"C:/Users/jandh/Downloads/pills/labels/train"
output_path = r"C:/Users/jandh/OneDrive/Desktop/pill_1000/dataset"

# Ensure the output dataset directory exists
os.makedirs(output_path, exist_ok=True)

# Get all label folders
label_folders = [folder for folder in os.listdir(labels_path) if os.path.isdir(os.path.join(labels_path, folder))]

# Create corresponding folders in the dataset directory
for label in label_folders:
    label_folder_path = os.path.join(output_path, label)
    os.makedirs(label_folder_path, exist_ok=True)

    # Find corresponding images in images_path
    image_folder_path = os.path.join(images_path, label)
    if os.path.exists(image_folder_path):
        for img in os.listdir(image_folder_path):
            img_src = os.path.join(image_folder_path, img)
            img_dest = os.path.join(label_folder_path, img)
            shutil.move(img_src, img_dest)  # Move images

print("Images have been organized successfully into respective folders.")
