import threading
import cv2
import os
import mediapipe as mp
import math
import sys
import enum


class LEGS(enum.Enum):
    LEFT = 0
    RIGHT = 1

# Global Constants
VIDEO_TYPE = sys.argv[1]
LEFTLEG_FILE = "leftleg.csv"
RIGHTLEG_FILE = "rightleg.csv"
STEPS_FILE = "steps.txt"

# Global Variables
counterval = 0
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

def printlivedata(results, mp_pose, image_width, image_height):
  print(
    f'Right Knee coordinates: ('
    f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE].x * image_width}, '
    f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE].y * image_height})'
    f'Left Knee coordinates: ('
    f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].x * image_width}, '
    f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].y * image_height})'
)

def livekneepos(results, mp_pose, image_width, image_height):
    global counter
    positions = dict()

    positions[LEGS.RIGHT] = ((str(counter)) + ',' + (str(
        f'{math.trunc(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE].x * image_height)}')))

    positions[LEGS.LEFT] = ((str(counter)) + ',' + (str(
        f'{math.trunc(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].x * image_height)}')))

    counter += 1
    return positions

def webcam():
    cap = cv2.VideoCapture('Video/'+VIDEO_TYPE+'.mp4')
    with mp_pose.Pose(
        min_detection_confidence=0.8,
        min_tracking_confidence=0.8) as pose:
        while cap.isOpened():
            success, image = cap.read()

            if not success:
                # If loading a video, use 'break' instead of 'continue'.
                break

            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            image_height, image_width, _ = image.shape

            if not results.pose_landmarks:
                continue

            knee_positions = livekneepos(
                results, mp_pose, image_width, image_height)

            with open(RIGHTLEG_FILE, "a") as o:
                o.write(knee_positions[LEGS.RIGHT])
                o.write("\n")
            with open(LEFTLEG_FILE, "a") as o:
                o.write(knee_positions[LEGS.LEFT])
                o.write("\n")

            # Draw the pose annotation on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Pose', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cap.release()
    exiting()

def graph():
    os.system('python graph_with_intersection.py')

def exiting():
    if os.path.isfile(LEFTLEG_FILE):
        os.remove(LEFTLEG_FILE)
    if os.path.isfile(RIGHTLEG_FILE):
        os.remove(RIGHTLEG_FILE)
    if os.path.isfile(STEPS_FILE):
        steps = open(STEPS_FILE, 'r').read().strip()
        os.remove(STEPS_FILE)

        multiline_string = (f"============================\n\n"
                            f"Total steps counted: {steps}\n\n"
                            f"============================")
        print(multiline_string)


if __name__ == '__main__': # Boilerplate
    try:
        sys.tracebacklimit = 0
        thread1 = threading.Thread(target=graph)
        thread1.start()
        thread2 = threading.Thread(target=webcam)
        thread2.start()
    except KeyboardInterrupt:
        sys.exit()