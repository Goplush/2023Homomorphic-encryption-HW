import sys
sys.path.append("..")
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QDialog, QHBoxLayout
from HE.paillier_test import integrated_testing

class TestDialog(QDialog):
    def __init__(self, test_name, parent=None):
        super(TestDialog, self).__init__(parent)
        self.setWindowTitle(test_name + "测试")
        self.setFixedSize(200, 100)
        
        self.label = QLabel("测试中")
        self.ok_button = QPushButton("确定")

        self.ok_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    #mode0 Elgamal;mode1 Paillier
    def test_exec(self,mode=0):
        self.show()
        integrated_testing()
        self.label.setText("测试完毕，测试结果请查看日志")
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