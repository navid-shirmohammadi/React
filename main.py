import cv2
import numpy as np
from timeit import default_timer as timer
from datetime import datetime

import draw

'''
--------------------------------
           setting
--------------------------------
'''
# setting range of blue color in hsv format
lower_blue = np.array([110, 50, 50])
upper_blue = np.array([130, 255, 255])
# setting range of purple color in hsv format
lower_purple = np.array([140, 50, 50])
upper_purple = np.array([160, 255, 255])

# the minimum distance of fish from target
reach_target_distance = 10

path = []  # path user selected for robot in editor
cap = cv2.VideoCapture(0)  # index of camera we use
kernel = np.ones((9, 9), np.uint8)  # kernel size for removing noise using morphologyEx

# data we report
data = {'start time': datetime.now(),
        'position': []}

start = timer()  # start timer

'''
--------------------------------
           functions
--------------------------------
'''


def editor(frame):
    """ this function get first frame of camera and let the user draw path for robot to go """
    global path
    path = draw.run(frame)


def camera():
    """ this function handle all camera related operations on one frame and return frame and time """
    if cap.isOpened():
        _, frame = cap.read()  # read a frame
        frame = cv2.flip(frame, 1)  # flip the frame vertically
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # change color space from BGR to HSV

        # define masks
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
        purple_mask = cv2.inRange(hsv, lower_purple, upper_purple)

        # filter noise
        opening_blue = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)
        opening_purple = cv2.morphologyEx(purple_mask, cv2.MORPH_OPEN, kernel)

        # thresh hold the image
        _, thresh_blue = cv2.threshold(opening_blue, 127, 255, 0)
        _, thresh_purple = cv2.threshold(opening_purple, 127, 255, 0)

        # get contours
        contours_blue, _ = cv2.findContours(thresh_blue, 1, 2)
        contours_purple, _ = cv2.findContours(thresh_purple, 1, 2)

        # draw contours
        try:
            (x_blue, y_blue), radius_blue = cv2.minEnclosingCircle(contours_blue[0])
            (x_purple, y_purple), radius_purple = cv2.minEnclosingCircle(contours_purple[0])
            center_blue = (int(x_blue), int(y_blue))
            center_purple = (int(x_purple), int(y_purple))

            frame = cv2.circle(frame, center_blue, int(radius_blue), (0, 0, 255), 2)
            frame = cv2.circle(frame, center_purple, int(radius_purple), (0, 0, 255), 2)
            return frame, timer() - start, center_blue, center_purple

        except IndexError:
            # if not found position of both circles return -1,-1 as center of them
            return frame, timer() - start, (-1, -1), (-1, -1)


def report():
    # report data
    with open('data.txt', 'a') as file:
        file.write('\n=========================\n')
        file.write(str(data['start time']))
        file.write('\n=========================\n')

        for item in data['position']:
            file.write(str(item) + '\n')
        file.close()


def control_unit(blue_center, purple_center, target):
    pass


'''
--------------------------------
             main
--------------------------------
'''

if __name__ == '__main__':
    # enter editor
    frame, _, _, _ = camera()  # just get a frame for editor
    editor(frame)

    target = 0  # index of target robot has to reach

    FPS = []  # use this list to calculate frame per second of camera

    while True:
        frame, time, c_blue, c_purple = camera()

        if c_blue != (-1, -1) and c_purple != (-1, -1):
            data['position'].append([time, path[target], c_blue, c_purple])

        # calculate FPS
        FPS.append(time)
        if len(FPS) > 10:
            FPS = FPS[-10:]
            print(10 / (FPS[-1] - FPS[-10]))

        # calculate the position of robot as center of both circles
        c = ((c_blue[0] + c_purple[0]) / 2,
             (c_blue[1] + c_purple[1]) / 2)

        # high light target
        target_size = 10
        target_color = (40, 20, 220)

        cv2.line(frame, (path[target][0] - target_size, path[target][1]),
                 (path[target][0] + target_size, path[target][1]),
                 target_color, 2)
        cv2.line(frame, (path[target][0], path[target][1] - target_size),
                 (path[target][0], path[target][1] + target_size),
                 target_color, 2)

        # draw a line from current position to target
        if c != (-1, -1):
            cv2.line(frame, (path[target][0], path[target][1]),
                     (int(c[0]), int(c[1])), (255, 255, 255), 2)

        # show frame
        cv2.imshow('experiment', frame)

        # send date to control unite

        if (c[0] - path[target][0]) ** 2 + (c[1] - path[target][1]) ** 2 < reach_target_distance ** 2:
            target += 1

            # reached the last target
            if target == len(path):
                break

        key = cv2.waitKey(20) & 0xff
        if key == 27:
            break

    report()
    cap.release()
    cv2.destroyAllWindows()
