# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor

# init, sys.argv -- command arguments
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Pimp My Ride")
window.setFixedWidth(1200)
window.setFixedHeight(800)
window.setStyleSheet("background: 'black';")

# grid layout
grid = QGridLayout()
grid.setContentsMargins(0, 0, 0, 200)


def frame():
    # display logo
    image = QPixmap("logo.png")
    logo = QLabel()     # creating label widget
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignHCenter)
    logo.setStyleSheet("margin-top: 100px;")

    # button widget
    button = QPushButton("Dalej")
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet(
        "*{border: 4px solid '#FBE405';" +
        "border-radius: 45px;" +
        "font-size: 35px;" +
        "color: 'white';" +
        "padding: 25px 0;}" +
        "*:hover{background: '#16B3D3';}"
    )

    grid.addWidget(logo, 0, 0, 0, 3)  # (row, column, row_span, column_span)
    grid.addWidget(button, 1, 1, 1, 1)


frame()

# applying this grid on layout
window.setLayout(grid)

# displaying window
window.show()
# terminate app
sys.exit(app.exec())
