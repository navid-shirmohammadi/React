import cv2
from cv2 import aruco
import draw
from numpy import sin, cos

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
amplitude = 0
angle = 0

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


def control(command):
	global ser, amplitude, angle

	if command == ord('w'):
		amplitude += 0.1
	elif command == ord('s'):
		amplitude -= 0.1
	elif command == ord('d'):
		angle += 5
	elif command == ord('a'):
		angle -= 5
	elif command == ord(' '):
		angle = 0
		amplitude = 0
	else:
		return

	x = amplitude * cos(int(angle) * 3.1415 / 180)
	y = amplitude * sin(int(angle) * 3.1415 / 180)

	poly_x = 114.8 * abs(x) ** 0.5157
	poly_y = 114.8 * abs(y) ** 0.5157

	if x < 0:
		poly_x = -poly_x
	if y < 0:
		poly_y = -poly_y

	COMMAND = str(int(poly_x)) + '^' + str(int(poly_y)) + '!'

	print('ang: ', angle, ' amp: ', amplitude)
	print(COMMAND)

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

	# FPS = []  # use this list to calculate frame per second of camera

	while True:
		frame, time, corners = camera()

		if len(corners):
			data['position'].append([time, path[target], corners, (amplitude, angle)])

		# calculate FPS
		"""
		FPS.append(time)
		if len(FPS) > 10:
			FPS = FPS[-10:]
			print(10 / (FPS[-1] - FPS[-10]))
		"""
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

		# show frame
		cv2.imshow('experiment', frame)

		key = cv2.waitKey(10) & 0xff

		if key == 27:
			break
		else:
			control(key)

	report()
	cap.release()
	cv2.destroyAllWindows()
