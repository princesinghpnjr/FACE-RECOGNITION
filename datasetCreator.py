import cv2
import numpy as np
import sqlite3

faceDetect= cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)

def insertOrUpdate(Id,Name):
    conn=sqlite3.connect("FaceBase.db")
    cmd="SELECT * FROM People WHERE Id="+str(Id)
    cursor=conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        cmd="UPDATE People SET Name="+str(Name)+"WHERE Id="+str(Id)
    else:
        cmd="INSERT INTO PEOPLE(Id,Name) values("+str(Id)+","+str(Name)+")"
        conn.execute(cmd)
        conn.commit()
        conn.close()

Id=input('Enter user id : ')
Name=input('Enter your name : ')
insertOrUpdate(Id,Name)
sampleNum=0
while(True):
    ret, img = cam.read();
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5);
    for (x,y,w,h) in faces:
        sampleNum=sampleNum+1
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        cv2.imwrite("dataSet/user."+Id+'.'+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
        cv2.imshow('Face',img);
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break
    elif sampleNum>20:
        break   
cam.release()
cv2.destroyAllWindows()
