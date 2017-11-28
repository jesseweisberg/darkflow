####!usr/bin/env python2
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# File: 	grasp_class.py
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
from multiprocessing import Process 
import sys
sys.path.append('../../pupil/pupil_src/shared_modules/')
from camera_models import *
import numpy as np
import cv2
from operator import itemgetter, attrgetter, methodcaller
import math
import scipy
from scipy import misc
from scipy.misc import imresize
from PupilData import *
from darkflow.net.build import TFNet

fixated_object_label = None

def publish_detected_object(label):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    addr = '127.0.0.1'  # remote ip or localhost
    port = "5556"  # same as in the pupil remote gui
    socket.bind("tcp://{}:{}".format(addr, port))
    time.sleep(1)
    while label is not None:
        topic = 'detected_object'
        #print ('%s %s' % (topic, label))
        try:
            socket.send_string('%s %s' % (topic, label))
        except TypeError:
            socket.send('%s %s' % (topic, label))
        break
      

def detect_gazed_object():
	# Run on yolo trained on COCO dataset (COCO is a dataset comprised of common household objects)
	options = {"model": "cfg/yolo.cfg", "load": "weights/yolo.weights", "demo": 'camera', "threshold": 0.2}

	# Run on tiny yolo (for ultimate speed)
	#options = {"model": "cfg/tiny-yolo.cfg", "load": "weights/tiny-yolo.weights", "threshold": 0.2}
	tfnet = TFNet(options)

	# Predetermined radial distortion coefficients and intrinsic camera parameters for undistorting later on.
	dist_coefs = np.array(pre_recorded_calibrations['Pupil Cam1 ID2']['(1280, 720)']['dist_coefs'])
	camera_matrix = np.array(pre_recorded_calibrations['Pupil Cam1 ID2']['(1280, 720)']['camera_matrix'])

	frame_width = 1280  # Alternate potential dimensions: 320x240
	frame_height = 720
	cam = cv2.VideoCapture(-1) # world camera: index=2, eye camera: index=3
	cam.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
	cam.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
	
	while(True):
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

			# Sort detected objects in increasing order by distance between center of object and gaze coordinate (on the image plane)
			if objects_detected:  # If there are still any detected objects after 'weeding out' irrelevant objects.
				sortedClasses = sorted(objects_detected, key=itemgetter(4),  reverse=False)
				closest_obj = True;
				for obj in sortedClasses:
					top_left_x, top_left_y = obj[2][0], obj[2][1] 
					bottom_right_x, bottom_right_y = obj[3][0], obj[3][1]
					bounding_box_color = (255,0,0) # Default bounding box color is blue.
					if(closest_obj==True):
						global fixated_object_label
						fixated_object_label = obj[0]
						#print(fixated_object_label)
						p2 = Process(target = publish_detected_object(fixated_object_label))
						p2.start()
						# publish_detected_object(fixated_object_label) via zmq so we can use in ROS
						bounding_box_color = (0,255,0) # Closest object has a green bounding box.
						closest_obj = False
						p2.terminate()
					# Append bounding boxes along with classification labels
					frame = cv2.rectangle(frame,(top_left_x, top_left_y),(bottom_right_x,bottom_right_y),bounding_box_color,3)
					label_font = cv2.FONT_HERSHEY_COMPLEX_SMALL
					cv2.putText(frame, obj[0], (top_left_x,top_left_y-15), label_font, 1,(255,255,255),1,cv2.LINE_AA)
					cv2.imshow('Object Detection',frame)		
			else:
				continue

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	cam.release()
	cv2.destroyAllWindows()

if __name__ == "__main__": 
	p1 = Process(target = detect_gazed_object)
	p1.start()
	
