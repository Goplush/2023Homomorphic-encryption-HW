# -*- coding: utf-8 -*-

'''
应用窗口主程序
'''


import sys
from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import (QMainWindow, QWidget, QLabel, QLineEdit,
                        QGridLayout, QVBoxLayout, QHBoxLayout,
                        QFrame, QMessageBox, QPushButton,
                        QAction,
                        QApplication)
from PyQt5.QtGui import QFont, QIcon
import patternWindow
import login
import register
import util
import os 
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))
from KeyGen.keyGen_Elg import EL_KeyGenWindow
from KeyGen.keyGen_pail import PA_KeyGenWindow
from Launch.launch import EL_LaunchWindow,PA_LaunchWindow
from Vote.vote import EL_VoteWindow,PA_VoteWindow
from View.view import PA_ViewWindow,EL_ViewWindow
from Test import test


class EL_CenterWidget(QWidget):
    
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)
        self.initUI(parent)
        self.EL_keyGenWindows = []
        self.launchWindows = []
        self.voteWindows = []
        self.EL_viewWindows = []


    def initUI(self, parent):

        keyGenButton = QPushButton('密钥生成', self)
        keyGenButton.setIcon(QIcon('../image/keyGen.png'))
        keyGenButton.setStyleSheet("QPushButton{color:black}"
                                "QPushButton:hover{color:red}")
        keyGenButton.clicked.connect(lambda: self.EL_onkeyGen(parent))

        launchButton = QPushButton('发起投票', self)
        launchButton.setIcon(QIcon('../image/launch.png'))
        launchButton.setStyleSheet("QPushButton{color:black}"
                                "QPushButton:hover{color:red}")
        launchButton.clicked.connect(lambda: self.onLaunch(parent))

        voteButton = QPushButton('进行投票', self)
        voteButton.setIcon(QIcon('../image/vote.jpg'))
        voteButton.setStyleSheet("QPushButton{color:black}"
                                "QPushButton:hover{color:red}")
        voteButton.clicked.connect(lambda : self.onVote(parent))

        viewButton = QPushButton('查看投票', self)
        viewButton.setIcon(QIcon('../image/view.png'))
        viewButton.setStyleSheet("QPushButton{color:black}"
                                "QPushButton:hover{color:red}")
        viewButton.clicked.connect(lambda: self.onView(parent))

        vbox = QVBoxLayout()
        vbox.addWidget(keyGenButton)
        vbox.addWidget(launchButton)
        vbox.addWidget(voteButton)
        vbox.addWidget(viewButton)

        midhobx = QHBoxLayout()
        midhobx.addStretch(1)
        midhobx.addLayout(vbox)
        midhobx.addStretch(1)

        centerFrame = QFrame(self)
        centerFrame.setFrameShape(QFrame.WinPanel)
        centerFrame.setLayout(midhobx)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(centerFrame)
        hbox.addStretch(1)
        hbox.setStretchFactor(centerFrame, 6)
        self.setLayout(hbox)

    def EL_onkeyGen(self, parent):
        if parent is not None:

            self.EL_keyGenWindows.append(EL_KeyGenWindow())
            self.EL_keyGenWindows[-1].show()
            parent.showMinimized()

    def onLaunch(self, parent):
        if parent is not None:
            self.launchWindows.append(EL_LaunchWindow(parent.usr))
            self.launchWindows[-1].show()
            parent.showMinimized()
    
    def onVote(self, parent):
        if parent is not None:
            self.voteWindows.append(EL_VoteWindow(parent.usr))
            self.voteWindows[-1].show()
            parent.showMinimized()

    def onView(self, parent):
        if parent is not None:
            self.EL_viewWindows.append(EL_ViewWindow(parent.usr))
            self.EL_viewWindows[-1].show()
            parent.showMinimized()


class EL_MainWindow(QMainWindow):

    def __init__(self, usr=None):
        super().__init__()
        self.usr = usr
        self.loginWindow = None 
        self.initUI()
    
    def initUI(self):
        
        #中心布局
        self.setCentralWidget(EL_CenterWidget(self))

        #菜单栏设置
        menu = self.menuBar().addMenu('应用操作')

        signoutAct = QAction('注销', self) 
        signoutAct.triggered.connect(self.onSignout)
        menu.addAction(signoutAct)

        exitAct = QAction('退出', self)
        exitAct.triggered.connect(self.onExit)
        menu.addAction(exitAct)

        #整体布局
        self.resize(750, 600)
        util.center(self)
        self.setFont(QFont("Microsoft YaHei", 11))
        self.setWindowTitle('ElGamal乘法同态加密')
        self.setWindowIcon(QIcon('./image/user.png'))
        
        self.bottomlbl = QLabel()
        self.bottomlbl.setFont(QFont("宋体"))
        self.statusBar().addPermanentWidget(self.bottomlbl)
        self.showbottom()

    def showbottom(self):
        #设置底部状态栏, 显示当前登录的用户
        if self.usr is not None:
            s = "Welcome: " + self.usr
            self.bottomlbl.setText(s)
        
    #注销重新登录
    def onSignout(self):
        if self.loginWindow is not None:
            self.close()
            self.loginWindow.show()
    
    def onExit(self):
        self.close()


