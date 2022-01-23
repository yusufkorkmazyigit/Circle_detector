import cv2
import numpy as np

videoCapture = cv2.VideoCapture(0)
prevCircle = None
dist = lambda x1,y1,x2,y2:(x1-x2)**2+(y1-y2)**2


while True:
    ret, frame = videoCapture.read()
    if not ret: break

    grayFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blurFrame = cv2.GaussianBlur(grayFrame,(17,17), 0)

    #cv2.imshow("Blur Frame",blurFrame)

    circles = cv2.HoughCircles(blurFrame,cv2.HOUGH_GRADIENT,1.18,200,
                               param1=95, param2=50,
                               minRadius=10, maxRadius=150)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        chosen = None
        for i in circles[0,:]:
            if chosen is None: chosen = i
            if prevCircle is not None:
                if dist(chosen[0],chosen[1],prevCircle[0],prevCircle[1])<= dist(i[0],i[1],prevCircle[0],prevCircle[1]):
                    chosen = i
        cv2.circle(frame, (chosen[0],chosen[1]), 1, (0,100,100),3)
        cv2.circle(frame,(chosen[0],chosen[1]),chosen[2], (0,0,255),5)
        prevCircle = chosen

    cv2.imshow("circles",frame)
    cv2.imshow("Blur ",blurFrame)


    if cv2.waitKey(25) & 0xFF == ord("q"): break

videoCapture.release()
cv2.destroyAllWindows()