'''
    OpenCV face recognition implementation and communication with Arduino listening at serial port
    Alexis Rodríguez Casañas.
    Last update: 09.02.2018.
'''

import cv2
import sys
import math
import serial
import time

X_RES = 800

Y_RES = 600
X_CENTER = X_RES / 2
Y_CENTER = Y_RES / 2
EPS = 80
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)
video_capture.set(3, X_RES)
video_capture.set(4, Y_RES)

ser = serial.Serial('COM3', 9600)
print(ser.name)
if (ser.isOpen()):
    ser.close()
ser.open()


def get_difference(x, y, w, h):
    x = x + w / 2
    y = y + h / 2
    x_correction = X_CENTER - x
    y_correction = Y_CENTER - y
    return x_correction,  y_correction

def correct_camera(x_correction, y_correction):
    correction_done = False
    if (math.fabs(x_correction) > EPS):
        correction_done = True
        if (x_correction < 0):
            print(x_correction, ", ", y_correction)
            ser.write('b'.encode())
        else:
            print(x_correction, ",  ",y_correction)
            ser.write('a'.encode())
    if (math.fabs(y_correction) > EPS):
        correction_done = True
        if (y_correction < 0):
            ser.write('c'.encode())        
        else:
            ser.write('d'.encode())


while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        x_correction, y_correction = get_difference(x, y, w, h)
        print("x:", x_correction, "y:", y_correction)
        correction_done = correct_camera(x_correction, y_correction)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
ser.close()


