
# Hardcoded RTSP stream URL --- REPLACE WITH YOUR RTSP URL
# rtsp_stream_url = rtsp://admin:admin123@172.15.121.50:554/cam/realmonitor?channel=1&subtype=0

import cv2
import os
import time
from datetime import datetime, timedelta
from threading import Thread

class RTSPRecorder:
    def __init__(self, rtsp_url, output_folder, segment_time=300):
        self.rtsp_url = rtsp_url
        self.output_folder = output_folder
        self.segment_time = segment_time
        self.fps = 25.0
        self.frame_width = 640
        self.frame_height = 480
        self.cap = None
        self.frames = []
        self.frame_count = 0
        self.last_notification_time = time.time()
        self.segment_start_time = datetime.now()

    def setup(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        self.cap = cv2.VideoCapture(self.rtsp_url)
        if not self.cap.isOpened():
            print("Error: Unable to open RTSP stream")
            return False

        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or self.fps
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or self.frame_width
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or self.frame_height

        print(f"Stream resolution: {self.frame_width}x{self.frame_height}")
        return True

    def generate_filename(self, start_time, end_time):
        start_str = start_time.strftime("%Y%m%d_%H%M%S")
        end_str = end_time.strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.output_folder, f"{start_str}_to_{end_str}.mp4")

    def save_video(self, frames, filename):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(filename, fourcc, self.fps, (self.frame_width, self.frame_height))
        for frame in frames:
            out.write(frame)
        out.release()

    def record(self):
        if not self.setup():
            return

        frames_per_segment = int(self.fps * self.segment_time)

        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("Error: Failed to read frame from stream")
                    break

                self.frames.append(frame)
                self.frame_count += 1

                current_time = time.time()
                if current_time - self.last_notification_time >= 60:
                    print(f"Recording... {time.strftime('%Y-%m-%d %H:%M:%S')}")
                    self.last_notification_time = current_time

                if self.frame_count >= frames_per_segment:
                    segment_end_time = datetime.now()
                    output_filename = self.generate_filename(self.segment_start_time, segment_end_time)

                    Thread(target=self.save_video, args=(self.frames, output_filename)).start()

                    self.segment_start_time = datetime.now()
                    self.frames = []
                    self.frame_count = 0
        except KeyboardInterrupt:
            print("\nRecording interrupted by user.")
        finally:
            self.cleanup()

    def cleanup(self):
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("Recording stopped.")

if __name__ == "__main__":
    # rtsp_stream_url = input("Enter the RTSP stream URL: ")
    # output_folder = input("Enter the folder to save videos: ")

    rtsp_stream_url = "rtsp://admin:admin123@172.15.121.50:554/cam/realmonitor?channel=1&subtype=0"
    output_folder = "output"
    recorder = RTSPRecorder(rtsp_stream_url, output_folder)
    recorder.record()

    input("Press Enter to exit...")