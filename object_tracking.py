import cv2
import numpy as np

v_cap = cv2.VideoCapture(0)

# tracker = cv2.legacy.TrackerMOSSE_create()
tracker = cv2.legacy.TrackerCSRT_create()
success, frame = v_cap.read()
bbox = cv2.selectROI('Tracking',frame,False)
tracker.init(frame,bbox)

def draw_box(frame,bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2,1)
    cv2.putText(frame, 'Tracking', (75, 75), 0, 0.7, (0, 255, 0), 2)


while True:
    timer = cv2.getTickCount()
    success, frame = v_cap.read()
    if not success:
        break
    success, bbox = tracker.update(frame)
    print(bbox)
    if success:
        draw_box(frame,bbox)
    else:
        cv2.putText(frame, 'lost', (75, 75), 0, 0.7, (0, 0, 255), 2)

    fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
    cv2.putText(frame, str(int(fps)),(75,50), 0, 0.7, (0,0,255), 2)

    cv2.imshow('Tracking', frame)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

v_cap.release()
cv2.destroyAllWindows()
