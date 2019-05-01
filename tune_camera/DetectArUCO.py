import datetime
import cv2
from cv2 import aruco


class DetectArUCO:
	def __init__(self):
		self.aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
		self.parameters = aruco.DetectorParameters_create()
	
	def detect(self, image):
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		cdf = cv2.equalizeHist(gray)
		corners, ids, rejectedImgPoints = aruco.detectMarkers(cdf, self.aruco_dict, parameters=self.parameters)
		return corners, datetime.datetime.now()
