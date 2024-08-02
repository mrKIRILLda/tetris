from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
import socket
import time

import rfkmrekznjh
import tetris
import os


# import server


def find(raw: str):
    first = None
    for num, sign in enumerate(raw):
        if sign == "<":
            first = num
        if sign == ">" and first is not None:
            second = num
            result = list(raw[first + 1:second].split(","))
            return result
    return ""


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(420, 671)
        MainWindow.setMinimumSize(QtCore.QSize(420, 671))
        MainWindow.setMaximumSize(QtCore.QSize(420, 671))
        MainWindow.setWindowIcon(QtGui.QIcon('a.ico'))

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 10, 421, 81))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 180, 431, 31))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(0, 270, 431, 31))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(0, 360, 431, 31))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")

        self.ip_row = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.ip_row.setGeometry(QtCore.QRect(70, 210, 301, 31))
        self.ip_row.setObjectName("ip_row")

        self.name_row = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.name_row.setGeometry(QtCore.QRect(70, 300, 301, 31))
        self.name_row.setObjectName("name_row")

        self.pass_row = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.pass_row.setGeometry(QtCore.QRect(70, 390, 301, 31))
        self.pass_row.setObjectName("pass_row")

        self.enter_button = QtWidgets.QPushButton(parent=self.centralwidget)
        self.enter_button.setGeometry(QtCore.QRect(110, 510, 221, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.enter_button.setFont(font)
        self.enter_button.setObjectName("enter_button")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Вход в игру"))
        self.label.setText(_translate("MainWindow",
                                      "<html><head/><body><p><span style=\" font-size:26pt; color:#ffffff;\">Вход в "
                                      "игру</span></p><p><br/></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "IP-адрес"))
        self.label_3.setText(_translate("MainWindow", "Никнейм"))
        self.label_4.setText(_translate("MainWindow", "Пароль"))
        self.enter_button.setText(_translate("MainWindow", "Вход"))


class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.name = None
        self.pasw = None
        self.ip = None
        self.port = None
        self.score = 0
        self.setupUi(self)
        # self.enter_button.clicked.connect(self.ip_check)
        self.enter_button.clicked.connect(self.connect)

    def ip_check(self):
        row = self.ip_row.text()
        if not (':' in row and '.' in row):
            return False
        self.ip, self.port = row.split(':')[0], row.split(':')[1]
        self.ip = self.ip.split('.')
        if not (self.port.isnumeric() and 1024 <= int(self.port) <= 65535):
            return False
        for i in self.ip:
            if not (i.isnumeric() and 0 <= int(i) <= 255 and len(self.ip) == 4):
                return False
        return True

    def empty_check(self):
        self.name = self.name_row.text()
        self.pasw = self.pass_row.text()

        if self.name == '':
            if self.pasw == '':
                return False, False
            return False, True

        elif self.pasw == '':
            if self.name == '':
                return False, False
            return True, False

        else:
            return True, True

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Настройка сокета
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Отключение пакетирования

        empty = self.empty_check()
        if not all(empty):
            wrong = QMessageBox()
            wrong.setWindowTitle("Внимание!")
            wrong.setText("Поля пустые")
            wrong.setIcon(QMessageBox.Icon.Warning)
            wrong.exec()
            return


        if not self.ip_check():
            print('IP не верен')
            wrong = QMessageBox()
            wrong.setWindowTitle("Внимание!")
            wrong.setText("IP не верен")
            wrong.setIcon(QMessageBox.Icon.Warning)
            wrong.exec()
            return

        self.ip = '.'.join(self.ip)
        self.port = int(self.port)

        try:
            sock.connect((self.ip, self.port))
            info = f'<{self.name},{self.pasw}>'.encode()
            sock.send(info)
        except:
            print('Не смог подключиться')
            wrong = QMessageBox()
            wrong.setWindowTitle("Внимание!")
            wrong.setText("Не смог подключиться")
            wrong.setIcon(QMessageBox.Icon.Warning)
            wrong.exec()
            return

        tick = 0
        while True:
            try:
                data = sock.recv(1024).decode()
                data = find(data)
                if int(data[0]) >= 0:
                    self.start_game()
                    return
                if data[0] == "0":
                    return
                elif data[0] == "-1":
                    wrong = QMessageBox()
                    wrong.setWindowTitle("Внимание!")
                    wrong.setText("Неправильный пароль. Попробуйте ещё раз.")
                    wrong.setIcon(QMessageBox.Icon.Warning)
                    wrong.exec()
                    return
                else:
                    return


            except:
                tick += 1
                print("Ошибка №" + str(tick))
                time.sleep(0.5)
                if tick == 20:
                    return

    def start_game(self):
        self.tetris = tetris.Tetris(self, app)
        self.tetris.show()
        self.close()

    def showEvent(self, event):
        print(self.score)
        if self.score == 0:
            return

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        try:
            sock.connect((self.ip, self.port))
            info = f"<final,{self.name},{self.pasw},{self.score}>".encode()
            sock.send(info)
        except:
            print("Не смог подключиться")
            return


stylesheet = """ 
QMainWindow { 
        background-image: url("login6.jpeg"); 
        background-repeat: no-repeat; 
        background-position: center; 
} """

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    w = Window()
    w.show()
    sys.exit(app.exec())
