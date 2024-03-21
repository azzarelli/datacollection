"""Taken from: https://www.geeksforgeeks.org/extract-images-from-video-in-python/ (minor modifications)

	Get JPG images for each video
"""

# Importing all necessary libraries
import cv2
import os
import numpy as np

dir = ['../data/trex_results/render_ZAM.mp4','../data/trex_results/render_HP.mp4']
destination = ['xt_ZAM.png','xt_HP.png']

start = 300
end = 500
y = 370

for d,dest in zip(dir, destination):
	# Read the video from specified path
	cam = cv2.VideoCapture(d)

	# Check if the video opened successfully
	if not cam.isOpened():
		print("Error: Could not open video file.")
		exit()
	# frame
	currentframe = 0
	while(True):
		# reading from frame
		ret,frame = cam.read()

		# Check if frame reading was successful
		if not ret:
			image = cv2.cvtColor(xt, cv2.COLOR_RGB2BGR)  # OpenCV uses BGR color space by default

			cv2.imwrite(dest, image)
			break
		
		flattened_matrix =  np.expand_dims(frame[y, start:end], axis=1)

		if currentframe == 0:
			# cv2.destroyAllWindows()
			xt = flattened_matrix
		else:
			xt = np.concatenate((xt, flattened_matrix), axis=1)
		currentframe += 1

		if currentframe == 12:
			print(frame[y, start:end])
			frame[y, start:end][0] = 255
			frame[y, start:end][1:] = 0
			cv2.imwrite('vector_line.png', frame)
			# Wait for a key press and close the window
			cv2.waitKey(0)

	# Release all space and windows once done
	cam.release()
	# cv2.destroyAllWindows()										
