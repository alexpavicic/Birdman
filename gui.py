import tkinter as tk
from tkinter import filedialog
import os
from datetime import datetime
import cv2

class ObjectDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Object Detection Tool")
        self.uploaded_filename = ""  # Initialize an instance variable to store the uploaded filename

        # Upload Video button
        self.upload_button = tk.Button(self.root, text="Upload Video", command=self.upload_video)
        self.upload_button.pack()

        # Detected Objects section
        self.detected_objects_frame = tk.Frame(self.root)
        self.detected_objects_frame.pack(pady=10)

        # Frame for Bird folder
        self.bird_folder = tk.Frame(self.detected_objects_frame)
        self.bird_folder.pack(side="left", padx=10)
        self.create_folder_ui(self.bird_folder, "Bird")

        # Frame for House Finch folder
        self.house_finch_folder = tk.Frame(self.detected_objects_frame)
        self.house_finch_folder.pack(side="left", padx=10)
        self.create_folder_ui(self.house_finch_folder, "House Finch")

        # Frame for Maybe folder
        self.maybe_folder = tk.Frame(self.detected_objects_frame)
        self.maybe_folder.pack(side="left", padx=10)
        self.create_folder_ui(self.maybe_folder, "Maybe")

    # Create UI elements for each folder
    def create_folder_ui(self, parent, folder_name):
        # Label for folder name
        label = tk.Label(parent, text=folder_name)
        label.pack()
        # Listbox to display detected objects
        images_listbox = tk.Listbox(parent, width=20, height=10)
        images_listbox.pack()

        # Delete button to remove selected item from listbox
        delete_button = tk.Button(parent, text="Delete", command=lambda: self.delete_image(images_listbox))
        delete_button.pack(pady=5)

        # Move button to move selected item to another folder
        move_button = tk.Button(parent, text="Move to Other Folder", command=lambda: self.move_image(images_listbox))
        move_button.pack()

    # Function to upload video file
    def upload_video(self):
        self.uploaded_filename = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4")])  # Store the uploaded filename
        detected_objects = self.perform_object_detection(self.uploaded_filename)
        self.update_ui(detected_objects)

    # Placeholder for object detection logic
    def perform_object_detection(self, filename):
        print(f"File name:{filename}")
        # Replace this with your actual object detection code
        # For simplicity, returning a list of detected objects with class and timestamp
        detected_objects = [("Bird", "2024-02-21 12:00:00"), ("House Finch", "2024-02-21 12:05:00")]
        return detected_objects

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

