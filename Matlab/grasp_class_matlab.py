#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# File: 	graspClass.py
#
# Purpose:  Integrate Pupil Labs eye-tracking headset with object detection and classification to perceive not only 
#			the objects in the camera's FOV, but what object the user is fixated upon.  
#        	Here,I use a neural network (darkflow, a tensorflow implementation of YOLO) that is pre-trained on 
#			household objects (using the COCO dataset).
#			Upon running this script, a streaming video from the Pupil world camera appears and bounding boxes will be drawn 
#			around objects that are detected and classified (above a certain confidence threshold). 
#			The green box is the detected object closest to the user's gaze, while all other blue bounding boxes are 
#			remaining detected objects in the FOV. 
#			
# 			Note: calibrate the Pupil labs headset in resolution 1280x720 before running graspClass.py in a terminal window.
# 			 		   
#
# Author: Jesse Weisberg, 6/13/17
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import sys
sys.path.append('../../pupil/pupil_src/shared_modules/')
from camera_models import *
from darkflow.net.build import TFNet
import numpy as np
import cv2
from operator import itemgetter, attrgetter, methodcaller
import math
import scipy
from scipy import misc
from scipy.misc import imresize
from PupilData import *

# Run on yolo trained on COCO dataset (COCO is a dataset comprised of common household objects)
#options = {"model": "cfg/yolo.cfg", "load": "weights/yolo.weights", "demo": 'camera', "threshold": 0.2}

# Run on tiny yolo (for ultimate speed)
options = {"model": "cfg/tiny-yolo.cfg", "load": "weights/tiny-yolo.weights", "threshold": 0.2}
tfnet = TFNet(options)

# Predetermined radial distortion coefficients and intrinsic camera parameters for undistorting later on.
dist_coefs = np.array(pre_recorded_calibrations['Pupil Cam1 ID2']['(1280, 720)']['dist_coefs'])
camera_matrix = np.array(pre_recorded_calibrations['Pupil Cam1 ID2']['(1280, 720)']['camera_matrix'])

frame_width = 1280
frame_height = 720
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

while(True):
	
	## Used for writing file to matlab
	#file = open('classFile.txt','a')

	# Capture frame by frame
	_, frame = cam.read()

	# Perform radial undistortion (Pupil world camera has significant radial distortion which adversely affects detection/classification).
	frame = cv2.undistort(frame, camera_matrix, dist_coefs)
	cv2.imshow('Object Detection',frame)
	
	# Uses neural network (darkflow) to predict detected objects and respective classifications. 
	objects_detected = tfnet.return_predict2(frame)
	#print(objects_detected)

	# Collect normalized gaze_data, denormalize according to camera resolution (bottom-left corner is (0,0), top-right is (1,1)).
	gaze_data = getGazeData()
	gaze_x = (gaze_data['gaze_coord'][0])*frame_width
	gaze_y = (1-gaze_data['gaze_coord'][1])*frame_height  # Y-coordinate was flipped initially

	# if gaze_data['confidence']>.7:
		# print(gazeX, gazeY, ' confidence:', gaze_data['confidence'])

	# Append gaze point to real-time stream as a green dot.
	frame = cv2.circle(frame, (int(gaze_x), int(gaze_y)), 10, (0,255,0), -1)
	cv2.imshow('Object Detection',frame)

	if objects_detected:
		# Weed out irrelevant bounding boxes (ones that aren't close to your gaze)
		# Calculate 'radius' of each bounding box - if the gaze point is outside of this radius, don't show the box
		for obj in objects_detected:
			radius = math.hypot(obj[2][1] - obj[2][0], obj[3][1] - obj[3][0])
			if radius > obj[4]:
				obj.append(radius) 
			else:
				objects_detected.remove(obj)

		#file = open('classFile.txt','w') 
		# Sort detected objects in increasing order by distance between center of object and gaze coordinate (on the image plane)
		if objects_detected:
			sortedClasses = sorted(objects_detected, key=itemgetter(4),  reverse=False)
			# topLeftX, topLeftY = sortedClasses[0][2][0], sortedClasses[0][2][1] 
			# bottomRightX, bottomRightY = sortedClasses[0][3][0], sortedClasses[0][3][1]
			# toWrite = ""
			counter = 1;
			for obj in sortedClasses:
				topLeftX, topLeftY = obj[2][0], obj[2][1] 
				bottomRightX, bottomRightY = obj[3][0], obj[3][1]
				color = (255,0,0)
				if(counter==1):
					color = (0,255,0)

				frame = cv2.rectangle(frame,(topLeftX, topLeftY),(bottomRightX,bottomRightY),color,3)
				font = cv2.FONT_HERSHEY_COMPLEX_SMALL
				cv2.putText(frame, obj[0], (topLeftX,topLeftY-15), font, 1,(255,255,255),1,cv2.LINE_AA)
				cv2.imshow('Object Detection',frame)
				counter = counter+1

			# toWrite = str(sortedClasses[0][0]) + '\n'
			
			# toWrite += str(sortedClasses[0][0]) + ', ' + str(topLeftX) + ', ' + str(topLeftY) + ', ' + str(bottomRightX) + ', ' + str(bottomRightY) + ', ' 
			
			#toWrite = toWrite[:-2] + '\n'
			# print(toWrite)
			# toWrite = str(sortedClasses[0][0]) + ', ' + str(topLeftX) + ', ' + str(topLeftY) + ', ' + str(bottomRightX) + ', ' + str(bottomRightY) + '\n'
			# file.write(toWrite)	
			#print(sorted(objects_detected, key=itemgetter(4),  reverse=False))
			#print(getGazeData())
			# file.close()
		#print("\n")
		else:
			continue

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cam.release()
cv2.destroyAllWindows()