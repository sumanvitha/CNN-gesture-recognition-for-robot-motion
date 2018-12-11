
from keras.models import model_from_json
from keras.preprocessing.image import ImageDataGenerator
import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import threading
from matplotlib.pyplot import imshow
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras import backend as K
import serial


def load_model():
    try:
        json_file = open('model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        model = model_from_json(loaded_model_json)
        model.load_weights("weights.hdf5")
        model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
        return model
    except:
        print("""Model not found.""")
        return None

def recognize():
    cv2.namedWindow("webcam")
    cap = cv2.VideoCapture(0)
    
    if cap.isOpened():
        rval, frame = cap.read()
        
    else:
        rval = False
    
    classes=["BACK","LEFT","NOTHING","RIGHT","START","STOP"]
    arduino = serial.Serial("COM1", 9600)
    connected=False
    while not connected:
        ser=arduino.read()
        connected=True
    out=""
    while rval:
        frame=cv2.flip(frame,1)
        cv2.rectangle(frame,(300,200),(500,400),(0,255,0),1)
        cv2.putText(frame,"Place your hand in the green box.", (50,50), cv2.FONT_HERSHEY_PLAIN , 1, 255)
        cv2.putText(frame,"Press esc to exit.", (50,100), cv2.FONT_HERSHEY_PLAIN , 1, 255)
        
        
        img=frame[200:400,300:500]
        img = cv2.cvtColor( img, cv2.COLOR_RGB2GRAY)
        value = (35, 35)
        blurred = cv2.GaussianBlur(img, value, 0)
        _,thresh=cv2.threshold(blurred,100,225,cv2.THRESH_BINARY)
        cv2.imshow("thresh",thresh)
        img=thresh.reshape((1,)+thresh.shape)
        img=img.reshape(img.shape+(1,))
        test_datagen = ImageDataGenerator(rescale=1./255)
        m=test_datagen.flow(img,batch_size=1)
        y_pred=model.predict_generator(m,1)
        if y_pred[0].max()>0.8:
            output=classes[list(y_pred[0]).index(y_pred[0].max())]
            cv2.putText(frame, '%s' % output, (50,400), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 4)
            cv2.putText(frame, '(score = %.5f)' % y_pred[0].max(), (50,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))
            if out!=output:
                out=output
                if output == "LEFT":
                    arduino.write(('L').encode())
                    print(output)
                elif output == "RIGHT":
                    arduino.write(('R').encode())
                    print(output)
                elif output == "START":
                    arduino.write(('S').encode())
                    print(output)
                elif output == "STOP":
                    arduino.write(('T').encode())
                    print(output)
                elif output == "BACK":
                    arduino.write(('B').encode())
                    print(output)
        cv2.imshow("webcam", frame)
        rval, frame = cap.read()
        key = cv2.waitKey(70)
        if key == 27:
            break
    arduino.close()
    cv2.destroyWindow("webcam")
    cap=None
    

model=load_model()


if model is not None:
    recognize()
    
