# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import glob
from utils import read_wav
from PyQt5 import QtCore, QtGui, QtWidgets
from playsound import playsound
from interface import ModelInterface
m,f= None, None

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(389, 250)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.ln_model = QtWidgets.QLineEdit(self.centralwidget)
        self.ln_model.setObjectName("ln_model")
        self.gridLayout.addWidget(self.ln_model, 0, 1, 1, 1)
        self.ln_predict = QtWidgets.QLineEdit(self.centralwidget)
        self.ln_predict.setObjectName("ln_predict")
        self.gridLayout.addWidget(self.ln_predict, 4, 1, 1, 1)
        self.ln_wav = QtWidgets.QLineEdit(self.centralwidget)
        self.ln_wav.setObjectName("ln_wav")
        self.gridLayout.addWidget(self.ln_wav, 1, 1, 1, 1)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 3, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.btn_load = QtWidgets.QPushButton(self.centralwidget)
        self.btn_load.setObjectName("btn_load")
        self.gridLayout.addWidget(self.btn_load, 0, 2, 1, 1)
        self.btn_open = QtWidgets.QPushButton(self.centralwidget)
        self.btn_open.setObjectName("btn_open")
        self.gridLayout.addWidget(self.btn_open, 1, 2, 1, 1)
        self.btn_play = QtWidgets.QPushButton(self.centralwidget)
        self.btn_play.setObjectName("btn_play")
        self.gridLayout.addWidget(self.btn_play, 2, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 389, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        # Su kien
        self.btn_load.clicked.connect(lambda:self.load_model(MainWindow))
        self.btn_open.clicked.connect(lambda:self.load_wav(MainWindow))
        self.btn_play.clicked.connect(self.play_predict)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    def load_model(self,MainWindow):
        global m
        fileName = QtWidgets.QFileDialog().getOpenFileName(MainWindow, "Load Model", "", "Model File (*.out)")
        print(fileName[0])
        self.ln_model.setText(fileName[0])
        m = ModelInterface.load(fileName[0])

    def load_wav(self, MainWindow):
        global f
        fileName = QtWidgets.QFileDialog().getOpenFileName(MainWindow, "Open file wav", "", "Wav File (*.wav)")
        self.ln_wav.setText(fileName[0])
        f = glob.glob(fileName[0])

    def play_wav(self):
        playsound(self.ln_wav.text())

    def pre_dict(self):
        fs, signal = read_wav(f[0])
        label, score = m.predict(fs, signal)
        self.ln_predict.setText(label)

    def play_predict(self):
        self.pre_dict()
        self.play_wav()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Model:"))
        self.label_2.setText(_translate("MainWindow", "File WAV:"))
        self.label_3.setText(_translate("MainWindow", "Predict:"))
        self.btn_load.setText(_translate("MainWindow", "Load"))
        self.btn_open.setText(_translate("MainWindow", "Open"))
        self.btn_play.setText(_translate("MainWindow", "Play"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

