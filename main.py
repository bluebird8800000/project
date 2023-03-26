#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

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QPushButton, QTextEdit, QVBoxLayout)
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        pixmap = QPixmap('black.jpg')

        lbl_img = QLabel()
        lbl_img.setPixmap(pixmap)
        lbl_size = QLabel()
        lbl_size.setAlignment(Qt.AlignCenter)

        vbox = QVBoxLayout()
        vbox.addWidget(lbl_img)
        vbox.addWidget(lbl_size)
        self.setLayout(vbox)

        btn1 = QPushButton('QUIT', self)
        btn1.resize(btn1.sizeHint())
        btn1.clicked.connect(QCoreApplication.instance().quit)

        grid = QGridLayout()
        self.setLayout(grid)

        grid.addWidget(QLabel('Game:'), 0, 0)
        grid.addWidget(QLabel('PACMAN'), 0, 1)
        grid.addWidget(btn1, 0, 2)

        self.setWindowTitle('QGridLayout')
        self.setGeometry(300, 300, 300, 250)
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_point(qp)
        qp.end()

    def draw_point(self, qp):
        qp.setPen(QPen(Qt.white, 8))
        qp.drawPoint(self.width() / 2, self.height() / 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
