import cv2
import numpy as np
import socket
import sys
import time
import asyncio
import websockets
Kpx = 0.25
Kpy = 0.25
Kdx = 0.25
Kdy = 0.25
Kix = 0
Kiy = 0
def _pid(out_1, err, err_1, Kp, Ki, Kd):
    return Kp*err + Ki*(err+err_1) + Kd*(err-err_1)
def _dist(ctr, dim, siz):
    siz = siz/2
    return 100*(ctr[dim] - siz)/float(siz)
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
cap=cv2.VideoCapture(0)
async def execFunction(websocket,path):
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
    if(len(contour_sizes)==0):
        print("None Found")
        vals=(None,None)
    else:
        biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
        x,y,w,h = cv2.boundingRect(biggest_contour)
        centroid=(x+w//2,y+h//2)
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
        vals=process_image((y+h/2,x+w/2),height,width,1500,1500)
    if vals[0] is not None:
        #c.send((str(int(vals[0]))+":"+str(int(vals[1]))).encode())
        send_str=f"{vals[0]}"+f":"+f"{vals[1]}"
        await websocket.send(send_str)
        print(str(int(vals[0]))+":"+str(int(vals[1])))
        #c.close()
    else:
        send_str=f"0:0"
        await websocket.send(send_str)
    #cv2.imshow("Image",image)
    if(cv2.waitKey(10) & 0xFF == ord('q')):
            return
start_server=websockets.serve(execFunction,'localhost',8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
cv2.release()
cv2.destroyAllWindows()
