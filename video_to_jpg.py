"""Taken from: https://www.geeksforgeeks.org/extract-images-from-video-in-python/ (minor modifications)

	Get JPG images for each video
"""

# Importing all necessary libraries
import cv2
import os

dir = "boat/boat.mp4"

# Read the video from specified path
cam = cv2.VideoCapture('./data/' + dir)

try:
	# creating a folder named data
	if not os.path.exists('data'):
		os.makedirs('data')

# if not created then raise error
except OSError:
	print ('Error: Creating directory of data')

# frame
currentframe = 0

while(True):
	
	# reading from frame
	ret,frame = cam.read()

	if ret:
		# if video is still left continue creating images
		name =   './data/'+ dir.split('/')[0] + '/images/'+str(currentframe).zfill(5) + '.jpg'
		print ('Creating...' + name)

		# writing the extracted images
		cv2.imwrite(name, frame)

		# increasing counter so that it will
		# show how many frames are created
		currentframe += 1
	else:
		break

# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()
