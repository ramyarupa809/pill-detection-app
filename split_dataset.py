import os
import shutil
import random

# Paths
images_root = r"C:\Users\jandh\OneDrive\Desktop\pill_1000\images"
labels_root = r"C:\Users\jandh\Downloads\pills\labels\train"
output_root = r"C:\Users\jandh\OneDrive\Desktop\pill_1000\dataset"

# Train/Val/Test split ratio
train_ratio = 0.7
val_ratio = 0.2
test_ratio = 0.1

# Ensure output directories exist
for split in ["train", "val", "test"]:
    os.makedirs(os.path.join(output_root, split, "images"), exist_ok=True)
    os.makedirs(os.path.join(output_root, split, "labels"), exist_ok=True)

# Get all pill categories (folders)
pill_classes = [folder for folder in os.listdir(images_root) if os.path.isdir(os.path.join(images_root, folder))]

for pill in pill_classes:
    pill_image_path = os.path.join(images_root, pill)
    pill_label_path = os.path.join(labels_root, pill)

    if not os.path.exists(pill_label_path):
        print(f"Skipping {pill}, no matching label folder found.")
        continue

    # Get all image files for this class
    image_files = [f for f in os.listdir(pill_image_path) if f.endswith(('.jpg', '.png', '.jpeg'))]

    # Shuffle for randomness
    random.shuffle(image_files)

    # Split dataset
    total = len(image_files)
    train_split = int(total * train_ratio)
    val_split = int(total * val_ratio)

    train_files = image_files[:train_split]
    val_files = image_files[train_split:train_split + val_split]
    test_files = image_files[train_split + val_split:]

    # Function to move files
    def move_files(files, split):
        for file in files:
            img_src = os.path.join(pill_image_path, file)
            label_src = os.path.join(pill_label_path, file.replace('.jpg', '.txt').replace('.png', '.txt').replace('.jpeg', '.txt'))

            # Destination paths
            img_dest = os.path.join(output_root, split, "images")
            label_dest = os.path.join(output_root, split, "labels")

            os.makedirs(img_dest, exist_ok=True)
            os.makedirs(label_dest, exist_ok=True)

            shutil.move(img_src, os.path.join(img_dest, file))

            if os.path.exists(label_src):
                shutil.move(label_src, os.path.join(label_dest, os.path.basename(label_src)))

    # Move files to respective directories
    move_files(train_files, "train")
    move_files(val_files, "val")
    move_files(test_files, "test")

print("✅ Dataset successfully split and organized.")
