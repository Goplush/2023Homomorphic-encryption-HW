# -*- coding: utf-8 -*-


'''
同态加密模式选择
'''

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QWidget, QLabel, QLineEdit,
                             QGridLayout, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QFrame, QMessageBox, QPushButton,
                             QApplication, QMainWindow)
from PyQt5.QtGui import QFont, QIcon, QPixmap

import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))


class PatternWindow(QWidget):

    def __init__(self, usr=None):
        super().__init__(parent=usr)
        self.EL_MainWindow = None
        self.PA_MainWindow = None
        self.registerWindow = None
        self.usr = usr
        self.initUI(usr)

    def initUI(self, parent):
        self.choosepatternbtn1 = QPushButton(self)
        self.choosepatternbtn1.setText("ElGama乘法同态加密")
        self.choosepatternbtn1.setFixedSize(200, 100)
        self.choosepatternbtn1.setStyleSheet("QPushButton{\n"
                                             "    background:orange;\n"
                                             "    color:white;\n"
                                             "    box-shadow: 1px 1px 3px;font-size:18px;border-radius: 30px;font-family: 微软雅黑;\n"
                                             "}\n"
                                             "QPushButton:pressed{\n"
                                             "    background:red;\n"
                                             "}")

        self.choosepatternbtn1.clicked.connect(self.onchoose_EL)

        self.choosepatternbtn2 = QPushButton(self)
        self.choosepatternbtn2.setText("Paillier加法同态加密")
        self.choosepatternbtn2.setFixedSize(200, 100)
        self.choosepatternbtn2.setStyleSheet("QPushButton{\n"
                                             "    background:green;\n"
                                             "    color:white;\n"
                                             "    box-shadow: 1px 1px 3px;font-size:18px;border-radius: 30px;font-family: 微软雅黑;\n"
                                             "}\n"
                                             "QPushButton:pressed{\n"
                                             "    background:red;\n"
                                             "}")

        self.choosepatternbtn2.clicked.connect(self.onchoose_PA)

        hbox = QHBoxLayout()
        hbox.addStretch(10)
        hbox.addWidget(self.choosepatternbtn1)
        hbox.addStretch(10)
        hbox.addWidget(self.choosepatternbtn2)
        hbox.addStretch(10)

        # 设置控件与控件之间的水平间距

        self.setLayout(hbox)

        centerFrame = QFrame(self)
        centerFrame.setFrameShape(QFrame.WinPanel)
        centerFrame.setLayout(hbox)

        totalLayout = QVBoxLayout()
        totalLayout.addWidget(centerFrame)

        self.setLayout(totalLayout)

        self.resize(950, 700)

        # center(self)
        self.setFont(QFont('宋体', 10))
        self.setWindowTitle('Patterns selection')
        self.setWindowIcon(QIcon('../image/record.png'))

    def onchoose_EL(self):
        self.EL_MainWindow.usr = self.usr
        self.EL_MainWindow.show()

        # self.close()

    def onchoose_PA(self):
        self.PA_MainWindow.usr = self.usr
        self.PA_MainWindow.show()
        # self.close()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    patternWindow = PatternWindow()
    patternWindow.show()
    sys.exit(app.exec_())

