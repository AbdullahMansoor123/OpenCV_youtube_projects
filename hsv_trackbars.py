import cv2
import numpy as np

v_cap = cv2.VideoCapture(0)
v_cap.set(3, 540)  # setting frame width
v_cap.set(4, 240)  # setting frame height


def empty():
    pass

#Creating a HSV window
cv2.namedWindow('HSV')
cv2.resizeWindow('HSV',(340,240))

#Creating track bar for the HSV window
cv2.createTrackbar('Hue Min','HSV',0,179,empty)
cv2.createTrackbar('Hue Max','HSV',179,179,empty)
cv2.createTrackbar('Sat Min','HSV',0,255,empty)
cv2.createTrackbar('Sat Max','HSV',255,255,empty)
cv2.createTrackbar('Value Min','HSV',0,255,empty)
cv2.createTrackbar('Value Max','HSV',255,255,empty)


while True:
    success, frame = v_cap.read()
    if not success:
        break
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # mask color filter
    h_min = cv2.getTrackbarPos('Hue Min','HSV')
    h_max = cv2.getTrackbarPos('Hue Max', 'HSV')
    s_min = cv2.getTrackbarPos('Sat Min', 'HSV')
    s_max = cv2.getTrackbarPos('Sat Max', 'HSV')
    v_min = cv2.getTrackbarPos('Value Min', 'HSV')
    v_max = cv2.getTrackbarPos('Value Max', 'HSV')

    # mask color range
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHSV, lower, upper)
    mask2 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    hstack = np.hstack([frame, mask2])


    cv2.imshow('Hoizontal Stack',hstack)

    if cv2.waitKey(1000) & 0xff == ord('q'):
        break

v_cap.release()
cv2.destroyAllWindows()