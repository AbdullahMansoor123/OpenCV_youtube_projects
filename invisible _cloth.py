import cv2
import numpy

def hello(x):
    #only for reference
    print('')

#initalization of the camera
v_cap = cv2.VideoCapture(0)
bars = cv2.namedWindow('bars')

cv2.createTrackbar('upper_hue', 'bars', 0, 180, hello)
cv2.createTrackbar('upper_saturation', 'bars', 255, 255, hello)
cv2.createTrackbar('upper_value', 'bars', 220, 255, hello)
cv2.createTrackbar('lower_hue', 'bars', 0, 170, hello)
cv2.createTrackbar('lower_saturation', 'bars', 230, 180, hello)
cv2.createTrackbar('lower_value', 'bars', 170, 182, hello)


#takes and saves the first frame int_frame for creation of background
while True:
    cv2.waitKey(1000)
    ret, int_frame = v_cap.read()
    if ret:
        break

## Start capturing frame for actual project
while True:

    ret, frame = v_cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #getting the hsv values for masking the cloak
    upper_hue = cv2.getTrackbarPos('upper_hue', 'bars')
    upper_saturated = cv2.getTrackbarPos('upper_saturation', 'bars')
    upper_value = cv2.getTrackbarPos('upper_value', 'bars')
    lower_hue = cv2.getTrackbarPos('lower_hue', 'bars')
    lower_saturated = cv2.getTrackbarPos('lower_saturation', 'bars')
    lower_value = cv2.getTrackbarPos('lower_value', 'bars')

    #kernel for dilation (helps removes noise in image)

    kernel = numpy.ones((3,3), numpy.uint8)

    # upper_hsv = numpy.array([upper_hue, upper_saturated, upper_value])
    # lower_hsv = numpy.array([lower_hue, lower_saturated, lower_value])

    upper_hsv = numpy.array([177, 242 , 255])
    lower_hsv = numpy.array([144, 68, 0])

    mask = cv2.inRange(hsv_frame, lower_hsv, upper_hsv)
    mask = cv2.medianBlur(mask, 3)
    mask_inv = 255 - mask
    mask = cv2.dilate(mask, kernel,5)

    #the mixing of frame in a combination to achieve required frame
    b = frame[:,:,0]
    g = frame[:,:,1]
    r = frame[:,:,2]
    b = cv2.bitwise_and(mask_inv,b)
    g = cv2.bitwise_and(mask_inv,g)
    r = cv2.bitwise_and(mask_inv,r)
    frame_inv = cv2.merge((b,g,r))

    #replace the black area with the inital frame
    b = int_frame[:,:,0]
    g = int_frame[:,:,1]
    r = int_frame[:,:,2]
    b = cv2.bitwise_and(b,mask)
    g = cv2.bitwise_and(g,mask)
    r = cv2.bitwise_and(r,mask)
    blanket_area = cv2.merge((b,g,r))

    final = cv2.bitwise_or(frame_inv, blanket_area)

    cv2.imshow("Harry's invisbility cloal", final)
    # cv2.imshow('original', frame)

    if cv2.waitKey(3) == ord('q'):
        break;

cv2.destroyAllWindows()
v_cap.release()
