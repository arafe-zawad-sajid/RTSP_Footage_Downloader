# To run: python video_to_img.py --input_folder [video_folder_path]

import cv2
import os
import argparse

def capture_frames_from_folder(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each video in the input folder
    for file in os.listdir(input_folder):
        if file.endswith('.mp4'):
            video_path = os.path.join(input_folder, file)
            video_name = os.path.splitext(file)[0]
            output_video_folder = os.path.join(output_folder, video_name)
            
            # Create a folder for this video's snapshots
            if not os.path.exists(output_video_folder):
                os.makedirs(output_video_folder)
            
            capture_and_save_frames(video_path, output_video_folder)

def capture_and_save_frames(video_path, output_folder):
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Failed to open video: {video_path}")
            return

        interval = 10  # Capture every 10th frame

        success, frame = cap.read()
        count = 0
        while success:
            if count % interval == 0:
                save_frame(frame, count, output_folder)
            success, frame = cap.read()
            count += 1
        cap.release()
        print(f"Finished processing: {video_path}")
    except Exception as e:
        print(f"Error capturing frames from {video_path}: {e}")

def save_frame(frame, frame_number, output_folder):
    try:
        frame_file_path = os.path.join(output_folder, f"frame_{frame_number:04d}.jpg")
        cv2.imwrite(frame_file_path, frame)
    except Exception as e:
        print(f"Error saving frame {frame_number}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Capture frames from videos in a folder")
    parser.add_argument("--input_folder", help="Path to the folder containing MP4 videos")
    parser.add_argument("--output_folder", help="Path to save the output snapshots (default: 'output' in the same directory as input)")
    
    args = parser.parse_args()

    input_folder = args.input_folder
    if args.output_folder:
        output_folder = args.output_folder
    else:
        output_folder = os.path.join(os.path.dirname(input_folder), "output")

    if not os.path.isdir(input_folder):
        print(f"Error: {input_folder} is not a valid directory")
        return

    print(f"Processing videos from: {input_folder}")
    print(f"Saving snapshots to: {output_folder}")
    
    capture_frames_from_folder(input_folder, output_folder)

if __name__ == "__main__":
    main()