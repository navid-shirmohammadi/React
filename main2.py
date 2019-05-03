import cv2
from cv2 import aruco
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
reach_target_distance = 20
ramp_distance = 50

# select camera
cap = cv2.VideoCapture(0)

gui_on = True

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
amplitude_save = 4
direction = 95
bias_angle = 15
freq = 5
frame = None
amplitude = amplitude_save

path = [(200, 200), (300, 200), (300, 300), (200, 300)]

# data we report
data = {'start time': datetime.now(), 'position': []}

# start timer
start = timer()

'''
--------------------------------
		   functions
--------------------------------
'''


def camera():  # TODO: use CameraVideoStream
	""" this function handle all camera related operations on one frame and return frame and time """
	_, frame = cap.read()  # read a frame
	corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)
	
	for corner in corners:
		coord1 = (int(corner[0, 0, 0]), int(corner[0, 0, 1]))
		coord2 = (int(corner[0, 1, 0]), int(corner[0, 1, 1]))
		coord3 = (int(corner[0, 2, 0]), int(corner[0, 2, 1]))
		coord4 = (int(corner[0, 3, 0]), int(corner[0, 3, 1]))
		
		if gui_on:
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


def control(fish_corners, target_):
	global ser, amplitude, direction, freq, bias_angle
	
	t = timer() - start
	
	if len(fish_corners):
		fish_corners = fish_corners
		
		pt0 = [(fish_corners[0][0] + fish_corners[2][0]) / 2,
			   (fish_corners[0][1] + fish_corners[2][1]) / 2]
	
	else:
		return
	
	pt1 = target_
	direction = (scipy.angle((pt0[0] - pt1[0]) + (pt0[1] - pt1[1]) * 1j, True) - 90) % 360
	
	# TODO: change angle curve from here
	angle = (direction + bias_angle * sin(freq*2*pi*t))  # sinusoid
	# angle = (direction + bias_angle * round(sin(freq*2*pi*t)))  # round
	# angle = (direction + bias_angle * -1**(sin(freq*2*pi*t) > 0))  # square
	# angle = (direction + bias_angle * (t % (1/freq) - 1/(2*freq))/(1/freq))  # linear

	x = amplitude * cos(angle * pi / 180)
	y = amplitude * sin(angle * pi / 180)
	
	poly_x = 114.8 * abs(x) ** 0.5157
	poly_y = 113.0 * abs(y) ** 0.5106
	
	if x < 0:
		poly_x = -poly_x
	if y < 0:
		poly_y = -poly_y
	
	command = str(int(poly_x)) + '^' + str(int(poly_y)) + '!'
	
	ser.write(bytes(command, 'ascii'))


'''
--------------------------------
			 main
--------------------------------
'''

if __name__ == '__main__':
	# enter editor
	frame, _, _ = camera()  # just get a frame for editor
	target = 0  # index of target robot has to reach
	start = datetime.now()
	number_of_frames = 0
	
	number_of_rounds = 12
	
	while True:
		frame, time, corners = camera()
		
		number_of_frames += 1
		
		if len(corners):
			corners = corners[0][0]
			c = [int(corners[0][0] + corners[1][0] + corners[2][0] + corners[3][0]),
				 int(corners[0][1] + corners[1][1] + corners[2][1] + corners[3][1])]
			data['position'].append([time, path[target], (int(c[0] / 4), int(c[1] / 4)), (amplitude, direction)])
		
		# high light target
		if gui_on:
			target_size = 10
			target_color = (40, 20, 220)
			
			cv2.line(frame, (path[target][0] - target_size, path[target][1]),
					 (path[target][0] + target_size, path[target][1]),
					 target_color, 2)
			cv2.line(frame, (path[target][0], path[target][1] - target_size),
					 (path[target][0], path[target][1] + target_size),
					 target_color, 2)
		
		if len(corners):
			current_position = (int((corners[0, 0] + corners[1, 0] + corners[2, 0] + corners[3, 0]) / 4),
								int((corners[0, 1] + corners[1, 1] + corners[2, 1] + corners[3, 1]) / 4))
			
			# draw a line from current position to target
			if gui_on:
				cv2.line(frame, (path[target][0], path[target][1]),
						 (int(current_position[0]), int(current_position[1])), (255, 255, 255), 2)
			
			distance_to_target = ((current_position[0]-path[target][0])**2+(current_position[1]-path[target][1])**2)**0.5
			
			# next target
			if distance_to_target < reach_target_distance:
				target += 1
			
			# ramp effect
			if distance_to_target < ramp_distance ** 2:
				amplitude = (distance_to_target/ramp_distance)*amplitude_save
			else:
				amplitude = amplitude_save
		
		# reached the last target
		if target == len(path):
			number_of_rounds -= 1
			print('number or rounds to go: ', number_of_rounds)
			target = 0
		
		key = cv2.waitKey(10) & 0xff
		
		if key == 27:
			break
		elif number_of_rounds == 0:
			break
		
		control(corners, path[target])
		
		# show frame
		cv2.imshow('experiment', frame)
	
	end = datetime.now()
	print('fps: ', number_of_frames / (end - start).microseconds * 10 ** 6)
	report()
	cap.release()
	cv2.destroyAllWindows()
