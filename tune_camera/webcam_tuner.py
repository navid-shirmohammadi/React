
import subprocess
from threading import Thread
import cv2
from cv2 import aruco


# get list with: v4l2-ctl -d /dev/video0 --list-ctrls


class DetectArUCO:
	"""
	this class detect ArUCO on a given frame
	"""
	
	def __init__(self):
		self.aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
		self.parameters = aruco.DetectorParameters_create()
	
	def detect(self, image):
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		cdf = cv2.equalizeHist(gray)
		corners, ids, rejected_img_points = aruco.detectMarkers(cdf, self.aruco_dict, parameters=self.parameters)
		return corners


class WebcamVideoStream:
	"""
	objects of this class read frame from camera using separate thread from mai code
	"""
	
	def __init__(self, src=0):
		self.stream = cv2.VideoCapture(src)
		(self.grabbed, self.frame) = self.stream.read()
		self.stopped = False
		self.thread = None
	
	def start(self):
		Thread(target=self.update, args=()).start()
		return self
	
	def update(self):
		while True:
			if self.stopped:
				self.stream.release()
				return
			
			(self.grabbed, self.frame) = self.stream.read()
	
	def read(self):
		return self.frame
	
	def stop(self):
		self.stopped = True


class TestCase:
	"""
	this class measure accuracy of one test case from given camera setting
	"""
	
	def __init__(self, update_after_n_frames):
		self.update_after_n_frames = update_after_n_frames
		self.current = 0
		self.detected = 0
		self.detected_aruco = DetectArUCO()
	
	
	def update(self, frame):
		if self.current == self.update_after_n_frames:
			accuracy = self.detected / self.update_after_n_frames
			self.current = 0
			self.detected = 0
			return accuracy
		
		else:
			self.current += 1
			corners = self.detected_aruco.detect(frame)
			if len(corners):
				self.detected += 1
			return None
	
	
range_set = {'exposure': {'min': 0, 'max': 100, 'step': None},
				'saturation': {'min': 0, 'max': 100, 'step': None},
				'gain': {'min': 0, 'max': 100, 'step': None},
				'contrast': {'min': 0, 'max': 100, 'step': None},
			 	'brightness': {'min': 0, 'max': 100, 'step': None}}

gain = range_set['gain']['min']
contrast = range_set['contrast']['min']
exposure = range_set['exposure']['min']
brightness = range_set['brightness']['min']
saturation = range_set['saturation']['min']

range_set['gain']['step'] = int((range_set['gain']['max']-range_set['gain']['min'])/10)
range_set['contrast']['step'] = int((range_set['contrast']['max']-range_set['contrast']['min'])/10)
range_set['exposure']['step'] = int((range_set['exposure']['max']-range_set['exposure']['min'])/10)
range_set['brightness']['step'] = int((range_set['brightness']['max']-range_set['brightness']['min'])/10)
range_set['saturation']['step'] = int((range_set['saturation']['max']-range_set['saturation']['min'])/10)

order_ = ('gain', 'contrast', 'exposure', 'brightness', 'saturation')
setting = {'gain': gain, 'contrast': contrast, 'exposure': exposure, 'brightness': brightness, 'saturation': saturation}

update_setting = True
found_best_setting = False

vs = WebcamVideoStream(0).start()
t = TestCase(100)

index_ = 0
on_peek = 0
prev_acc = 0.0
go_forward = True

acc_array = []


while not found_best_setting:
	
	if on_peek == 5:
		print(acc_array)
		break
		
	if update_setting:
		print(acc_array)
		print("next test case")
		# TODO: reset motor here
		# subprocess.check_call("v4l2-ctl -d /dev/video0 -c gain={0}".format(setting['gain']), shell=True)
		# subprocess.check_call("v4l2-ctl -d /dev/video0 -c contrast={0}".format(setting['contrast']), shell=True)
		# subprocess.check_call("v4l2-ctl -d /dev/video0 -c saturation={0}".format(setting['saturation']), shell=True)
		# subprocess.check_call("v4l2-ctl -d /dev/video0 -c brightness={0}".format(setting['brightness']), shell=True)
		# subprocess.check_call("v4l2-ctl -d /dev/video0 -c exposure_absolute={0}".format(setting['exposure']), shell=True)
		
		update_setting = False
		
	frame = vs.read()
	acc = t.update(frame)
	cv2.imshow('frame', frame)
	
	if acc is not None:
		update_setting = True
		d = {'accuracy': 100*acc}
		d.update(setting)
		acc_array.append(d)
		
		variable_name = order_[index_]
		step = range_set[variable_name]['step']
		current_value = setting[variable_name]
		
		if acc > prev_acc:
			on_peek = 0
			if go_forward:
				pass
			else:
				step *= -1
				
		else:
			if go_forward:
				step *= -1
				go_forward = False
			else:
				on_peek += 1
				go_forward = True
				index_ = (index_ + 1) % len(order_)
				
		if go_forward:
			if current_value + step < range_set[variable_name]['max']:
				setting[variable_name] = current_value + step
			else:
				index_ = (index_ + 1) % len(order_)
		
		else:
			if current_value + step > range_set[variable_name]['min']:
				setting[variable_name] = current_value + step
			else:
				index_ = (index_ + 1) % len(order_)

		prev_acc = acc
		
	key = cv2.waitKey(1)
	if key == ord('q'):
		break


vs.stop()
cv2.destroyAllWindows()
