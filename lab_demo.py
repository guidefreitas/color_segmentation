import cv2
import numpy as np

threshold = 0.2
kernel5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(20,20))
lab_img = None
x_co = 0
y_co = 0
L = 0
A = 0
B = 0
thr_L = 100*threshold
thr_A = 255*threshold
thr_B = 255*threshold

def on_mouse(event,x,y,flag,param):
  global x_co,y_co,L,A,B,lab_img
  if(event==cv2.EVENT_LBUTTONDOWN):
    x_co=x
    y_co=y
    p_sel = lab_img[y_co][x_co]
    L = p_sel[0]
    A = p_sel[1]
    B = p_sel[2]

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
    lab_img = cv2.cvtColor(src, cv2.COLOR_BGR2LAB)
    cv2.setMouseCallback("camera2",on_mouse, 0);

    min_color = np.array([L-thr_L,A-thr_A,B-thr_B])
    max_color = np.array([L+thr_L,A+thr_A,B+thr_B])
    mask = cv2.inRange(lab_img, min_color, max_color)
    #mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel5)
    
    res = cv2.cvtColor(lab_img, cv2.COLOR_LAB2BGR)
    cv2.putText(mask,"L:" + str(L)+" A:"+str(A)+" B:"+str(B), (10,30), cv2.FONT_HERSHEY_PLAIN, 2.0, (255,255,255), thickness = 1)
    cv2.imshow("camera", mask)
    cv2.imshow("camera2", src)
    src_segmented = cv2.add(src,src,mask=mask)
    cv2.imshow("camera3", src_segmented)
    if cv2.waitKey(10) == 27:
        break