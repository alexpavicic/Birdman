import tkinter as tk
from tkinter import filedialog, messagebox
import os
import cv2
import subprocess

class ObjectDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Object Detection Tool")
        self.root.geometry("900x600")  # Set initial window size
        self.root.configure(bg="#f0f0f0")

        # Create a main frame
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")  # Set background color
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Upload Folder button
        self.upload_button = tk.Button(self.main_frame, text="Upload Folder", command=self.upload_folder, bg="#4CAF50",
                                       fg="white", font=("Helvetica", 12, "bold"), relief=tk.RAISED)
        self.upload_button.pack(pady=20, padx=50, ipadx=20, ipady=10)

        # Analyze Folder button
        self.upload_button = tk.Button(self.main_frame, text="Analyze Folder", command=self.choose_video, bg="#4CAF50",
                                       fg="white", font=("Helvetica", 12, "bold"), relief=tk.RAISED)
        self.upload_button.pack(pady=20, padx=50, ipadx=20, ipady=10)

        # Set Custom confidence 
        self.upload_button = tk.Button(self.main_frame, text="Set Confidence", command=self.confidence_level, bg="#4CAF50",
                                       fg="white", font=("Helvetica", 12, "bold"), relief=tk.RAISED)
        self.upload_button.pack(pady=20, padx=50, ipadx=20, ipady=10)

        # Detected Objects section
        self.detected_objects_frame = tk.Frame(self.main_frame, bg="#f0f0f0")  # Set background color
        self.detected_objects_frame.pack(expand=True, fill=tk.BOTH, pady=10)

        # Create frames for each folder
        self.create_folder_ui(self.detected_objects_frame, "Male House Finch")
        self.create_folder_ui(self.detected_objects_frame, "Female House Finch")
        self.create_folder_ui(self.detected_objects_frame, "Unknown")

        # default confidence
        self.custom_confidence = "0.5"

        # Video/Image source:
        self.uploaded_filename = None
        self.chosen_vid = None

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
        delete_button = tk.Button(folder_frame, text="Delete", command=lambda: self.delete_image(images_listbox, folder_name),
                                  bg="#f44336", fg="white", font=("Helvetica", 10, "bold"), relief=tk.RAISED)
        delete_button.pack(pady=5)

        # Move button to move selected item to another folder
        move_button = tk.Button(folder_frame, text="Move to Other Folder",
                                command=lambda: self.move_image(images_listbox), bg="#008CBA", fg="white",
                                font=("Helvetica", 10, "bold"), relief=tk.RAISED)
        move_button.pack(pady=5)

        # Store the Listbox reference
        setattr(self, f"{folder_name.lower().replace(' ', '_')}_listbox", images_listbox)

    # Function to upload video file
    def upload_folder(self):
        self.uploaded_folder = filedialog.askdirectory(mustexist=True, title="Select a Folder")  # Store the uploaded folder
       
        self.folder_contents = os.listdir(self.uploaded_folder)

        for i in self.folder_contents:
            if ".mp4" in i:
                # self.uploaded_filename = self.uploaded_folder + file_str + i
                self.uploaded_filename = os.path.join(self.uploaded_folder, i)
                self.perform_object_detection()

    def confidence_level(self):
        # User input for custom confidence level
        def display_message():
            self.custom_confidence = entry.get()
            message_label.configure(text=f"Confidence set to:{self.custom_confidence}!")

        # Create the main window
        window = tk.Tk()
        window.title("Set Custom Confidence between 0.0 - 1.0")

        # Create an Entry widget
        entry = tk.Entry(window, width=30)
        entry.pack()
        # Create a button to display the welcome message
        button = tk.Button(window, text="Submit", command=display_message)
        button.pack()

        # Message Label
        message_label = tk.Label(window, text="")
        message_label.pack()

    # Perform object detection
    def perform_object_detection(self):
        # Change the working directory to YOLOv7
        os.chdir('YOLOv7')

        self.file_save = list(self.uploaded_filename.split("/"))
        self.file_save = self.file_save[len(self.file_save)-1].rstrip(".mp4")

        try:
            # Now paths in detect.py will be relative to YOLOv7
            command = [
                'python3', 'detect.py',
                '--weights', 'weights/house_finch.pt',
                '--conf', self.custom_confidence,
                '--img-size', '640',
                '--source', self.uploaded_filename,  # Assuming filename is an absolute path
                '--no-trace',
                '--save-txt',
                '--save-conf',
                '--project', 'Results/Detect',
                '--name', self.file_save
            ]
            subprocess.run(command, check=True)
        finally:
            # Change back to the original directory
            os.chdir(self.base_directory)

        # After object detection, extract frames and update UI
        self.extract_frames_with_labels(self.update_ui)
        self.preserve_labels(self.update_ui)

    # Extract frames from video and save along with text labels

    def extract_frames_with_labels(self, callback=None):

        video = self.file_save + ".mp4"
        analyze_output = list(os.listdir(os.path.join(self.base_directory, "YOLOv7", "Results", "Detect")))
        filter_analyze_output = len([i for i in analyze_output if self.file_save in i])

        if filter_analyze_output > 1:
            video_version = self.file_save + str(filter_analyze_output)

        else:
            video_version = self.file_save

        output_video_path = os.path.join("YOLOv7", "Results", "Detect", video_version, str(video))
        video_capture = cv2.VideoCapture(output_video_path)
        success, frame = video_capture.read()
        dest_directory = os.path.join(self.base_directory, "Results", video_version)
        frame_count = 0

        while success:
            frame_count += 1
            frame_filename = f"{os.path.splitext(os.path.basename(self.uploaded_filename))[0]}_{frame_count}.jpg"
            cv2.imwrite(frame_filename, frame)

            # Move frame to appropriate folder based on text label
            label_filename = f"{os.path.splitext(os.path.basename(self.uploaded_filename))[0]}_{frame_count}.txt"
            label_filepath = os.path.join("YOLOv7", "Results", "Detect", video_version, "labels", label_filename)

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

        # last check for bug
        base_dir_contents = os.listdir(self.base_directory)
        for i in base_dir_contents:
            if ".jpg" in i:

                image = os.path.join(self.base_directory, i)
                dest_dir = os.path.join(self.base_directory, "Results", video_version, "Detected_Objects", "Unknown", i)
                os.rename(image, dest_dir)

        video_capture.release()

        # remove video once analysis has finished
        os.remove(output_video_path)

        # Call the callback function if provided (to update UI)
        if callback:
            callback()

    def preserve_labels(self, callback=None):
        # Moves the labels from the recently analyzed video to Results folder
        analyze_output = list(os.listdir(os.path.join(self.base_directory, "YOLOv7", "Results", "Detect")))
        filter_analyze_output = len([i for i in analyze_output if self.file_save in i])

        if filter_analyze_output > 1:
            video_version = self.file_save + str(filter_analyze_output)

        else:
            video_version = self.file_save

        labels = os.listdir(os.path.join("YOLOv7", "Results", "Detect", video_version, "labels"))

        for label in labels:

            labl = os.path.join("YOLOv7", "Results", "Detect", video_version, "labels", label)
            dest_dir = os.path.join("Results", video_version, "Detected_Objects", "Label")

            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir, exist_ok=True)

            os.rename(labl, os.path.join(dest_dir, label))

        labl_dir = os.path.join("YOLOv7", "Results", "Detect", video_version, "labels")
        os.rmdir(labl_dir)


    # Get class name based on class id
    def get_class_name(self, class_id):
        # Class mapping for Male House Finch and Female House Finch
        if class_id == 0:
            return "Male House Finch"
        elif class_id == 1:
            return "Female House Finch"
        else:
            return None

    # Function to delete selected image from listbox and folder
    def delete_image(self, images_listbox, folder_name):
        selected_index = images_listbox.curselection()
        if selected_index:
            selected_item = images_listbox.get(selected_index)
            file_path = os.path.join(self.chosen_vid, "Detected_Objects", folder_name, selected_item)

            # Delete file from filesystem
            try:
                os.remove(file_path)
            except OSError as e:
                messagebox.showerror("Error", f"Error deleting file: {str(e)}")
                return

            # Delete file from Listbox
            images_listbox.delete(selected_index)

    # Function to move selected image to another folder
    def move_image(self, images_listbox):
        selected_index = images_listbox.curselection()
        if selected_index:
            selected_item = images_listbox.get(selected_index)

            # Attempt to split selected_item into parts based on " - "
            item_parts = selected_item.split(" - ")

            # Check if item_parts contains at least two parts
            if len(item_parts) < 2:
                # Display an error message if the format is invalid
                messagebox.showerror("Error", "Invalid selection format")
                return

            # Extract obj_class and timestamp from item_parts
            # obj_class = item_parts[0]
            name = item_parts[0]
            timestamp = item_parts[1]

            # Prompt the user to select a destination folder
            destination_folder = filedialog.askdirectory(title="Select Destination Folder")
            if destination_folder:
                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)

                # Move the selected item to the destination folder (replace with actual move logic)
                print(f"Moving {selected_item} to {destination_folder}")

                # Update the UI to reflect the changes (refresh Listbox contents)
                self.update_ui()

    def choose_video(self):
        # Allows user to choose video to analyze frames
        self.chosen_vid = filedialog.askdirectory(mustexist=True, initialdir=os.path.join(self.base_directory, "Results"), title="Select a Folder to Analyze")
        folders = ["Male House Finch", "Female House Finch", "Unknown"]

        for folder_name in folders:
            images_listbox = getattr(self, f"{folder_name.lower().replace(' ', '_')}_listbox", None)
            if images_listbox:
                images_listbox.delete(0, tk.END)  # Clear existing items
                # Get list of files in the folder
                folder_path = os.path.join(self.chosen_vid, "Detected_Objects", folder_name)
                if os.path.exists(folder_path) and os.path.isdir(folder_path):
                    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
                    for file_name in files:
                        images_listbox.insert(tk.END, file_name)

    def update_ui(self):
        # Update the UI to display all files in each folder
        folders = ["Male House Finch", "Female House Finch", "Unknown"]

        for folder_name in folders:
            images_listbox = getattr(self, f"{folder_name.lower().replace(' ', '_')}_listbox", None)
            if images_listbox:
                images_listbox.delete(0, tk.END)  # Clear existing items

                # Get list of files in the folder
                folder_path = os.path.join("Results", "Detected_Objects", folder_name)
                if os.path.exists(folder_path) and os.path.isdir(folder_path):
                    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
                    for file_name in files:
                        images_listbox.insert(tk.END, file_name)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":

    root = tk.Tk()
    app = ObjectDetectionApp(root)
    app.run()
