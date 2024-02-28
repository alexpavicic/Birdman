import os
import shutil
from sklearn.model_selection import train_test_split
from random import randint

def clear_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

# Define your paths
source_images_dir = ''
source_labels_dir = ''
train_images_dir = ''
train_labels_dir = ''
val_images_dir = ''
val_labels_dir = ''

# Clear existing files in training and validation directories
clear_directory(train_images_dir)
clear_directory(train_labels_dir)
clear_directory(val_images_dir)
clear_directory(val_labels_dir)

# Ensure the output directories exist
os.makedirs(train_images_dir, exist_ok=True)
os.makedirs(train_labels_dir, exist_ok=True)
os.makedirs(val_images_dir, exist_ok=True)
os.makedirs(val_labels_dir, exist_ok=True)

# Get a list of filenames without the file extension
filenames = [os.path.splitext(f)[0] for f in os.listdir(source_images_dir) if os.path.isfile(os.path.join(source_images_dir, f))]

# Split filenames into training and validation sets, without specifying random_state for true randomization
train_filenames, val_filenames = train_test_split(filenames, test_size=0.3, random_state=randint(0, 1000))

print(f'{len(train_filenames)}\n\n{len(val_filenames)}\n\n')


# Function to copy files
def copy_files(filenames, source_dir_images, source_dir_labels, target_dir_images, target_dir_labels, file_extension_image, file_extension_label):
    for filename in filenames:
        # Copy image files to their respective directories
        image_source_path = os.path.join(source_dir_images, f"{filename}{file_extension_image}")
        image_target_path = os.path.join(target_dir_images, f"{filename}{file_extension_image}")
        if os.path.exists(image_source_path):  # Check if the source image file exists before copying
            shutil.copy2(image_source_path, image_target_path)
       
        # Copy label files to their respective directories
        label_source_path = os.path.join(source_dir_labels, f"{filename}{file_extension_label}")
        label_target_path = os.path.join(target_dir_labels, f"{filename}{file_extension_label}")
        if os.path.exists(label_source_path):  # Check if the source label file exists before copying
            shutil.copy2(label_source_path, label_target_path)

# Copy files to their respective directories
copy_files(train_filenames, source_images_dir, source_labels_dir, train_images_dir, train_labels_dir, '.jpg', '.txt')
copy_files(val_filenames, source_images_dir, source_labels_dir, val_images_dir, val_labels_dir, '.jpg', '.txt')

print(f"Training images and labels copied: {len(train_filenames)}")
print(f"Validation images and labels copied: {len(val_filenames)}")
