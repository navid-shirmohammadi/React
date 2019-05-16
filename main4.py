import cv2
from numpy import sin, cos, pi, arcsin, sign
from numpy import sum as nsum
import scipy
from cv2 import aruco
from time import sleep
from timeit import default_timer as timer
from datetime import datetime
import serial

from thread_test.WebcamVideoStream import WebcamVideoStream



aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters_create()

'''
--------------------------------
		variables
--------------------------------
'''
# the minimum distance of fish from target
reach_target_distance = 20
ramp_distance = 50

'''
--------------------------------
		   init
--------------------------------
'''
ser = serial.Serial('COM4', 9600, timeout=0, rtscts=1)

# I used this vars for control function
amplitude = 2
direction = 90
bias_angle = 15
freq = 3
freq_save = freq

frame = None

# tracker
tracker_type = 'KCF'
tracker = cv2.TrackerCSRT_create()

ROI_coord = None
# path user selected for robot in editor
a = 200
b = 150
w = 250
path = [(a, b), (a+w, b), (a+w, b+w), (a, b+w)]
path = 4*path
print(path)
# data we report
data = {'start time': datetime.now(), 'position': []}

# start timer
start = timer()

vs = WebcamVideoStream(src=0).start()

'''
--------------------------------
		   functions
--------------------------------
'''



def report():
	# report data
	with open('data.txt', 'w') as file:
		for item in data['position']:
			file.write(str(item) + '\n')
		file.close()



def control(target_):
	global ser, amplitude, direction, freq, bias_angle, angle_backup, frame, ROI_coord
	
	t = timer() - start
	pt0 = ROI_coord
	pt1 = target_
	
	data['position'].append((pt0, pt1, t))
	
	direction = (scipy.angle((pt0[0] - pt1[0]) + (pt0[1] - pt1[1]) * 1j, True) - 90) % 360
	
	# angle = (direction + bias_angle * sin(freq * 2 * pi * t))  # sinusoid
	# angle = (direction + bias_angle * round(sin(freq*2*pi*t)))  # round
	# angle = (direction + bias_angle * sign(sin(freq*2*pi*t)))  # square
	angle = (direction + bias_angle * arcsin(sin(2*pi*freq*t)))  # triangle
	
	x = amplitude * cos(angle * pi / 180)
	y = amplitude * sin(angle * pi / 180)
	
	poly_x = 114.8 * abs(x) ** 0.5157
	poly_y = 113.0 * abs(y) ** 0.5106
	
	if x < 0:
		poly_x = -poly_x
	if y < 0:
		poly_y = -poly_y
	
	scale = 1
	cv2.line(frame, (int(pt0[0]), int(pt0[1])), (int(pt0[0] + scale * poly_x), int(pt0[1] + scale * poly_y)),
			 (0, 200, 100), 2)
	
	command = str(int(poly_x)) + '^' + str(int(poly_y)) + '!'
	
	ser.write(bytes(command, 'ascii'))


'''
--------------------------------
			 main
--------------------------------
'''
vs.stop()
cap = cv2.VideoCapture(0)

if __name__ == '__main__':
	# enter editor
	_, frame = cap.read()  # just get a frame for editor
	
	# ROI
	bbox = cv2.selectROI(frame, False)
	ok = tracker.init(frame, bbox)
	
	target = 0  # index of target robot has to reach
	
	FPS = []  # use this list to calculate frame per second of camera
	s = datetime.now()
	while True:
		_, frame = cap.read()
		
		ok, bbox = tracker.update(frame)
		
		# high light target
		target_size = 10
		target_color = (40, 20, 220)
		
		cv2.line(frame, (path[target][0] - target_size, path[target][1]),
				 (path[target][0] + target_size, path[target][1]),
				 target_color, 2)
		cv2.line(frame, (path[target][0], path[target][1] - target_size),
				 (path[target][0], path[target][1] + target_size),
				 target_color, 2)
		
		
		if ok:
			p1 = (int(bbox[0]), int(bbox[1]))
			p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
			
			ROI_coord = (int((p1[0] + p2[0]) / 2), int((p1[1] + p2[1]) / 2))
			
			cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
			
			distance_to_target = ((ROI_coord[0]-path[target][0])**2+(ROI_coord[1]-path[target][1])**2)**0.5
			if distance_to_target < reach_target_distance:
				target += 1
				# reached the last target
				if target == len(path):
					break
			
			if distance_to_target < ramp_distance:
				freq = (distance_to_target / ramp_distance) * freq_save

			else:
				freq = freq_save
			
			
		else:
			cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
			sleep(1)
	
		cv2.putText(frame, tracker_type + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
		
		key = cv2.waitKey(10) & 0xff
		
		
		corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)
		coord = []
		if len(corners):
			for corner in corners:
				coord.append((int(corner[0, 0, 0]), int(corner[0, 0, 1])))
				coord.append((int(corner[0, 1, 0]), int(corner[0, 1, 1])))
				coord.append((int(corner[0, 2, 0]), int(corner[0, 2, 1])))
				coord.append((int(corner[0, 3, 0]), int(corner[0, 3, 1])))
			center = nsum(coord, 0)
			center = (int(center[0]/4), int(center[1]/4))
			width_2 = 50
			bbox = (center[0]-width_2, center[1]-width_2, width_2*2, width_2*2)
			tracker_type = 'KCF'
			tracker = cv2.TrackerCSRT_create()
			tracker.init(frame, bbox)
			
		if key == ord('w'):
			sleep(1)
			
		if key == 27:
			break
		else:
			control(path[target])
		
		# show frame
		cv2.imshow('experiment', frame)
	
	print((datetime.now()-s).microseconds*10**-6)
	cap.release()
	report()
	vs.stop()
	cv2.destroyAllWindows()
