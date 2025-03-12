import os

labels_path = r"C:\Users\jandh\OneDrive\Desktop\pill_1000\dataset\train\labels"

# Collect all unique class indices
classes = set()
for label_file in os.listdir(labels_path):
    if label_file.endswith(".txt"):
        with open(os.path.join(labels_path, label_file), "r") as f:
            for line in f:
                class_id = line.split()[0]  # First number in each line is the class ID
                classes.add(class_id)

# Convert to sorted list
class_list = sorted(list(classes), key=int)

# Print results
print(f"Total Classes: {len(class_list)}")
print("Class IDs:", class_list)
