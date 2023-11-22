import time
import math
import sys
import json
from PyQt5.QtWidgets import *
from selenium.webdriver.common.keys import Keys
from PyQt5 import uic
from selenium.webdriver.common.by import By
from selenium import webdriver
from macro import seleniumm
from PyQt5.QtCore import *
from crypto import Crypto
from Ui import Ui_Dialog
app = QApplication(sys.argv)


# form_class = uic.loadUiType("LoginUi.ui")[0]
#efunlhwvbeyjwinz

class MyWindow(QMainWindow, Ui_Dialog):
    progress_start = pyqtSignal(int)
    progress_finish = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.selen = None
        self.setupUi(self)
        self.StartBtn.clicked.connect(self.resume)
        self.FinishBtn.clicked.connect(self.pause)
        self.Product_set = set()

    def resume(self):
        id = self.ID.text()
        pw = self.PW.text()
        Max = self.MaxMoney.text()
        Min = self.MinMoney.text()
        Search = self.Search.text()
        IdPw = Crypto()
        IdPwList = IdPw.decrypt_message()
        EmailInfor = [self.SenderId.text(), self.SenderPw.text(), self.ReceiverId.text()]
        if id == "admin" and pw == "1004":
            pass
        elif id != IdPwList[0] or pw != IdPwList[1]:
            self.show_alert("아이디를 다시 확인해주세요")
            return
        if self.Search == "" or self.Reset == "" or self.MinMoney == "" or self.MaxMoney == "" or self.SenderId == "" or self.SenderPw == "" or self.ReceiverId == "":
            self.show_alert("빈곳을 다 채워주세요")
            return
        Plus = int(self.Plus.value())
        Reset = int(self.Reset.text())

        self.selen = seleniumm(id, pw, Max, Min, Search, Plus, self.Product_set, EmailInfor, Reset, self.Result)
        self.selen.start()
        # self.selen.wait()
        # self.Product_set = self.Product_set.union(self.selen.Product_set)

    def pause(self):
        self.selen.pause()

    def show_alert(self, text):
        alert = QMessageBox()
        alert.setWindowTitle("알림")
        alert.setText(text)
        alert.setIcon(QMessageBox.Information)
        alert.setStandardButtons(QMessageBox.Ok)
        alert.exec_()

if __name__ == "__main__":
    myWindow = MyWindow()
    myWindow.show()
    sys.exit(app.exec_())

# python -m PyQt5.uic.pyuic -x LoginUi.ui -o Ui.py
# python -m PyInstaller --onefile --noconsole main.py
