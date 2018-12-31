#!/usr/bin/python
# -*- coding: UTF-8 -*-

import numpy as np
import cv2
import screeninfo
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QLabel, QComboBox
from PyQt5.QtGui import QPixmap, QImage  
import sys  
import multiprocessing

# get the size of the screen
screen_id = 1
is_color = False
screen = screeninfo.get_monitors()[screen_id]
full_screen_width, full_screen_height = screen.width, screen.height


class Q_Window(QWidget): 
      
    def __init__(self):  
        super(Q_Window, self).__init__()    
        self.initParas()
        self.initUI()


    def initParas(self):
        self.timer_camera = QtCore.QTimer()
        self.timer_camera_2 = QtCore.QTimer()

        self.cap = cv2.VideoCapture()
        self.cap_size = [1280, 720]
        self.cap_2 = cv2.VideoCapture()
        self.cap_2_size = [1280, 720]

        self.CAM_1 = 1
        self.CAM_2 = 2
        self.full_screen_show_id = 1
          

    def initUI(self):                 
        self.image_View = QLabel("image", self)
        self.image_View.resize(640, 480)
        self.image_View.setScaledContents(True)
        self.image_View.move(60,30)
        jpg=QPixmap('timg.jpeg')  
        self.image_View.setPixmap(jpg)

        self.image_View_2 = QLabel("image2", self)
        self.image_View_2.resize(640, 480)
        self.image_View_2.setScaledContents(True)
        self.image_View_2.move(760,30)
        self.image_View_2.setPixmap(jpg) 

        self.det_Button = QPushButton(u'打开输入源一', self)
        self.det_Button.clicked.connect(self.open_camera)  
        self.det_Button.resize(200,40)  
        self.det_Button.move(360, 560) 

        self.det_Button_2 = QPushButton(u'打开输入源二', self)
        self.det_Button_2.clicked.connect(self.open_camera_2)  
        self.det_Button_2.resize(200,40)  
        self.det_Button_2.move(900, 560)

        self.switch_Button = QPushButton(u'切换到二号输入源', self)
        self.switch_Button.clicked.connect(self.switch_input)  
        self.switch_Button.resize(200,80)  
        self.switch_Button.move(630, 620)
        
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_camera_2.timeout.connect(self.show_camera_2)

        self.setGeometry(300, 300, 1460, 720)  
        self.setWindowTitle('ChgDirector')      
        self.show() 


    def switch_input(self):
        if self.full_screen_show_id == 1:
            self.full_screen_show_id = 2
            self.switch_Button.setText(u'切换到一号输入源')
        else:
            self.full_screen_show_id = 1
            self.switch_Button.setText(u'切换到二号输入源')


    def open_camera(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_1)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.cap_size[0])
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cap_size[1])

            if flag == False:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请检测相机与电脑是否连接正确", buttons=QtWidgets.QMessageBox.Ok,
                                                defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                self.timer_camera.start(40)
                self.det_Button.setText(u'关闭输入源')
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.image_View.clear()
            self.det_Button.setText(u'打开输入源')


    def show_camera(self):
        flag, image = self.cap.read()

        if self.full_screen_show_id == 1:
            self.show_full_screen(image)

        show = cv2.resize(image, (640, 480))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.image_View.setPixmap(QtGui.QPixmap.fromImage(showImage))

        
    def open_camera_2(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap_2.open(self.CAM_2)
            self.cap_2.set(cv2.CAP_PROP_FRAME_WIDTH, self.cap_2_size[0])
            self.cap_2.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cap_2_size[1])

            if flag == False:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请检测输入源与电脑是否连接正确", buttons=QtWidgets.QMessageBox.Ok,
                                                defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                self.timer_camera_2.start(40)
                self.det_Button_2.setText(u'关闭输入源')
        else:
            self.timer_camera_2.stop()
            self.cap_2.release()
            self.image_View_2.clear()
            self.det_Button_2.setText(u'打开输入源')


    def show_camera_2(self):
        flag, image = self.cap_2.read()

        if self.full_screen_show_id == 2:
            self.show_full_screen(image)

        show = cv2.resize(image, (640, 480))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.image_View_2.setPixmap(QtGui.QPixmap.fromImage(showImage))


    def show_full_screen(self, img):
        full_screen_img = cv2.resize(img, (full_screen_width, full_screen_height))
        window_name = 'projector'
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow(window_name, full_screen_img)
        cv2.waitKey(1)


if __name__ == '__main__':

    app = QApplication(sys.argv)  
    ex = Q_Window()  
    sys.exit(app.exec_())

