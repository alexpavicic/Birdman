import tkinter as tk
from tkinter import filedialog
import os
import subprocess
import cv2

class ObjectDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Object Detection Tool")
        self.root.geometry("900x600")  # Set initial window size

        # Set background color
        self.root.configure(bg="#f0f0f0")

        # Create a main frame
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")  # Set background color
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Upload Video button
        self.upload_button = tk.Button(self.main_frame, text="Upload Video", command=self.upload_video, bg="#4CAF50",
                                       fg="white", font=("Helvetica", 12, "bold"), relief=tk.RAISED)
        self.upload_button.pack(pady=20, padx=50, ipadx=20, ipady=10)

        # Detected Objects section
        self.detected_objects_frame = tk.Frame(self.main_frame, bg="#f0f0f0")  # Set background color
        self.detected_objects_frame.pack(expand=True, fill=tk.BOTH, pady=10)

        # Create frames for each folder
        self.create_folder_ui(self.detected_objects_frame, "Bird")
        self.create_folder_ui(self.detected_objects_frame, "House Finch")
        self.create_folder_ui(self.detected_objects_frame, "Maybe")

        # Video/Image source:
        self.uploaded_filename = None

        # Base working directory
        self.base_directory = os.getcwd()

    # Create UI elements for each folder
    def create_folder_ui(self, parent, folder_name):
        folder_frame = tk.LabelFrame(parent, text=folder_name, bg="#f0f0f0", relief=tk.GROOVE)
        folder_frame.pack(side="left", padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Listbox to display detected objects
        images_listbox = tk.Listbox(folder_frame, width=30, height=15, bg="white", font=("Helvetica", 10), relief=tk.FLAT)
        images_listbox.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

        # Scrollbar for the listbox
        scrollbar = tk.Scrollbar(folder_frame, orient="vertical", command=images_listbox.yview)
        scrollbar.pack(side="right", fill="y")

        images_listbox.config(yscrollcommand=scrollbar.set)

        # Delete button to remove selected item from listbox
        delete_button = tk.Button(folder_frame, text="Delete", command=lambda: self.delete_image(images_listbox),
                                  bg="#f44336", fg="white", font=("Helvetica", 10, "bold"), relief=tk.RAISED)
        delete_button.pack(pady=5)

        # Move button to move selected item to another folder
        move_button = tk.Button(folder_frame, text="Move to Other Folder",
                                command=lambda: self.move_image(images_listbox), bg="#008CBA", fg="white",
                                font=("Helvetica", 10, "bold"), relief=tk.RAISED)
        move_button.pack(pady=5)

    # Function to upload video file
    def upload_video(self):
        self.uploaded_filename = filedialog.askopenfilename(
            filetypes=[("Video Files", "*.mp4")])  # Store the uploaded filename

        if self.uploaded_filename:
            self.perform_object_detection()

    # Perform object detection
    def perform_object_detection(self):
        # Change the working directory to YOLOv7
        os.chdir('YOLOv7')

        try:
            # Now paths in detect.py will be relative to YOLOv7
            command = [
                'python3', 'detect.py',
                '--weights', 'weights/best_v5.pt',
                '--conf', '0.5',
                '--img-size', '640',
                '--source', self.uploaded_filename,  # Assuming filename is an absolute path
                '--no-trace',
                '--save-txt',
                '--save-conf',
                '--project', 'Results/Detect',
                '--name', 'Runs'
            ]
            subprocess.run(command, check=True)
        finally:
            # Change back to the original directory
            os.chdir(self.base_directory)

        # Extract frames and save along with text labels
        self.extract_frames_with_labels()

    # Extract frames from video and save along with text labels
    def extract_frames_with_labels(self):
        output_video_path = os.path.join("YOLOv7", "Results", "Detect", "Runs", f"{os.path.splitext(os.path.basename(self.uploaded_filename))[0]}.mp4")
        video_capture = cv2.VideoCapture(output_video_path)
        success, frame = video_capture.read()
        dest_directory = os.path.join(self.base_directory, "Results")
        frame_count = 0

        while success:
            frame_count += 1
            frame_filename = f"{os.path.splitext(os.path.basename(self.uploaded_filename))[0]}_{frame_count}.jpg"
            cv2.imwrite(frame_filename, frame)

            # Move frame to appropriate folder based on text label
            label_filename = f"{os.path.splitext(os.path.basename(self.uploaded_filename))[0]}_{frame_count}.txt"
            label_filepath = os.path.join("YOLOv7", "Results", "Detect", "Runs", "labels", label_filename)

            if os.path.exists(label_filepath):
                with open(label_filepath) as label_file:
                    label_lines = label_file.readlines()
                    for label_line in label_lines:
                        label_info = label_line.strip().split()
                        class_id = int(label_info[0])
                        confidence = float(label_info[-1])
                        class_name = self.get_class_name(class_id)  # Get class name based on class id

                        if class_name:
                            destination_folder = os.path.join(dest_directory, "Detected_Objects", class_name)
                            if not os.path.exists(destination_folder):
                                os.makedirs(destination_folder, exist_ok=True)
                            # Check if frame file exists before moving
                            if os.path.exists(frame_filename):
                                os.rename(frame_filename, os.path.join(destination_folder, frame_filename))


            # the condition where the model didn't identify class
            else:
                destination_folder = os.path.join(dest_directory, "Detected_Objects", "Unknown")
                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder, exist_ok=True)
                # Check if frame file exists before moving
                if os.path.exists(frame_filename):
                    os.rename(frame_filename, os.path.join(destination_folder, frame_filename))

            success, frame = video_capture.read()

        video_capture.release()

    # Get class name based on class id
    def get_class_name(self, class_id):
        # You can implement a mapping from class id to class name here
        class_mapping = {
            0: "Class_A",
            1: "Class_B",
            # Add more class mappings as needed
        }
        return class_mapping.get(class_id)

    # Function to delete selected image from listbox
    def delete_image(self, images_listbox):
        selected_index = images_listbox.curselection()
        if selected_index:
            images_listbox.delete(selected_index)

    # Function to move selected image to another folder
    def move_image(self, images_listbox):
        selected_index = images_listbox.curselection()
        if selected_index:
            selected_item = images_listbox.get(selected_index)
            obj_class, timestamp = selected_item.split(" - ")
            destination_folder = filedialog.askdirectory(title="Select Destination Folder")
            if destination_folder:
                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)
                print(f"Moving {selected_item} to {destination_folder}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ObjectDetectionApp(root)
    root.mainloop()