class PA_CenterWidget(QWidget):

    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)
        self.initUI(parent)
        self.PA_keyGenWindows = []
        self.launchWindows = []
        self.voteWindows = []
        self.PA_viewWindows = []

    def initUI(self, parent):

        keyGenButton = QPushButton('密钥生成', self)
        keyGenButton.setIcon(QIcon('../image/keyGen.png'))
        keyGenButton.setStyleSheet("QPushButton{color:black}"
                                   "QPushButton:hover{color:red}")
        keyGenButton.clicked.connect(lambda: self.PA_onkeyGen(parent))

        launchButton = QPushButton('发起投票', self)
        launchButton.setIcon(QIcon('../image/launch.png'))
        launchButton.setStyleSheet("QPushButton{color:black}"
                                   "QPushButton:hover{color:red}")
        launchButton.clicked.connect(lambda: self.onLaunch(parent))

        voteButton = QPushButton('进行投票', self)
        voteButton.setIcon(QIcon('../image/vote.jpg'))
        voteButton.setStyleSheet("QPushButton{color:black}"
                                 "QPushButton:hover{color:red}")
        voteButton.clicked.connect(lambda: self.onVote(parent))

        viewButton = QPushButton('查看投票', self)
        viewButton.setIcon(QIcon('../image/view.png'))
        viewButton.setStyleSheet("QPushButton{color:black}"
                                 "QPushButton:hover{color:red}")
        viewButton.clicked.connect(lambda: self.onView(parent))

        vbox = QVBoxLayout()
        vbox.addWidget(keyGenButton)
        vbox.addWidget(launchButton)
        vbox.addWidget(voteButton)
        vbox.addWidget(viewButton)

        midhobx = QHBoxLayout()
        midhobx.addStretch(1)
        midhobx.addLayout(vbox)
        midhobx.addStretch(1)

        centerFrame = QFrame(self)
        centerFrame.setFrameShape(QFrame.WinPanel)
        centerFrame.setLayout(midhobx)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(centerFrame)
        hbox.addStretch(1)
        hbox.setStretchFactor(centerFrame, 6)
        self.setLayout(hbox)

    def PA_onkeyGen(self, parent):
        if parent is not None:
            self.PA_keyGenWindows.append(PA_KeyGenWindow())
            self.PA_keyGenWindows[-1].show()
            parent.showMinimized()

    def onLaunch(self, parent):
        if parent is not None:
            self.launchWindows.append(PA_LaunchWindow(parent.usr))
            self.launchWindows[-1].show()
            parent.showMinimized()

    def onVote(self, parent):
        if parent is not None:
            self.voteWindows.append(PA_VoteWindow(parent.usr))
            self.voteWindows[-1].show()
            parent.showMinimized()

    def onView(self, parent):
        if parent is not None:
            self.PA_viewWindows.append(PA_ViewWindow(parent.usr))
            self.PA_viewWindows[-1].show()
            parent.showMinimized()


class PA_MainWindow(QMainWindow):

    def __init__(self, usr=None):
        super().__init__()
        self.usr = usr
        self.loginWindow = None
        self.initUI()

    def initUI(self):

        # 中心布局
        self.setCentralWidget(PA_CenterWidget(self))

        # 菜单栏设置
        menu = self.menuBar().addMenu('应用操作')

        signoutAct = QAction('注销', self)
        signoutAct.triggered.connect(self.onSignout)
        menu.addAction(signoutAct)

        exitAct = QAction('退出', self)
        exitAct.triggered.connect(self.onExit)
        menu.addAction(exitAct)

        # 整体布局
        self.resize(750, 600)
        util.center(self)
        self.setFont(QFont("Microsoft YaHei", 11))
        self.setWindowTitle('Paillier加法同态加密')
        self.setWindowIcon(QIcon('./image/user.png'))

        self.bottomlbl = QLabel()
        self.bottomlbl.setFont(QFont("宋体"))
        self.statusBar().addPermanentWidget(self.bottomlbl)
        self.showbottom()

    def showbottom(self):
        # 设置底部状态栏, 显示当前登录的用户
        if self.usr is not None:
            s = "Welcome: " + self.usr
            self.bottomlbl.setText(s)

    # 注销重新登录
    def onSignout(self):
        if self.loginWindow is not None:
            self.close()
            self.loginWindow.show()

    def onExit(self):
        self.close()


def main():
    
    app = QApplication(sys.argv)


    loginWindow = login.LoginWindow()
    registerWindow = register.RegisterWindow()
    testWindow = test.MainWindow()

    el_mainWindow = EL_MainWindow()
    pa_mainWindow = PA_MainWindow()

    vPatternWindow = patternWindow.PatternWindow()

    # mainWindow.loginWindow = loginWindow
    registerWindow.loginWindow = loginWindow
    loginWindow.registerWindow = registerWindow
    loginWindow.testWindow = testWindow

    vPatternWindow.EL_MainWindow = el_mainWindow
    vPatternWindow.PA_MainWindow = pa_mainWindow
    loginWindow.patternWindow = vPatternWindow

    loginWindow.show()
    sys.exit(app.exec_())



if __name__=="__main__":
    main()