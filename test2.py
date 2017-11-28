import sys
sys.path.append('../../pupil/pupil_src/shared_modules/')
from camera_models import *
from operator import itemgetter, attrgetter, methodcaller
import numpy as np
import math
#from darkflow.net.build import TFNet
import cv2
# import scipy
# from scipy import misc
# from scipy.misc import imresize
from PupilData import *

# options = {"model": "cfg/tiny-yolo.cfg", "load": "weights/tiny-yolo.weights", "demo": 'camera', "threshold": 0.12}

# tfnet = TFNet(options)

dist_coefs = np.array(pre_recorded_calibrations['Pupil Cam1 ID2']['(1280, 720)']['dist_coefs'])
camera_matrix = np.array(pre_recorded_calibrations['Pupil Cam1 ID2']['(1280, 720)']['camera_matrix'])
cam = cv2.VideoCapture(-1)
# cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while(True):
	#m = getGazeData()
	__, frame = cam.read()

	#undistorted_frame = cv2.undistort(frame, camera_matrix, dist_coefs)
	# if ret==False:
	# 	print("frame is empty")
	#cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
	# frame = cv2.resize(frame, (0,0), fx=.5, fy=.5)
	#frame = scipy.misc.imresize(frame, .7)
	cv2.imshow('frame',frame)
	#cv2.imshow('undistorted frame', undistorted_frame)
	# gazeX = (m['gaze_coord'][0])*1920*.7
	# gaze_x = gazeX
	# gazeY = (1-m['gaze_coord'][1])*1080*.7

	# print('m[gaze_coord][0]', m['gaze_coord'][0])
	
	# if m['confidence']>.8 :
	# 	print(gazeX, gazeY, ' confidence:', m['confidence'])

	#frame = cv2.circle(frame, (int(gazeX), int(gazeY)), 20, (255,0,0), -1)
	cv2.imshow('frame',frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cam.release()
# print(tfnet.FLAGS)

# boxesInfo = list()

# boxesInfo.append([
#             'person', .9]
#         )

# boxesInfo.append([
#             'dog', .5]
#         )

# print (boxesInfo[0][0])


# s = str(2) + '\n'

# print(s)

# print(str(sorted(boxesInfo, key=itemgetter(1),  reverse=True)))
# print(sorted(boxesInfo, key=itemgetter(1),  reverse=True))

#print(math.sqrt(4))
