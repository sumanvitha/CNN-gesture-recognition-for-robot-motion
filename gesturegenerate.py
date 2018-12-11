import cv2
from time import sleep
import os

if not os.path.exists("Dataset"):os.mkdir("Dataset")
if not os.path.exists("Dataset/training_set"):os.mkdir("Dataset/training_set")


dirs=['back/back','left/left','nothing/nothing','right/right','start/start','stop/stop']
sets={'training_set':500}

for set_name in sets:
    print("Taking images for the {}. Press enter ".format(set_name.upper()))
    input()
    if not os.path.exists("Dataset"):os.mkdir("Dataset/{}".format(set_name))
    for dir_name in dirs:
        print("""\nTaking images for the {} dataset. Press enter""".format(dir_name))
        input()
        
        sleep(1)
        if not os.path.exists("Dataset/{}/{}".format(set_name,os.path.basename(dir_name))):os.mkdir("Dataset/{}/{}".format(set_name,os.path.basename(dir_name)))
        cap=cv2.VideoCapture(0)
        if cap.isOpened():
            rval,frame= cap.read()
        else:
            rval=False
        index=0
        x=0
        while rval:
            index+=1
            rval, frame = cap.read()
            frame=cv2.flip(frame,1)
            cv2.putText(frame,"Keep your hand gesture in the green box.", (20,50), cv2.FONT_HERSHEY_PLAIN , 1, 255)
            cv2.putText(frame," {} dataset".format(dir_name), (20,80), cv2.FONT_HERSHEY_PLAIN , 2, 255)
            cv2.rectangle(frame,(300,200),(500,400),(0,255,0),1)
            cv2.imshow("Recording", frame)
            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            value = (35, 35)
            blurred = cv2.GaussianBlur(gray, value,0)
            _,thresh=cv2.threshold(blurred,105,225,cv2.THRESH_BINARY)
            cv2.imwrite("Dataset/{}/".format(set_name)+str(dir_name)+"{}.jpg".format(index),thresh[200:400,300:500]) 
            print("images taken: {}".format(index))
            key = cv2.waitKey(20)
            if key == 27 or index==sets[set_name]:
                break

        cv2.destroyWindow("Recording")
        cap=None
