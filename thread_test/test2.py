import datetime
import cv2

from DetectArUCO import DetectArUCO
from WebcamVideoStream import WebcamVideoStream


vs = WebcamVideoStream(src=0).start()
start = datetime.datetime.now()

numFrames = 0
save = []
while numFrames < 300:
	frame = vs.read()
	pos_detect = DetectArUCO(frame)
	position, t = pos_detect.detect()
	
	
	save.append(position)
	numFrames += 1

end = datetime.datetime.now()
elapsed = (end - start).total_seconds()
fps = numFrames/elapsed

print("[INFO] elasped time: {:.2f}".format(elapsed))
print("[INFO] approx. FPS: {:.2f}".format(fps))
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
