from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time
import cv2
import sys
import sip
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2

import dlib
from scipy.spatial import distance

from time import sleep
from pyfirmata import Arduino, util, SERVO

is_clicked = False
is_check = False

prototext = "ml_file/deploy.prototxt.txt"
model = "ml_file/res10_300x300_ssd_iter_140000.caffemodel"
net = cv2.dnn.readNetFromCaffe(prototext, model)

hog_face_detector = dlib.get_frontal_face_detector()
dlib_facelandmark = dlib.shape_predictor("ml_file/shape_predictor_68_face_landmarks.dat")

board = Arduino('COM3')
sleep(1)
board.digital[5].mode = SERVO
board.digital[4].mode = SERVO

def servoX(position):
    board.digital[5].write(position)

def servoY(position):
    board.digital[4].write(position)

# ? set defult servo position
moveServoX = 90
moveServoY = 90
servoX(moveServoX)
servoY(moveServoY)

class Ui_CureMyopia(QWidget):
    def setupUi(self, CureMyopia):
        CureMyopia.setObjectName("Cure myopia")
        CureMyopia.resize(1440, 960)
        CureMyopia.setMinimumSize(QtCore.QSize(1440, 960))
        CureMyopia.setMaximumSize(QtCore.QSize(1440, 960))
        self.centralwidget = QtWidgets.QWidget(CureMyopia)
        self.centralwidget.setObjectName("centralwidget")

        self.Worker1 = Worker1()
        self.Worker1.start()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        
        self.btn = QtWidgets.QLabel(self.centralwidget)
        self.btn.setGeometry(QtCore.QRect(480, 720, 480, 240))
        self.btn.setStyleSheet("background-color : rgb(225, 140, 45);\n"
"font: 100px \"FC Lamoon\";\n"
"font-weight: bold;\n"
"color: white;\n"
"border: 2px solid rgb(90,90,90);")
        self.btn.setObjectName("btn")
        self.btn.setAlignment(QtCore.Qt.AlignCenter)
        self.head_time = QtWidgets.QLabel(self.centralwidget)
        self.head_time.setGeometry(QtCore.QRect(960, 480, 480, 240))
        self.head_time.setStyleSheet("background-color : rgb(25, 25, 25);\n"
"font: 100px \"FC Lamoon\" ;\n"
"font-weight: bold;\n"
"color: white;\n"
"border: 2px solid rgb(90,90,90);")
        self.head_time.setAlignment(QtCore.Qt.AlignCenter)
        self.head_time.setObjectName("head_time")
        self.head_console = QtWidgets.QLabel(self.centralwidget)
        self.head_console.setGeometry(QtCore.QRect(960, 0, 480, 120))
        self.head_console.setStyleSheet("background-color : rgb(25, 25, 25);\n"
"font: 60px \"FC Lamoon\";\n"
"font-weight: bold;\n"
"color: white;\n"
"border: 2px solid rgb(90,90,90);")
        self.head_console.setAlignment(QtCore.Qt.AlignCenter)
        self.head_console.setObjectName("head_console")
        self.show_console = QtWidgets.QLabel(self.centralwidget)
        self.show_console.setGeometry(QtCore.QRect(960, 120, 480, 360))
        self.show_console.setStyleSheet("background-color : rgb(50, 50, 50);\n"
"font: 30px \"FC Lamoon\";\n"
"color: white;\n"
"border: 2px solid rgb(90,90,90);")
        self.show_console.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.show_console.setObjectName("show_console")
        self.show_time = QtWidgets.QLabel(self.centralwidget)
        self.show_time.setGeometry(QtCore.QRect(960, 720, 480, 240))
        self.show_time.setStyleSheet("background-color : rgb(50, 50, 50);\n"
"font: 100px \"FC Lamoon\";\n"
"color: white;\n"
"border: 2px solid rgb(90,90,90);")
        self.show_time.setAlignment(QtCore.Qt.AlignCenter)
        self.show_time.setObjectName("show_time")
        self.head_status = QtWidgets.QLabel(self.centralwidget)
        self.head_status.setGeometry(QtCore.QRect(0, 720, 240, 120))
        self.head_status.setStyleSheet("background-color : rgb(25, 25, 25);\n"
"font: 60px \"FC Lamoon\";\n"
"font-weight: bold;\n"
"color: white;\n"
"border: 2px solid rgb(90,90,90);")
        self.head_status.setAlignment(QtCore.Qt.AlignCenter)
        self.head_status.setObjectName("head_status")
        self.show_status = QtWidgets.QLabel(self.centralwidget)
        self.show_status.setGeometry(QtCore.QRect(0, 840, 240, 120))
        self.show_status.setStyleSheet("background-color : rgb(50, 50, 50);\n"
"font: 50px \"FC Lamoon\";\n"
"color: white;\n"
"border: 2px solid rgb(90,90,90);")
        self.show_status.setAlignment(QtCore.Qt.AlignCenter)
        self.show_status.setObjectName("show_status")
        self.logo_bg = QtWidgets.QLabel(self.centralwidget)
        self.logo_bg.setGeometry(QtCore.QRect(240, 720, 240, 240))
        self.logo_bg.setStyleSheet("background-color : rgb(90, 90, 90);")
        self.logo_bg.setText("")
        self.logo_bg.setObjectName("logo_bg")
        self.display = QtWidgets.QLabel(self.centralwidget)
        self.display.setGeometry(QtCore.QRect(0, 0, 960, 720))
        self.display.setStyleSheet("background-color : rgb(50, 50, 50);\n"
"font: 140px \"FC Lamoon\";\n"
"color: white;\n"
"border: 2px solid rgb(90,90,90);")
        self.display.setAlignment(QtCore.Qt.AlignCenter)
        self.display.setObjectName("display")
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(260, 740, 200, 200))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap("img/focus_200px.png"))
        self.logo.setObjectName("logo")
        CureMyopia.setCentralWidget(self.centralwidget)

        CureMyopia.setWindowIcon(QtGui.QIcon("img/focus_200px.png")) 

        self.retranslateUi(CureMyopia)
        QtCore.QMetaObject.connectSlotsByName(CureMyopia)

    def retranslateUi(self, CureMyopia):
        _translate = QtCore.QCoreApplication.translate
        CureMyopia.setWindowTitle(_translate("CureMyopia", "CureMyopia"))
        self.btn.setText(_translate("CureMyopia", "Let's Go!"))
        self.head_time.setText(_translate("CureMyopia", "TIME"))
        self.head_console.setText(_translate("CureMyopia", "CONSOLE"))
        self.show_console.setText(_translate("CureMyopia", "[+] loading face bounding box model  [DONE]\n"
"[+] loading eye detector model         [DONE]\n"
"[+] connecting servo serial              [DONE]\n\n"
"[ FINISHED! ]"))
        self.show_time.setText(_translate("CureMyopia", "00 : 00"))
        self.head_status.setText(_translate("CureMyopia", "STATUS"))
        self.show_status.setText(_translate("CureMyopia", "nope"))
        self.display.setText(_translate("CureMyopia", "display"))
    
    def __init__(self, *args):
        super(QWidget, self).__init__()
        self.setupUi(CureMyopia)
        self.show_status.setText("nope")
        self.show_status.setStyleSheet("background-color : rgb(50, 50, 50);\n"
"font: 50px \"FC Lamoon\";\n"
"color: white;\n"
"border: 2px solid rgb(90,90,90);")
           
    def ImageUpdateSlot(self, Image):
        self.display.setPixmap(QPixmap.fromImage(Image))

