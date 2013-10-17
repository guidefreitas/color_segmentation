import cv2
import numpy as np

kernel5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(20,20))
x_co = 0
y_co = 0
H = 0
S = 0
V = 0

def on_mouse(event,x,y,flag,param):
  global x_co,y_co,H,S,V
  if(event==cv2.EVENT_LBUTTONDOWN):
    x_co=x
    y_co=y
    p_sel = param[y_co][x_co]
    H = p_sel[0]
    S = p_sel[1]
    V = p_sel[2]

cv2.namedWindow("camera", 1)
cv2.namedWindow("camera2", 2)
cv2.namedWindow("camera3", 3)
#cam = video.create_capture(0)
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, src = cam.read()
    src = cv2.blur(src, (3,3))
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    cv2.setMouseCallback("camera2",on_mouse, hsv);

    min_color = np.array([H-25,S-50,V-50])
    max_color = np.array([H+25,S+50,V+50])
    mask = cv2.inRange(hsv, min_color, max_color)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel5)
    
    res = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    cv2.putText(mask,"H:" + str(H)+" S:"+str(S)+" V:"+str(V), (10,30), cv2.FONT_HERSHEY_PLAIN, 2.0, (255,255,255), thickness = 1)
    cv2.imshow("camera", mask)
    cv2.imshow("camera2", src)
    src_segmented = cv2.add(src,src,mask=mask)
    cv2.imshow("camera3", src_segmented)
    if cv2.waitKey(10) == 27:
        break