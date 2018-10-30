import cv2
import numpy as np
import socket
import sys
import serial
import time
Kpx = 0.25
Kpy = 0.25
Kdx = 0.25
Kdy = 0.25
Kix = 0
Kiy = 0
#ser=serial.Serial("COM4",115200)
def _pid(out_1, err, err_1, Kp, Ki, Kd):
    return Kp*err + Ki*(err+err_1) + Kd*(err-err_1)
def _dist(ctr, dim, siz):
    siz = siz/2
    return 200*(ctr[dim] - siz)/float(siz)
def process_image(centroid,img_height,img_width,roll,pitch):
    if not hasattr(process_image,'count'):
        process_image.count=0
        process_image.errx_prev=0
        process_image.erry_prev=0
        process_image.roll_prev=0
        process_image.pitch_prev=0
    if centroid:
        erry=_dist(centroid,0,img_height)
        errx=_dist(centroid,1,img_width)
        if process_image.count>0:
            roll=1500+_pid(process_image.roll_prev,errx,process_image.errx_prev,Kpx,Kix,Kdx)        
            pitch=1500+_pid(process_image.pitch_prev,erry,process_image.erry_prev,Kpy,Kiy,Kdy)
        process_image.errx_prev=errx
        process_image.erry_prev=erry
        process_image.count += 1
    return (roll,pitch)
def convertStr(val,state):
    return (str(state)+":"+str(val)+"E").encode()
def landing(ser):
    for x in range(1500,0,-7):
        ser.write(convertStr(x,3))
def arm(ser):
    ser.write(convertStr(1500,1))
    ser.write(convertStr(1500,2))
    ser.write(convertStr(1000,3))
    ser.write(convertStr(1000,4))
    print("Armed..")
    time.sleep(0.5)
    ser.write(convertStr(1500,1))
    ser.write(convertStr(1500,2))
    ser.write(convertStr(1000,3))
    ser.write(convertStr(1500,4))
def disarm(ser):
    ser.write(convertStr(1500,1))
    ser.write(convertStr(1500,2))
    ser.write(convertStr(1000,3))
    ser.write(convertStr(2000,4))
    time.sleep(0.5)
    ser.write(convertStr(1500,1))
    ser.write(convertStr(1500,2))
    ser.write(convertStr(1000,3))
    ser.write(convertStr(1500,4))
    print("Disarmed.")
cap=cv2.VideoCapture(0)
count_probz=0
##a=int(input("Enter step: "))
##if(a==1):
##    arm(ser)
##if(a==2):
##    disarm(ser)
##b=int(input("Enter step 2: "))
##if(b==1):
##    disarm(ser)
##for x in range(1000,1500,7):
##    ser.write(convertStr(x,3))
##    ser.write(convertStr(0,1))
##    ser.write(convertStr(0,2))
##    ser.write(convertStr(0,4))
##    time.sleep(0.1)
##print("Takeoff completed..")
while True:
    ret,image=cap.read()
    frameHSV  = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    height, width = image.shape[:2]
    cv2.rectangle(image,(width//2,height//2),(width//2+1,height//2+1),(0,255,0),2)
    colorLow = np.array([15, 150, 150])
    colorHigh = np.array([90, 255, 255])
    mask = cv2.inRange(frameHSV, colorLow, colorHigh)
    #cv2.imshow("Mask",mask)
    im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    if(count_probz>30):
        landing(ser)
        break
    if(len(contour_sizes)==0):
        print("None Found")
        vals=(None,None)
        #count_probz+=1
    else:
        biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
        x,y,w,h = cv2.boundingRect(biggest_contour)
        centroid=(x+w//2,y+h//2)
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
        vals=process_image((y+h/2,x+w/2),height,width,1500,1500)
    if vals[0] is not None:
        #ser.write(convertStr(vals[0],1))
        #ser.write(convertStr(vals[1],3))
        print(str(int(vals[0]))+":"+str(int(vals[1])))
    else:
        pass
    cv2.imshow("Image",image)
    if(cv2.waitKey(10) & 0xFF == ord('q')):
            break
#disarm(ser)
cv2.release()
cv2.destroyAllWindows()