class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)
        
    def run(self):
        
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        
        def blinked():
            self.parent.show_status.setText("blinked")
            self.parent.show_status.setStyleSheet("background-color : rgb(140, 200, 60);\n"
                        "font: 50px \"FC Lamoon\";\n"
                        "color: white;\n"
                        "border: 2px solid rgb(90,90,90);")

        def nope():
            self.parent.show_status.setText("nope")
            self.parent.show_status.setStyleSheet("background-color : rgb(20, 200, 90);\n"
                        "font: 50px \"FC Lamoon\";\n"
                        "color: white;\n"
                        "border: 2px solid rgb(90,90,90);")

        while self.ThreadActive:
            global is_clicked, is_check
            
            ret, frame = Capture.read()
            cv2.rectangle(frame, (315, 235), (325, 245), (45,140,225), cv2.FILLED)
            cv2.rectangle(frame, (135, 95), (145, 105), (45,140,225), cv2.FILLED)
            cv2.rectangle(frame, (495, 95), (505, 105), (45,140,225), cv2.FILLED)
            cv2.rectangle(frame, (135, 375), (145, 385), (45,140,225), cv2.FILLED)
            cv2.rectangle(frame, (495, 375), (505, 385), (45,140,225), cv2.FILLED) 

            if is_check == True:
                set_confidence = float(0.5)		# ? add confidence(%) you can customize.

                def calculate_EAR(eye):
                    A = distance.euclidean(eye[1], eye[5])
                    B = distance.euclidean(eye[2], eye[4])
                    C = distance.euclidean(eye[0], eye[3])
                    ear_aspect_ratio = (A+B)/(2.0*C)
                    return ear_aspect_ratio

                frame = imutils.resize(frame, width=640) 

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = hog_face_detector(gray)

                (h, w) = frame.shape[:2]
                blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

                net.setInput(blob)
                detections = net.forward()
                
            else:
                set_confidence = float(0.5)		# ? add confidence(%) you can customize.
                def calculate_EAR(eye):
                    A = distance.euclidean(eye[1], eye[5])
                    B = distance.euclidean(eye[2], eye[4])
                    C = distance.euclidean(eye[0], eye[3])
                    ear_aspect_ratio = (A+B)/(2.0*C)
                    return ear_aspect_ratio

                frame = imutils.resize(frame, width=640) 

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = hog_face_detector(gray)

                (h, w) = frame.shape[:2]
                blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

                net.setInput(blob)
                detections = net.forward()
                for i in range(0, detections.shape[2]):
                    confidence = detections[0, 0, i, 2]
                    if confidence < set_confidence : 
                        continue
                    # * compute the (x, y)-coordinates of the bounding box for the
                    # * object
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    # print (endX-startX, endY-startY)

                    text = "{:.2f}%".format(confidence * 100)
                    y = startY - 10 if startY - 10 > 10 else startY + 10
                    cv2.rectangle(frame, (startX, startY), (endX, endY),(45,140,225), 2)
                    cv2.putText(frame, "Human_face : " + text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (45,140,225), 2)

                    # ? just face detection decorate.
                    centerX = int((startX + endX) / 2)
                    centerY = int((startY + endY) / 2)
                    
                    line1_top = (int(centerX - 8), int(centerY + 8))
                    line1_bot = (int(centerX + 8), int(centerY - 8))
                    line2_top = (int(centerX + 8), int(centerY + 8))
                    line2_bot = (int(centerX - 8), int(centerY - 8))

                    cv2.line(frame, line1_top, line1_bot, (45, 140, 225), 2)
                    cv2.line(frame, line2_top, line2_bot, (45, 140, 225), 2)

                    cv2.rectangle(frame, (startX + 5, startY - 5), (startX - 5, startY + 5), (45,140,225), cv2.FILLED)
                    cv2.rectangle(frame, (startX + 5, endY - 5), (startX - 5, endY + 5), (45,140,225), cv2.FILLED)
                    cv2.rectangle(frame, (endX + 5, startY - 5), (endX - 5, startY + 5), (45,140,225), cv2.FILLED)
                    cv2.rectangle(frame, (endX + 5, endY - 5), (endX - 5, endY + 5), (45,140,225), cv2.FILLED)

                    global moveServoX, moveServoY

                    # ? set move position of servo
                    if centerX < 140 : 
                        MoveX = 140 - centerX 
                        moveServoX = moveServoX + (MoveX / 5)
                        servoX(moveServoX)
                    elif centerX > 500 :
                        MoveX = centerX - 500
                        moveServoX = moveServoX - (MoveX / 5)
                        servoX(moveServoX)

                    if centerY < 105 :
                        MoveY = 105 - centerY
                        moveServoY = moveServoY + (MoveY / 4)	
                        new_pos = abs(180 - moveServoY)         # ? this you can do like servoX but my servo is reverse ก็เลยต้องลบค่าเเล้ว absloute เอา
                        servoY(new_pos)  
                    elif centerY > 375 :
                        MoveY = centerY - 375
                        moveServoY = moveServoY - (MoveY / 4)
                        new_pos = abs(180 - moveServoY)
                        servoY(new_pos)
                    
                    # ? make line that connect to center
                    cv2.line(frame, (320, 240), (centerX, centerY), (45, 140, 225), 2)
                    #!========================================================================
                    for face in faces:
                        face_landmarks = dlib_facelandmark(gray, face)
                        leftEye = []
                        rightEye = []

                        for n in range(36,42):
                            x = face_landmarks.part(n).x
                            y = face_landmarks.part(n).y
                            leftEye.append((x,y))
                            next_point = n+1
                            if n == 41:
                                next_point = 36
                            x2 = face_landmarks.part(next_point).x
                            y2 = face_landmarks.part(next_point).y
                            cv2.line(frame,(x,y),(x2,y2),(77,233,245),2)

                        for n in range(42,48):
                            x = face_landmarks.part(n).x
                            y = face_landmarks.part(n).y
                            rightEye.append((x,y))
                            next_point = n+1
                            if n == 47:
                                next_point = 42
                            x2 = face_landmarks.part(next_point).x
                            y2 = face_landmarks.part(next_point).y
                            cv2.line(frame,(x,y),(x2,y2),(77,233,245),2)

                        left_ear = calculate_EAR(leftEye)
                        right_ear = calculate_EAR(rightEye)

                        EAR = (left_ear+right_ear)/2
                        EAR = round(EAR,2)
                        if EAR<0.20:
                            # cv2.putText(frame,"DROWSY",(20,100), cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),4)
                            # cv2.putText(frame,"Are you Sleepy?",(20,400), cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),4)
                            # blinked() 
                            print("yeah, him blinked")
                            # print(time.strftime("%M : %S", time.gmtime(elapsed)))
                            # print(EAR)
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(828, 684, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic) 

    def stop(self):
        self.ThreadActive = False

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CureMyopia = QtWidgets.QMainWindow()
    ui = Ui_CureMyopia()
    CureMyopia.show()
    sys.exit(app.exec_())
