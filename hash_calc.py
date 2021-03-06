#!/usr/bin/env python3

import sys
import os
from PyQt5 import uic, QtGui
from back import HashCalc, CheckEvent
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import (QMessageBox,
                             QMainWindow, QApplication, QLabel, QStackedWidget, QComboBox, QFileDialog)

mainwindow = uic.loadUiType(os.path.join("ui", "hash_calc.ui"))


class Main(*mainwindow):

    # In charge of emitting the file path
    trigger_file = pyqtSignal(CheckEvent)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.icono = QtGui.QIcon()
        self.icono.addFile(os.path.join("ui", "hashtag.svg"))
        self.setWindowIcon(self.icono)
        self.selectedFile = None
        self.back = HashCalc(self)
        self.comboHash.addItems(self.back.methods.keys())
        self.trigger_file.connect(self.back.checksum)
        self.fileButton.clicked.connect(self.getfile)
        self.verifyButton.clicked.connect(self.verify)
        self.show()

    def getfile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file')
        self.selectedFile = fname[0]

    def display_result(self, boolean):
        message = "Sums match" if boolean else "Sums do not match"
        msg = QMessageBox.information(
            self, "Message", message, QMessageBox.Ok, QMessageBox.Ok)

    def verify(self):
        if self.selectedFile:
            mode = self.comboHash.currentText()
            _hash = self.hashEdit.text().strip().upper()
            self.trigger_file.emit(CheckEvent(self.selectedFile, mode, _hash))
        else:
            msg = QMessageBox.information(
                self, "Message", "No file was selected", QMessageBox.Ok, QMessageBox.Ok)


def main():
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
