# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QTableWidgetItem

widgets = {
    "logo": [],
    "next_button": [],
    "add_order_button": [],
    "run_algorithm_button": [],
    "show_timetable_button": [],
    "timetable_widget": [],
}

# init, sys.argv -- command arguments
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Pimp My Ride")
window.setFixedWidth(1200)
window.setFixedHeight(900)
window.setStyleSheet("background: #858585;")

# grid layout
grid = QGridLayout()


def set_content_margins(left_margin, top_margin, right_margin, bottom_margin):
    grid.setContentsMargins(left_margin, top_margin, right_margin, bottom_margin)


def display_logo():
    # display logo
    image = QPixmap("logo.png")
    logo = QLabel()     # creating label widget
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignHCenter)
    logo.setStyleSheet("margin-top: 100px;")
    widgets["logo"].append(logo)
    return logo


def clear_widgets():
    for widget in widgets:
        if widgets[widget] != []:  # if not empty -> hide widget
            widgets[widget][-1].hide()
        for i in range(0, len(widgets[widget])):
            widgets[widget].pop()  # remove widgets from global dictionary


def next_on_click():
    clear_widgets()
    menu_frame()


def show_timetable_button_on_click():
    clear_widgets()
    timetable_frame()


def create_button(name):
    button = QPushButton(name)
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet(
        "*{border: 4px solid '#16B3D3';" +
        "border-radius: 45px;" +
        "font-size: 35px;" +
        "font-weight: bold;" +
        "color: 'black';" +
        "padding: 25px 0;" +
        "background: #FBE405;}" +
        "*:hover{background: '#16B3D3';" +
        "color: 'white';" +
        "border: 4px solid '#FBE405';}"
    )
    return button


def init_frame():
    set_content_margins(0, 0, 0, 300)
    logo = display_logo()

    # button widget
    next_button = create_button("Dalej")
    widgets["next_button"].append(next_button)

    grid.addWidget(widgets["logo"][-1], 0, 0, 1, 3)  # (row, column, row_span, column_span)
    grid.addWidget(widgets["next_button"][-1], 1, 1, 1, 1)  # -1 is index

    next_button.clicked.connect(next_on_click)


def menu_frame():
    set_content_margins(0, 0, 0, 100)
    logo = display_logo()

    grid.addWidget(widgets["logo"][-1], 0, 0, 0, 3)  # (row, column, row_span, column_span)

    add_order_button = create_button("Dodaj zamówienie")
    run_algorithm_button = create_button("Uruchom algorytm")
    show_timetable_button = create_button("Pokaż harmonogram")

    widgets["add_order_button"].append(add_order_button)
    widgets["run_algorithm_button"].append(run_algorithm_button)
    widgets["show_timetable_button"].append(show_timetable_button)

    grid.addWidget(widgets["add_order_button"][-1], 1, 1, 1, 1)
    grid.addWidget(widgets["run_algorithm_button"][-1], 2, 1, 1, 1)
    grid.addWidget(widgets["show_timetable_button"][-1], 3, 1, 1, 1)

    show_timetable_button.clicked.connect(show_timetable_button_on_click)


def timetable_frame():
    timetable_widget = QtWidgets.QTableWidget()

    # timetable_widget.setGeometry(QtCore.QRect(100, 100, 660, 660))  # (x, y, width, height )
    timetable_widget.setColumnCount(2)
    timetable_widget.setRowCount(2)
    timetable_widget.setHorizontalHeaderLabels(["ID zamówienia", "Kwota"])
    timetable_widget.setItem(0, 0, QTableWidgetItem("Name"))
    timetable_widget.setItem(0, 1, QTableWidgetItem("2222"))

    widgets["timetable_widget"].append(timetable_widget)
    grid.addWidget(widgets["timetable_widget"][-1], 1, 1, 1, 3)
    set_content_margins(0, 100, 0, 0)


init_frame()
# applying this grid on layout
window.setLayout(grid)

# displaying window
window.show()
# terminate app
sys.exit(app.exec())
