# -*- coding: utf-8 -*-
# @Time    : 2022-09-01 12:19
# @Author  : gzzz
# @FileName: keyGen_pail.py
# @Software: PyCharm
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QVBoxLayout, QHBoxLayout,
                             QFileDialog,
                             QMessageBox, QPushButton,
                             QApplication)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import QRegExp

import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))

from APP.util import center
from HE.paillier import keyGen_Pai, save_key, load_key


class PA_KeyGenWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        title_PA = QLabel(self)
        title_PA.setText('Paillier')
        keysize = QLabel('请输入密钥长度: ')
        self.keysizeInput = QLineEdit()
        self.keysizeInput.setPlaceholderText('1024')
        intValidator = QIntValidator()
        intValidator.setRange(512, 2147483647)
        self.keysizeInput.setValidator(intValidator)

        self.confirmButton = QPushButton('生成')
        self.confirmButton.setFont(QFont('黑体'))
        self.confirmButton.setIcon(QIcon('../image/confirm.png'))
        self.confirmButton.clicked.connect(self.onConfirm)

        tophox = QHBoxLayout()
        tophox.addWidget(keysize)
        tophox.addWidget(self.keysizeInput)

        downhox = QHBoxLayout()
        downhox.addStretch(1)
        downhox.addWidget(self.confirmButton)
        downhox.addStretch(1)

        totalLayout = QVBoxLayout()
        # totalLayout.addLayout(title_PA)
        totalLayout.addLayout(tophox)
        totalLayout.addLayout(downhox)

        self.setLayout(totalLayout)

        center(self)
        self.resize(325, 150)
        self.setWindowTitle('密钥生成')
        self.setWindowIcon(QIcon('../image/keyGen_Elg.png'))

    def savekey(self, key, filename='', mode=0):
        '''
        mode 0 公钥 / 1 私钥
        '''
        filename = QFileDialog.getSaveFileName(self, 'save', './key/' + filename, "Text Files(*.txt)")
        if len(filename[0]):
            try:
                ok = save_key(key, filename[0], mode)
                return True
            except Exception as e:
                print(e)
                return False
        return False

    def onConfirm(self):
        keysize = self.keysizeInput.text()
        keysize = int(keysize)
        if keysize == 0:
            QMessageBox.warning(self, 'warning', '密钥长度不能为零', QMessageBox.Yes)
        else:
            if keysize < 128:
                QMessageBox.warning(self, 'warning', '密钥长度低于128不太适合安全加密', QMessageBox.Yes)
            (pubkey, privkey) = keyGen_Pai(keysize)
            QMessageBox.information(self, 'save', '准备开始保存公钥', QMessageBox.Yes)
            filename = 'public_key.txt'
            if self.savekey(pubkey, filename, 0) == True:
                QMessageBox.information(self, 'congratulation', '公钥保存成功', QMessageBox.Yes)
                QMessageBox.information(self, 'save', '准备开始保存私钥', QMessageBox.Yes)
                filename = 'private_key.txt'
                if self.savekey(privkey, filename, 1) == True:
                    QMessageBox.information(self, 'congratulation', '私钥保存成功', QMessageBox.Yes)


def openPA_Key(widget, mode=0):
    '''
    # 功能：打开密钥
    # 接受参数：
    widget: 可视化组件
    mode(0, 1): 0代表加载公钥, 1代表加载的是私钥
    # 返回参数：
    如果有选择文件返回对应的公钥类或者私钥类
    否则返回False
    '''
    filename = QFileDialog.getOpenFileName(widget, 'Open Key File', './home', '(*.txt)')
    if filename[0]:
        return load_key(filename[0], mode)
    return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    keyGenWindow = PA_KeyGenWindow()
    # keyGenWindow.show()
    # print(openKey(keyGenWindow))
    sys.exit(app.exec_())