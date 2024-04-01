import tkinter as tk
from tkinter import filedialog
import os
from datetime import datetime
import subprocess
import cv2


class ObjectDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Object Detection Tool")
        self.root.geometry("800x500")  # Set initial window size

        # Set background color
        self.root.configure(bg="#f0f0f0")

        # Create a main frame
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")  # Set background color
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Upload Video button
        self.upload_button = tk.Button(self.main_frame, text="Upload Video", command=self.upload_video, bg="#4CAF50",
                                       fg="white", font=("Helvetica", 12, "bold"), relief=tk.RAISED)
        self.upload_button.pack(pady=10)

        # Detected Objects section
        self.detected_objects_frame = tk.Frame(self.main_frame, bg="#f0f0f0")  # Set background color
        self.detected_objects_frame.pack(expand=True, fill=tk.BOTH, pady=10)

        # Create frames for each folder
        self.create_folder_ui(self.detected_objects_frame, "Bird")
        self.create_folder_ui(self.detected_objects_frame, "House Finch")
        self.create_folder_ui(self.detected_objects_frame, "Maybe")

        # Video/Image source:
        self.filename = None

    # Create UI elements for each folder
    def create_folder_ui(self, parent, folder_name):
        folder_frame = tk.LabelFrame(parent, text=folder_name, bg="#f0f0f0", relief=tk.GROOVE)
        folder_frame.pack(side="left", padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Listbox to display detected objects
        images_listbox = tk.Listbox(folder_frame, width=30, height=15)
        images_listbox.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

        # Scrollbar for the listbox
        scrollbar = tk.Scrollbar(folder_frame, orient="vertical")
        scrollbar.config(command=images_listbox.yview)
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
        print(f'{type(self.uploaded_filename)}, {self.uploaded_filename}')

        if self.uploaded_filename:
            current_directory = os.getcwd()
            relative_path = os.path.relpath(self.uploaded_filename, current_directory)
            print("Absolute path:", self.uploaded_filename)
            print("Relative path:", relative_path)

        # Perform object detection
        detected_objects = self.perform_object_detection(self.uploaded_filename)
        print("Success")
        self.update_ui(detected_objects)

    # Placeholder for object detection logic
    def perform_object_detection(self, filename):
        print(f"File name:{filename}")
        # Replace this with your actual object detection code
        # For simplicity, returning a list of detected objects with class and timestamp
        # detected_objects = [("Bird", "2024-02-21 12:00:00"), ("House Finch", "2024-02-21 12:05:00")]
        # return detected_objects

        # Save the current working directory
        original_cwd = os.getcwd()

        # Change the working directory to YOLOv7
        os.chdir('YOLOv7')

        try:
            # Now paths in detect.py will be relative to YOLOv7
            command = [
                'python3', 'detect.py',
                '--weights', 'weights/best_v5.pt',
                '--conf', '0.5',
                '--img-size', '640',
                '--source', filename,  # Assuming filename is an absolute path
                '--no-trace',
                '--save-txt',
                '--save-conf',
                '--project', 'Results/Detect',
                '--name', 'Runs'
            ]
            subprocess.run(command, check=True)
        finally:
            # Change back to the original directory
            os.chdir(original_cwd)

    # Update UI with detected objects
    def update_ui(self, detected_objects):
        for obj_class, timestamp in detected_objects:
            if obj_class == "Bird":
                images_listbox = self.bird_folder.winfo_children()[1]
            elif obj_class == "House Finch":
                images_listbox = self.house_finch_folder.winfo_children()[1]
            else:
                images_listbox = self.maybe_folder.winfo_children()[1]
            images_listbox.insert(tk.END, f"{obj_class} - {timestamp}")

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
