import sys
from time import sleep
sys.path.append("..")
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QDialog, QHBoxLayout
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QPushButton

from HE.paillier_test import integrated_testing
from HE.ElGamaltest import test

class TestDialog(QDialog):
    def __init__(self, test_name, parent=None):
        super(TestDialog, self).__init__(parent)
        self.setWindowTitle(test_name + "测试")
        self.setFixedSize(300, 200)
        
        self.label = QLabel("测试中，测试包含长密钥生成，请耐心等待")
        self.ok_button = QPushButton("确定")

        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setDisabled(True)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    #mode0 Elgamal;mode1 Paillier
    def test_exec(self,mode=1):
        if mode == 1:
             integrated_testing()
        else:
            def show_confirmation_dialog():
                dialog = QMessageBox()

                dialog.setWindowTitle("是否进行测试")
                dialog.setText("该测试要消耗大量时间，请问是否确定？")

                yes_button = QPushButton("是")
                no_button = QPushButton("否")

                dialog.addButton(yes_button, QMessageBox.YesRole)
                dialog.addButton(no_button, QMessageBox.NoRole)

                result = dialog.exec_()

                if result == QMessageBox.YesRole:
                    print("用户选择了是")
                    return True
                else:
                    print("用户选择了否")
                    return False
            if show_confirmation_dialog():
                test()
            else:
                return

        self.label.setText("测试完毕，测试结果请查看日志")
        self.ok_button.setDisabled(False)
        self.show()

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        # 设置窗口初始大小
        self.setFixedSize(400, 300)  # 或者使用 self.resize(400, 300)

        self.setWindowTitle("同态加密测试")

        paillier_button = QPushButton("Paillier测试", self)
        elgamal_button = QPushButton("Elgamal测试", self)

        paillier_button.clicked.connect(self.paillier_test)
        elgamal_button.clicked.connect(self.elgamal_test)

        layout = QVBoxLayout()
        layout.addWidget(paillier_button)
        layout.addWidget(elgamal_button)

        self.setLayout(layout)

        self.setLayout(layout)

    def paillier_test(self):
        dialog = TestDialog("Paillier", self)
        result = dialog.test_exec(1)

        if result == QDialog.Accepted:
            print("Paillier测试：确定")
        else:
            print("Paillier测试：取消")

    def elgamal_test(self):
        dialog = TestDialog("Elgamal", self)
        result = dialog.test_exec(0)

        if result == QDialog.Accepted:
            print("Elgamal测试：确定")
        else:
            print("Elgamal测试：取消")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())