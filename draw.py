import cv2
from copy import deepcopy

window_name = 'path editor'
image = None
path = []
min_dist = 50


def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(path):
            if (x-path[-1][0])**2 + (y-path[-1][1])**2 < min_dist**2:
                return
        cv2.circle(image, (x, y), 4, (100, 15, 160), -1)
        if len(path):
            cv2.line(image, path[-1], (x, y), (160, 160, 15), 2)
        path.append((x, y))


def run(frame):
    global image, path
    image = deepcopy(frame)
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, draw_circle)

    while True:
        cv2.imshow(window_name, image)

        key = cv2.waitKey(20)

        if key == 27:
            cv2.destroyWindow(window_name)
            return path

        elif key == ord('r'):
            image = deepcopy(frame)
            path = []
