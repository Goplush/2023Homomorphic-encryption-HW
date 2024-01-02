# -*- coding: utf-8 -*-


'''
登录界面设计
'''

import sys
from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import (QWidget, QWidget, QLabel, QLineEdit,
                        QGridLayout, QVBoxLayout, QHBoxLayout,
                        QFrame, QMessageBox, QPushButton,
                        QApplication)
from PyQt5.QtGui import QFont, QIcon, QPixmap

import util

import os 
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..')) #当前python程序所在目录的父目录的绝对路径加入到环境变量PYTHON_PATH中
from Database.util import login # PYTHON_PATH是python的搜索路径，再引入模块时就可以从父目录中搜索得到了

class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.el_mainWindow = None
        self.pa_mainWindow = None
        self.registerWindow = None
        self.patternWindow = None
        self.initUI()

    def initUI(self): 
        
        logomap = QPixmap('./image/signin.png')

        logolbl = QLabel(self)
        logolbl.setPixmap(logomap)
        logolbl.setScaledContents(True) # 图片自适应标签大小

        title = QLabel('Evote—电子投票系统')
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Microsoft YaHei", 15))

        user = QLabel('账号: ')
        pwd = QLabel('密码: ')

        user = QLabel('账号: ')
        pwd = QLabel('密码: ')

        self.userInput = QLineEdit()
        self.userInput.setPlaceholderText('请输入用户名')

        self.pwdInput = QLineEdit()
        self.pwdInput.setPlaceholderText('请输入密码')
        self.pwdInput.setEchoMode(QLineEdit.Password) #密码不以明文显示

        self.loginButton = QPushButton('登录', self)
        self.loginButton.setIcon(QIcon('./image/start.png'))
        self.loginButton.clicked.connect(self.onLogin)

        self.registerButton = QPushButton('注册', self)
        self.registerButton.setFont(QFont('黑体'))
        self.registerButton.setIcon(QIcon('./image/register.png'))
        self.registerButton.clicked.connect(self.onRegister)

        rightcenterLayout = QGridLayout()
        rightcenterLayout.addWidget(user, 0, 0, 1, 1)
        rightcenterLayout.addWidget(pwd, 1, 0, 1, 1)
        rightcenterLayout.addWidget(self.userInput, 0, 1, 1, 3)
        rightcenterLayout.addWidget(self.pwdInput, 1, 1, 1, 3)

        rightcenterFrame = QFrame()
        rightcenterFrame.setFrameShape(QFrame.WinPanel)
        rightcenterFrame.setLayout(rightcenterLayout)

        rightdownLayout = QHBoxLayout()
        rightdownLayout.addWidget(self.loginButton)
        rightdownLayout.addWidget(self.registerButton)

        rightLayout = QVBoxLayout()
        rightLayout.addWidget(title)
        rightLayout.addWidget(rightcenterFrame)
        rightLayout.addLayout(rightdownLayout)

        totalLayut = QHBoxLayout()
        totalLayut.addWidget(logolbl)
        totalLayut.addLayout(rightLayout)

        self.setLayout(totalLayut)
        self.resize(480, 200)
        util.center(self) 
        self.setFont(QFont('宋体', 12))
        self.setWindowTitle('登录')
        self.setWindowIcon(QIcon('./image/car.png'))

        self.setWindowFlags(Qt.FramelessWindowHint)  # 去边框
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        button_red = QPushButton(self)
        button_red.move(20, 20)
        button_red.setFixedSize(20, 20)
        button_red.setStyleSheet("QPushButton{\n"
                                 "    background:#CE0000;\n"
                                 "    color:white;\n"
                                 "    border-radius: 10px;\n"
                                 "}\n"
                                 "QPushButton:hover{                    \n"
                                 "    background:red;\n"
                                 "}\n"
                                 "QPushButton:pressed{\n"
                                 "    border: 1px solid #3C3C3C!important;\n"
                                 "    background:black;\n"
                                 "}")
        button_red.clicked.connect(self.quit_button)

        button_orange = QPushButton(self)
        button_orange.move(50, 20)
        button_orange.setFixedSize(20, 20)
        button_orange.setStyleSheet("QPushButton{\n"
                                    "    background:orange;\n"
                                    "    color:white;\n"
                                    "    border-radius: 10px;\n"
                                    "}\n"
                                    "QPushButton:hover{                    \n"
                                    "    background:yellow;\n"
                                    "}\n"
                                    "QPushButton:pressed{\n"
                                    "    border: 1px solid #3C3C3C!important;\n"
                                    "    background:black;\n"
                                    "}")

        button_green = QPushButton(self)
        button_green.move(80, 20)
        button_green.setFixedSize(20, 20)
        button_green.setStyleSheet("QPushButton{\n"
                                   "    background:green;\n"
                                   "    color:white;\n"
                                   "    border-radius: 10px;\n"
                                   "}\n"
                                   "QPushButton:hover{                    \n"
                                   "    background:#08BF14;\n"
                                   "}\n"
                                   "QPushButton:pressed{\n"
                                   "    border: 1px solid #3C3C3C!important;\n"
                                   "    background:black;\n"
                                   "}")

    def quit_button(self):
        quit()

    def onLogin(self):

        usr = self.userInput.text()
        pwd = self.pwdInput.text()

        if usr == '':
            QMessageBox.warning(self, 'warning', '用户名不能为空', QMessageBox.Yes)
        elif pwd == '':
            QMessageBox.warning(self, 'warning', '请输入密码', QMessageBox.Yes)
        else:
            flag = login(usr, pwd)
            if flag == 1:
                # if self.mainWindow is not None:
                #     self.close()
                #     self.mainWindow.usr = usr
                #     self.mainWindow.showbottom()
                #     self.mainWindow.show()
                #     # self.patternWindow.show()
                if self.patternWindow is not None:
                    self.close()
                    # self.el_mainWindow.usr= usr
                    # self.pa_mainWindow.usr = usr
                    self.patternWindow.usr = usr
                    self.patternWindow.show()

            elif flag == 0:

                QMessageBox.information(self, 'sorry', '程序出了点bug', QMessageBox.Yes)
            elif flag == -1:
                QMessageBox.warning(self, 'warning', '用户不存在, 请先注册', QMessageBox.Yes)
            else:
                QMessageBox.warning(self, 'warning', '密码错误', QMessageBox.Yes)
        
        self.userInput.clear()
        self.pwdInput.clear()
    
    def onRegister(self):

        if self.registerWindow is not None:
            self.userInput.clear()
            self.pwdInput.clear()
            self.close()
            self.registerWindow.show() 

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    LoginWindow = LoginWindow()
    LoginWindow.show()
    sys.exit(app.exec_())




