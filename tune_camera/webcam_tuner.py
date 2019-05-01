import cv2
import pandas
import subprocess


from WebcamVideoStream import WebcamVideoStream
from DetectArUCO import DetectArUCO

# get list with: v4l2-ctl -d /dev/video0 --list-ctrls


class UpdateData:
	def __init__(self, update_after_n_frames):
		self.update_after_n_frames = update_after_n_frames
		self.current = 0
		self.detected = 0
		self.accuracy_record = []
		
	def increase_total(self):
		self.current += 1
		
	def increase_detected(self):
		self.detected += 1
		
	def cam_setting(self, cam_setting):
		self.setting = cam_setting
		
	def check(self, last_change):
		if self.current == self.update_after_n_frames:
			accuracy = self.detected / self.update_after_n_frames
			self.accuracy_record.append((cam_info, accuracy))
			
			if accuracy < self.accuracy_record[-2][1]:
				prev_setting = self.accuracy_record[-2][0]
				change_idx, change_vale = last_change
				if change_vale > 0:
					prev_setting[(change_idx+1) % 5] -= change_vale
		
			
	def __new_test(self, exposure, saturation, gain, contrast, brightness):
		self.current = 0
		self.detected = 0

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


vs = WebcamVideoStream(src=0).start()

if __name__ == '__main__':
	
	test_set = [range_set['exposure']['min'],
				range_set['saturation']['min'],
				range_set['gain']['min'],
				range_set['contrast']['min'],
				range_set['brightness']['min']]
	
	update_data = UpdateData(200)
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
