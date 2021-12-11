import cv2
import numpy as np

v_cap = cv2.VideoCapture(0)
v_cap.set(3, 640)  # setting frame width
v_cap.set(4, 340)  # setting frame height

while True:
    success, frame = v_cap.read()
    if not success:
        break
    # Gaussian blur is used for reducing noise detected by mask
    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    imgHSV = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

    # yellow object
    lower = np.array([17, 75, 159])
    upper = np.array([37, 212, 255])
    # ~skin color~
    # lower = np.array([0, 22, 86])
    # upper = np.array([22, 92, 255])
    mask = cv2.inRange(imgHSV, lower, upper)

    # finding the contour of the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        color_area = cv2.contourArea(contour)

        # put a bounding box around the color region
        if color_area > 1500:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # show display
    cv2.imshow("frame", frame)
    # cv2.imshow('Contours', contours)

    # exit button
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

v_cap.release()
cv2.destroyAllWindows()
