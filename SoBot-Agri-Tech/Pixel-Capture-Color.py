import cv2
import numpy as np

def get_pixel_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        bgr_color = frame[y, x]
        hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)[0][0]
        # print("Pixel color (BGR): ", bgr_color)
        print("Pixel color (HSV): ", hsv_color)

# Starts video capture from the camera
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

cap.set(3, 640)
cap.set(4, 360)
cap.set(5, 25)  # Set frame rate
cap.set(cv2.CAP_PROP_BRIGHTNESS, 128)
cap.set(cv2.CAP_PROP_CONTRAST, 32)
cap.set(cv2.CAP_PROP_AUTO_WB, 1)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
# cap.set(cv2.CAP_PROP_EXPOSURE, -1)

# Defines the mouse callback function to capture click coordinates
cv2.namedWindow("image")
cv2.setMouseCallback("image", get_pixel_color)

while True:
    # Captures a video frame
    ret, frame = cap.read()
    
    # Checks if the frame was successfully captured
    if not ret:
        print("Error capturing video frame")
        break
    
    # Displays the video frame in a window
    cv2.imshow("image", frame)
    
    # Checks if the 'q' key was pressed to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Releases the camera and closes the window
cap.release()
cv2.destroyAllWindows()
