# To run: python video_to_img.py --input_folder [video_folder_path]

import cv2
import os
import argparse

def capture_frames_from_folder(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # print(f"Scanning folder: {input_folder} for .mp4 files")

    # Process each video in the input folder
    for file in os.listdir(input_folder):
        if file.endswith('.mp4'):
            video_path = os.path.join(input_folder, file)
            print(f"Processing video: {video_path}")

            video_name = os.path.splitext(file)[0]
            output_video_folder = os.path.join(output_folder, video_name)

            print(f"Saving snapshots to: {output_video_folder}")
            
            # Create a folder for this video's snapshots
            if not os.path.exists(output_video_folder):
                os.makedirs(output_video_folder)
            capture_and_save_frames(video_name, video_path, output_video_folder)
        else:
            print(f"Skipped non-MP4 file: {file}")

def capture_and_save_frames(video_name, video_path, output_folder):
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Failed to open video: {video_path}")
            return
        
        interval = 0
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        if fps<=15:
            interval = 5  # Capture every 5th frame
            print(f"Since video fps is {fps}, interval is set to {interval}")
        elif fps>=25:
            interval = 10  # Capture every 10th frame
            print(f"Since video fps is {fps}, interval is set to {interval}")

        success, frame = cap.read()
        count = 0
        while success:
            if count % interval == 0:
                # print(f"Saving frame {count} from video {video_path}")
                save_frame(video_name, frame, count, output_folder)
            success, frame = cap.read()
            count += 1
        cap.release()
        print(f"Finished processing: {video_path}")
        print(f"Total frames: {count+1}")
    except Exception as e:
        print(f"Error capturing frames from {video_path}: {e}")

def save_frame(video_name, frame, frame_number, output_folder):
    try:
        frame_file_path = os.path.join(output_folder, f"{video_name}_frame_{frame_number:04d}.jpg")
        cv2.imwrite(frame_file_path, frame)
        # print(f"Saved frame {frame_number} to {frame_file_path}")
    except Exception as e:
        print(f"Error saving frame {frame_number}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Capture frames from videos in a folder")
    parser.add_argument("--input_folder", help="Path to the folder containing MP4 videos")
    parser.add_argument("--output_folder", help="Path to save the output snapshots (default: 'output folder' in the 'input folder')")
    
    args = parser.parse_args()

    input_folder = args.input_folder
    if args.output_folder:
        output_folder = args.output_folder
    else:
        output_folder = os.path.join(input_folder)

    if not os.path.isdir(input_folder):
        print(f"Error: {input_folder} is not a valid directory")
        return

    print(f"Looking for videos in: {input_folder}")
    
    capture_frames_from_folder(input_folder, output_folder)

if __name__ == "__main__":
    main()