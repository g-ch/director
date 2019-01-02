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
import random
import time

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
        self.switch_game_timer = QtCore.QTimer()

        # Video resolution
        self.cap = cv2.VideoCapture()
        self.cap_size = [1920, 1080]
        self.cap_2 = cv2.VideoCapture()
        self.cap_2_size = [1920, 1080]

        self.CAM_1 = 0
        self.CAM_2 = 1
        self.full_screen_show_id = 1

        # Poster path
        self.poster = cv2.imread('timg.jpeg') 
        self.game_background = 'red.jpeg'
        self.game_question_img = [cv2.imread('877668843.jpg'), cv2.imread('1063312050.jpg'), cv2.imread('1986420780.jpg')]

        # Table list for game
        self.table_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
        self.table_counter = 0
        self.counter_max = len(self.table_list)
        random.shuffle(self.table_list)


    def initUI(self):
        self.image_View = QLabel("image", self)
        self.image_View.resize(640, 480)
        self.image_View.setScaledContents(True)
        self.image_View.move(60, 30)
        jpg = QPixmap('timg.jpeg')
        self.image_View.setPixmap(jpg)

        self.image_View_2 = QLabel("image2", self)
        self.image_View_2.resize(640, 480)
        self.image_View_2.setScaledContents(True)
        self.image_View_2.move(760, 30)
        self.image_View_2.setPixmap(jpg)

        self.image_View_out = QLabel("image_out", self)
        self.image_View_out.resize(320, 240)
        self.image_View_out.setScaledContents(True)
        self.image_View_out.move(700, 620)
        self.image_View_out.setPixmap(jpg)

        self.det_Button = QPushButton(u'打开输入源一', self)
        self.det_Button.clicked.connect(self.open_camera)
        self.det_Button.resize(200, 40)
        self.det_Button.move(360, 520)

        self.det_Button_2 = QPushButton(u'打开输入源二', self)
        self.det_Button_2.clicked.connect(self.open_camera_2)
        self.det_Button_2.resize(200, 40)
        self.det_Button_2.move(900, 520)

        self.switch_Button_1 = QPushButton(u'切换到一号输入源', self)
        self.switch_Button_1.clicked.connect(self.switch_input_1)
        self.switch_Button_1.resize(200, 60)
        self.switch_Button_1.move(400, 600)

        self.switch_Button_2 = QPushButton(u'切换到二号输入源', self)
        self.switch_Button_2.clicked.connect(self.switch_input_2)
        self.switch_Button_2.resize(200, 60)
        self.switch_Button_2.move(400, 670)

        self.switch_Button_3 = QPushButton(u'切换到海报显示', self)
        self.switch_Button_3.clicked.connect(self.switch_poster)
        self.switch_Button_3.resize(200, 60)
        self.switch_Button_3.move(400, 740)

        self.switch_Button_4 = QPushButton(u'切换到桌号选择', self)
        self.switch_Button_4.clicked.connect(self.switch_game)
        self.switch_Button_4.resize(200, 60)
        self.switch_Button_4.move(400, 810)

        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_camera_2.timeout.connect(self.show_camera_2)
        self.switch_game_timer.timeout.connect(self.show_game_result)

        self.setGeometry(300, 300, 1460, 900)
        self.setWindowTitle('ChgDirector')
        self.show()


    def switch_input_1(self):
        self.full_screen_show_id = 1


    def switch_input_2(self):
        self.full_screen_show_id = 2


    def switch_poster(self):
        self.full_screen_show_id = 3
        self.show_full_screen(self.poster)
        self.show_small_window(self.poster)
        

    def switch_game(self):
        self.full_screen_show_id = 4
        seq = random.randint(0, len(self.game_question_img)-1)
        question_img = self.game_question_img[seq]
        self.show_full_screen(question_img)
        self.show_small_window(question_img)

        self.switch_game_timer.start(1000)
        

    def show_game_result(self):
        self.switch_game_timer.stop()
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        place_x = 540
        place_y = 400

        if self.table_list[self.table_counter] > 9:
            place_x -= 100

        background = cv2.imread(self.game_background)
        img_num = cv2.putText(background, str(self.table_list[self.table_counter]), (place_x, place_y), font, 8, (255, 255, 255), 15)
        
        self.table_counter += 1
        if self.table_counter >= self.counter_max:
            self.table_counter = 0

        self.show_full_screen(img_num)
        self.show_small_window(img_num)


    def open_camera(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_1)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.cap_size[0])
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cap_size[1])
            self.cap.set(cv2.CAP_PROP_FPS, 25)

            if flag == False:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请检测相机与电脑是否连接正确",
                                                    buttons=QtWidgets.QMessageBox.Ok,
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
            self.show_small_window(image)

        show = cv2.resize(image, (640, 480))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.image_View.setPixmap(QtGui.QPixmap.fromImage(showImage))


    def open_camera_2(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap_2.open(self.CAM_2)
            self.cap_2.set(cv2.CAP_PROP_FRAME_WIDTH, self.cap_2_size[0])
            self.cap_2.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cap_2_size[1])
            self.cap_2.set(cv2.CAP_PROP_FPS, 25)

            if flag == False:
                msg = QtWidgets.QMessageBox.warning(self, u"Warning", u"请检测输入源与电脑是否连接正确",
                                                    buttons=QtWidgets.QMessageBox.Ok,
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
            self.show_small_window(image)

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


    def show_small_window(self, img):
        out_img = cv2.resize(img, (320, 240))
        out_img = cv2.cvtColor(out_img, cv2.COLOR_BGR2RGB)
        showImage_out = QtGui.QImage(out_img.data, out_img.shape[1], out_img.shape[0], QtGui.QImage.Format_RGB888)
        self.image_View_out.setPixmap(QtGui.QPixmap.fromImage(showImage_out))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Q_Window()
    sys.exit(app.exec_())
