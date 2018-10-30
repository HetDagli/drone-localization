import cv2
import numpy
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
    return 1000*(ctr[dim] - siz)/float(siz)
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
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap=cv2.VideoCapture(0)
while True:
    ret,frame=cap.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    height, width = frame.shape[:2]
    for (x,y,w,h) in faces:
        print(process_image((y+h/2,x+w/2),height,width,1000,1000))
        cv2.rectangle(frame,(int(width/2),int(height/2)),(int(width/2+1),int(height/2+1)),(255,0,0),2)
        cv2.rectangle(frame,(x+w//2,y+h//2),(x+w//2+1,y+h//2+1),(255,0,0),2)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        break
    if(cv2.waitKey(10) & 0xFF == ord('q')):
            break
    cv2.imshow('img',frame)
cv2.release()
cv2.destroyAllWindows()
