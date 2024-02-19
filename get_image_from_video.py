import cv2
import os


def extract_images_from_videos(folder_path, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file is a video
        if filename.endswith(".mp4") or filename.endswith(".avi") or filename.endswith(".mov"):
            video_path = os.path.join(folder_path, filename)
            video_name = os.path.splitext(filename)[0]

            # Create subfolder for each video
            video_output_folder = os.path.join(output_folder, video_name)
            if not os.path.exists(video_output_folder):
                os.makedirs(video_output_folder)

            # Open video file
            cap = cv2.VideoCapture(video_path)
            frame_count = 0

            # Read until video is completed
            while (cap.isOpened()):
                ret, frame = cap.read()
                if ret:
                    frame_count += 1

                    # Save frame as image
                    frame_output_path = os.path.join(video_output_folder, f"{video_name}_frame_{frame_count}.jpg")
                    cv2.imwrite(frame_output_path, frame)
                else:
                    break

            # Release the video capture object
            cap.release()


# Specify folder containing videos and output folder for extracted images
folder_origin = input("Please specify the full path to the videos: ")
folder_dest = input("Please specify the full path to an output folder: ")

while True:
    try:
        print(os.listdir(folder_origin))
        break

    except:
        print("\n")
        folder_origin = input("The location you specified does not exist, please try again: ")

# input_folder = r'C:\HOFI_training_videos'
# output_folder = r'C:\image_from_video'
extract_images_from_videos(folder_origin, folder_dest)
