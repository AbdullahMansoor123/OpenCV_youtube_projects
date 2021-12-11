import cv2
import numpy as np

v_cap = cv2.VideoCapture(0)
v_cap.set(3, 340)  # setting frame width
v_cap.set(4, 140)  # setting frame height


def empty():
    pass


cv2.namedWindow("HSV")
cv2.resizeWindow('HSV', 340, 240)
cv2.createTrackbar('HUE Min', 'HSV', 0, 179, empty)
cv2.createTrackbar('HUE Max', 'HSV', 179, 179, empty)
cv2.createTrackbar('SAT Min', 'HSV', 0, 255, empty)
cv2.createTrackbar('SAT Max', 'HSV', 255, 255, empty)
cv2.createTrackbar('VALUE Min', 'HSV', 0, 255, empty)
cv2.createTrackbar('VALUE Max', 'HSV', 255, 255, empty)

while True:
    success, frame = v_cap.read()
    if not success:
        break
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # get trackbar values
    h_min = cv2.getTrackbarPos('HUE Min', 'HSV')
    h_max = cv2.getTrackbarPos('HUE Max', 'HSV')
    s_min = cv2.getTrackbarPos('SAT Min', 'HSV')
    s_max = cv2.getTrackbarPos('SAT Max', 'HSV')
    v_min = cv2.getTrackbarPos('VALUE Min', 'HSV')
    v_max = cv2.getTrackbarPos('VALUE Max', 'HSV')

    # preparing mask
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHSV, lower, upper)
    results = cv2.bitwise_and(frame, frame, mask=mask)
    #to stack masks as well we need our mask (1 channel) into 3 channel
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    #stacking frame,results and mask together
    hstack = np.hstack([frame,results,mask])

    # cv2.imshow("frame", frame)
    # cv2.imshow('HSV color space', imgHSV)
    # cv2.imshow("Mask", mask)
    # cv2.imshow('results', results)
    cv2.imshow('Horizontal stack', hstack)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

v_cap.release()
cv2.destroyAllWindows()
