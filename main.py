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

lower_blue = np.array([110, 50, 50])
upper_blue = np.array([130, 255, 255])

lower_yellow = np.array([20, 50, 50])
upper_yellow = np.array([40, 255, 255])

hardware = {'x': {'initial_pwm': 100, 'pin': (12, 11)},
            'y': {'initial_pwm': 100, 'pin': (13, )}}

reach_target_distance = 10

path = []
cap = cv2.VideoCapture(0)
kernel = np.ones((9, 9), np.uint8)
data = {'start time': datetime.now(),
        'position': []}
start = timer()

'''
--------------------------------
           functions
--------------------------------
'''


def editor(frame):
    global path
    path = draw.run(frame)


def camera():
    if cap.isOpened():
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # define masks
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
        yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # filter noise
        opening_blue = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)
        opening_yellow = cv2.morphologyEx(yellow_mask, cv2.MORPH_OPEN, kernel)

        # get contours
        _, thresh_blue = cv2.threshold(opening_blue, 127, 255, 0)
        _, thresh_yellow = cv2.threshold(opening_yellow, 127, 255, 0)
        contours_blue, _ = cv2.findContours(thresh_blue, 1, 2)
        contours_yellow, _ = cv2.findContours(thresh_yellow, 1, 2)

        # draw contours
        try:
            (x_blue, y_blue), radius_blue = cv2.minEnclosingCircle(contours_blue[0])
            (x_yellow, y_yellow), radius_yellow = cv2.minEnclosingCircle(contours_yellow[0])
            center_blue = (int(x_blue), int(y_blue))
            center_yellow = (int(x_yellow), int(y_yellow))

            frame = cv2.circle(frame, center_blue, int(radius_blue), (0, 0, 255), 2)
            frame = cv2.circle(frame, center_yellow, int(radius_yellow), (0, 0, 255), 2)
            return frame, timer() - start, center_blue, center_yellow

        except IndexError:
            return frame, timer() - start, (-1, -1), (-1, -1)


def report():
    # report data
    with open('data.txt', 'a') as file:
        file.write('\n=========================\n')
        file.write(str(data['start time']))
        file.write('\n=========================\n')

        for item in data['position']:
            file.write(str(item)+'\n')
        file.close()


def control_unit(blue_center, yellow_center, target):
    pass


'''
--------------------------------
             main
--------------------------------
'''


if __name__ == '__main__':
    # enter editor
    frame, _, _, _ = camera()
    editor(frame)

    target = 0

    while True:
        frame, time, c_blue, c_yellow = camera()

        if c_blue != (-1, -1) and c_yellow != (-1, -1):
            data['position'].append([time, path[target], c_blue, c_yellow])

        c = ((c_blue[0] + c_yellow[0]) / 2,
             (c_blue[1] + c_yellow[1]) / 2)

        # high light target
        cv2.line(frame, (path[target][0] - 5, path[target][1]),
                        (path[target][0] + 5, path[target][1]),
                        (10, 240, 140), 2)
        cv2.line(frame, (path[target][0], path[target][1] - 5),
                        (path[target][0], path[target][1] + 5),
                        (10, 240, 140), 2)

        # show frame
        cv2.imshow('experiment', frame)

        # send date to control unite

        if (c[0]-path[target][0])**2 + (c[1]-path[target][1])**2 < reach_target_distance**2:
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
