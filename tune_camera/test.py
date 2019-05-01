import cv2
import pandas
import subprocess

from WebcamVideoStream import WebcamVideoStream
from DetectArUCO import DetectArUCO


# get list with: v4l2-ctl -d /dev/video0 --list-ctrls


class UpdateData:
	def __init__(self, update_after_n_frames, namespace, range_limits):
		self.update_after_n_frames = update_after_n_frames
		self.current_frame = 0
		self.detected_aruco = 0
		self.accuracy_record = []
		self.cam_setting = None
		self.change_info = []
		self.namespace = namespace
		self.range_limits = range_limits
		
	def increase_total(self):
		self.current += 1
	
	def increase_detected(self):
		self.detected += 1
	
	def change_record(self, change_index, value):
		self.change_info = (change_index, value)
		
	def check(self):
		if self.current_frame == self.update_after_n_frames:  # end of current test
			accuracy = self.detected_aruco / self.update_after_n_frames
			
			if len(self.accuracy_record) == 0:  # first record
				self.accuracy_record.append((self.cam_setting, accuracy))  # record data before next test
			
			elif accuracy > self.accuracy_record[-1][1]:  # better result
				self.accuracy_record.append((self.cam_setting, accuracy))  # record data before next test
				
				idx, val = self.change_info
				var_name = self.namespace[idx]

				if self.range_limits[var_name]['max'] >= self.cam_setting[idx] + val >= self.range_limits[var_name]['min']:
					self.cam_setting[var_name] += val
				else:
					# go and change next setting
					self.change_info = (idx+1, 10)
				
			else:  # worse result
				idx, val = self.change_info
				
				if val > 0:
					val *= -1
				
				else:
					self.cam_setting = self.accuracy_record[-3][0]
					self.change_record((idx+1) % 5, )
				
				
	def __new_test(self, exposure, saturation, gain, contrast, brightness):
		self.current = 0
		self.detected = 0
		self.cam_setting = (exposure, saturation, gain, contrast, brightness)
		
		subprocess.check_call("v4l2-ctl -d /dev/video0 -c exposure_absolute={0}".format(exposure), shell=True)
		subprocess.check_call("v4l2-ctl -d /dev/video0 -c saturation={0}".format(saturation), shell=True)
		subprocess.check_call("v4l2-ctl -d /dev/video0 -c gain={0}".format(gain), shell=True)
		subprocess.check_call("v4l2-ctl -d /dev/video0 -c contrast={0}".format(contrast), shell=True)
		subprocess.check_call("v4l2-ctl -d /dev/video0 -c brightness={0}".format(brightness), shell=True)


dataFrame = pandas.DataFrame({'exposure': [],
							  'saturation': [],
							  'gain': [],
							  'contrast': [],
							  'brightness': [],
							  'accuracy': []})

# range of checking parameters: min max step --> depends on camera
range_set = {'exposure': {'min': 0, 'max': 100},
			 'saturation': {'min': 0, 'max': 100},
			 'gain': {'min': 0, 'max': 100},
			 'contrast': {'min': 0, 'max': 100},
			 'brightness': {'min': 0, 'max': 100}}

namespace = ['exposure', 'saturation', 'gain', 'contrast', 'brightness']

"""
vs = WebcamVideoStream(src=0).start()


if __name__ == '__main__':
	
	test_set = [range_set['exposure']['min'],
				range_set['saturation']['min'],
				range_set['gain']['min'],
				range_set['contrast']['min'],
				range_set['brightness']['min']]
	
	update_data = UpdateData(200, range_set)
	
	detect_aruco = DetectArUCO()
	
	while True:
		frame = vs.read()
		
		corners, time = detect_aruco.detect(frame)
		
		update_data.increase_total()
		if corners:
			update_data.increase_detected()
		
		update_data.check()
		
		key = cv2.waitKey(1) & 0xff
		
		if key == 27:
			break
		
		cv2.imshow('experiment', frame)
	
	vs.stop()
	cv2.destroyAllWindows()
"""
