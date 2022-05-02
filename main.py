import threading
import cv2
import os
import mediapipe as mp
import math
import sys

videotype = sys.argv[1]

counterval = 0
counterval2 = 2

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

def livekneepos(results, mp_pose, image_width,image_height,leg):
  if (leg == "r"):
    global counterval
    counterval += 1
    rightkneexypos = ((str(counterval)) + ',' + (str(f'{math.trunc(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE].x * image_height)}')))
    return rightkneexypos
  elif (leg == "l"):
    global counterval2
    counterval2 += 1
    leftkneexypos = ((str(counterval2)) + ',' + (str(f'{math.trunc(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].x * image_height)}')))
    return leftkneexypos
  else:
    print("No idea how you got here haha!")

def webcam():
    cap = cv2.VideoCapture('Video/'+videotype+'.mp4')
    with mp_pose.Pose(
        min_detection_confidence=0.8,
        min_tracking_confidence=0.8) as pose:
        while cap.isOpened():
            success, image = cap.read()

            if not success:
                # If loading a video, use 'break' instead of 'continue'.
                break

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            image_height, image_width, _ = image.shape

            if not results.pose_landmarks:
                continue

            rightleg = livekneepos(results, mp_pose, image_width, image_height,"r")
            leftleg = livekneepos(results, mp_pose, image_width, image_height, "l")

            with open("rightleg.csv", "a") as o:
                o.write(rightleg)
                o.write("\n")
            with open("leftleg.csv", "a") as o:
                o.write(leftleg)
                o.write("\n")

            #printlivedata(results, mp_pose, image_width, image_height)
            
            # Draw the pose annotation on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Pose', image) # Flip Image:     cv2.flip(image, 1)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cap.release()
    exiting()

def graph():
    os.system('python graph_with_intersection.py')

def exiting():
    os.remove("leftleg.csv")
    os.remove("rightleg.csv")
    steps = open('steps.txt','r').read().strip()
    os.remove("steps.txt")
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
