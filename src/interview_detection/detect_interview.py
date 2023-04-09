import os
import sys
import time

from pprint import pprint

import ffmpeg

import cv2
import mediapipe as mp


NUM_CONT_DETECTS = 10


def get_video_metadata(media_file_path):
    # uses ffprobe command to extract all possible metadata from the media file
    metadata = ffmpeg.probe(media_file_path)["streams"]

    # print()
    # print("type(metadata):\t", type(metadata))
    # print("metadata")
    # pprint(metadata[0])

    duration = int(float(metadata[0].get("duration", 0)))
    num_frames = int(metadata[0].get("nb_frames", 0))
    frame_rate = int(eval(metadata[0].get("avg_frame_rate", 0)))

    return duration, num_frames, frame_rate


def convert_seconds_to_time(seconds):
    return time.strftime("%H:%M:%S", time.gmtime(seconds))


class InterviewDetector():
    def __init__(self, min_confidence=0.5):
        self.start = 0
        self.end = 0
        self.n_cont_detects = 0
        self.mp_draw = mp.solutions.drawing_utils
        self.face_detector = mp.solutions.face_detection.FaceDetection(
            min_confidence)

    def find_faces(self, img, frame_num, draw=True):
        global NUM_CONT_DETECTS
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.face_detector.process(img_rgb)
        # print(self.results)

        bboxs = []
        if self.results.detections:
            self.n_cont_detects += 1
            if (not self.start) and self.n_cont_detects > NUM_CONT_DETECTS:
                self.start = frame_num
            else:
                self.end = frame_num
            for id, detection in enumerate(self.results.detections):
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = img.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                    int(bboxC.width * iw), int(bboxC.height * ih)
                bboxs.append([id, bbox, detection.score])
                if draw:
                    img = self.fancy_draw(img, bbox)
                    cv2.putText(img, f'{int(detection.score[0] * 100)}%',
                                (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,
                                2, (255, 0, 255), 2)
        return img, bboxs

    def fancy_draw(self, img, bbox, l=30, t=5, rt=1):
        x, y, w, h = bbox
        x1, y1 = x + w, y + h
        color = (255, 0, 255)

        cv2.rectangle(img, bbox, color, rt)
        # Top Left  x,y
        cv2.line(img, (x, y), (x + l, y), color, t)
        cv2.line(img, (x, y), (x, y + l), color, t)
        # Top Right  x1,y
        cv2.line(img, (x1, y), (x1 - l, y), color, t)
        cv2.line(img, (x1, y), (x1, y + l), color, t)
        # Bottom Left  x,y1
        cv2.line(img, (x, y1), (x + l, y1), color, t)
        cv2.line(img, (x, y1), (x, y1 - l), color, t)
        # Bottom Right  x1,y1
        cv2.line(img, (x1, y1), (x1 - l, y1), color, t)
        cv2.line(img, (x1, y1), (x1, y1 - l), color, t)
        return img


def main():
    # read the audio/video file from the command line arguments
    video_path = sys.argv[1]
    print()
    print('*' * 50)
    print("video_path:\t", video_path)

    # get metadata of the video
    duration, num_frames, frame_rate = get_video_metadata(video_path)
    print()
    print("Duration:\t", convert_seconds_to_time(duration))
    # print("# frames:\t", num_frames)
    print("Frame rate:\t", frame_rate)

    # process frame-by-frame
    cap = cv2.VideoCapture(video_path)
    p_time = 0
    frame_counter = 0

    detector = InterviewDetector()

    while True:
        success, img = cap.read()
        if not success:
            break
        img, bboxs = detector.find_faces(img, frame_counter)
        # print(bboxs)

        frame_counter += 1
        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time
        cv2.putText(img, f'FPS: {int(fps)}', (20, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

    print()
    # print("frame_counter:\t", frame_counter)
    # print("Start frame #:\t", START)
    # print("End frame #:\t", END)
    print("Interview start time (s):\t", convert_seconds_to_time(
        int(detector.start / frame_rate)))
    print("Interview end time (s):\t\t", convert_seconds_to_time(
        int(detector.end / frame_rate)))


if __name__ == "__main__":
    main()
