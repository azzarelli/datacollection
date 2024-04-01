# From ChatGPT:

import cv2

# Open the video file
cap = cv2.VideoCapture('input_video.mp4')

# Read the first frame to initialize background
ret, background = cap.read()
background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)

# Process each frame
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Compute absolute difference between background and current frame
    diff = cv2.absdiff(gray_frame, background)
    
    # Threshold the difference to obtain a binary mask
    _, mask = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)
    
    # Apply the mask to the original frame
    masked_frame = cv2.bitwise_and(frame, frame, mask=mask)
    
    # Display the masked frame
    cv2.imshow('Masked Video', masked_frame)
    
    # Press 'q' to exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
