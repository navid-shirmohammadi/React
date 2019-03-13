import cv2
from cv2 import aruco
import draw
from numpy import sin, cos, pi
import scipy

from timeit import default_timer as timer
from datetime import datetime

import serial

'''
--------------------------------
		variables
--------------------------------
'''
# the minimum distance of fish from target
reach_target_distance = 10

# select camera
cap = cv2.VideoCapture(0)

'''
--------------------------------
		   init
--------------------------------
'''
ser = serial.Serial('COM4', 9600, timeout=0, rtscts=1)

# load aruco dict
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters_create()

# I used this vars for control function
amplitude = 0.05
direction = 95
bias_angle = 20
freq = 0.5
frame = None

# path user selected for robot in editor
path = []

# data we report
data = {'start time': datetime.now(), 'position': []}

# start timer
start = timer()

'''
--------------------------------
		   functions
--------------------------------
'''


def editor(image):
	""" this function get first frame of camera and let the user draw path for robot to go """
	global path
	path = draw.run(image)


def camera():
	""" this function handle all camera related operations on one frame and return frame and time """
	if cap.isOpened():
		_, frame = cap.read()  # read a frame
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		cdf = cv2.equalizeHist(gray)
		corners, ids, rejectedImgPoints = aruco.detectMarkers(cdf, aruco_dict, parameters=parameters)

		for corner in corners:
			coord1 = (int(corner[0, 0, 0]), int(corner[0, 0, 1]))
			coord2 = (int(corner[0, 1, 0]), int(corner[0, 1, 1]))
			coord3 = (int(corner[0, 2, 0]), int(corner[0, 2, 1]))
			coord4 = (int(corner[0, 3, 0]), int(corner[0, 3, 1]))
			cv2.line(frame, coord1, coord2, (0, 0, 255), 3)
			cv2.line(frame, coord1, coord4, (255, 0, 0), 3)

		return frame, timer() - start, corners


def report():
	# report data
	with open('data.txt', 'a') as file:
		file.write('\n=========================\n')
		file.write(str(data['start time']))
		file.write('\n=========================\n')

		for item in data['position']:
			file.write(str(item) + '\n')
		file.close()


angle_backup = 0


def control(fish_corners, target_):
	global ser, amplitude, direction, freq, bias_angle, angle_backup, frame

	t = timer() - start

	angle = angle_backup
	pt = None
	if fish_corners:
		fish_corners = fish_corners[0][0]

		pt0 = [(fish_corners[0][0] + fish_corners[2][0]) / 2,
			   (fish_corners[0][1] + fish_corners[2][1]) / 2]
		pt = pt0
		pt1 = target_
		
		direction = (scipy.angle((pt0[0] - pt1[0]) + (pt0[1] - pt1[1]) * 1j, True) - 90) % 360

		angle = (direction + bias_angle * sin(freq * 2 * pi * t))
		angle_backup = angle

	x = amplitude * cos(angle * pi / 180)
	y = amplitude * sin(angle * pi / 180)

	poly_x = 114.8 * abs(x) ** 0.5157
	poly_y = 114.8 * abs(y) ** 0.5157

	if x < 0:
		poly_x = -poly_x
	if y < 0:
		poly_y = -poly_y
	
	scale = 1
	if pt:
		cv2.line(frame, (int(pt[0]), int(pt[1])), (int(pt[0]+scale*poly_x), int(pt[1]+scale*poly_y)), (0, 200, 100), 2)

	COMMAND = str(int(poly_x)) + '^' + str(int(poly_y)) + '!'

	ser.write(bytes(COMMAND, 'ascii'))


'''
--------------------------------
			 main
--------------------------------
'''

if __name__ == '__main__':
	# enter editor
	frame, _, _ = camera()  # just get a frame for editor
	editor(frame)

	target = 0  # index of target robot has to reach

	FPS = []  # use this list to calculate frame per second of camera

	while True:
		frame, time, corners = camera()

		if len(corners):
			data['position'].append([time, path[target], corners, (amplitude, direction)])

		# calculate FPS
		
		FPS.append(time)
		if len(FPS) > 10:
			FPS = FPS[-10:]
			print(10 / (FPS[-1] - FPS[-10]))
		
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
		if corners:
			corner = corners[0]
			current_position = (int((corner[0, 0, 0] + corner[0, 1, 0] + corner[0, 2, 0] + corner[0, 3, 0]) / 4),
								int((corner[0, 0, 1] + corner[0, 1, 1] + corner[0, 2, 1] + corner[0, 3, 1]) / 4))

			cv2.line(frame, (path[target][0], path[target][1]),
					 (int(current_position[0]), int(current_position[1])), (255, 255, 255), 2)

			# send date to control unite

			if (current_position[0] - path[target][0]) ** 2 + \
				(current_position[1] - path[target][1]) ** 2 < reach_target_distance ** 2:
				target += 1

				# reached the last target
				if target == len(path):
					break


		key = cv2.waitKey(10) & 0xff

		if key == 27:
			break
		else:
			control(corners, path[target])
			
		# show frame
		cv2.imshow('experiment', frame)
	
	report()
	cap.release()
	cv2.destroyAllWindows()
