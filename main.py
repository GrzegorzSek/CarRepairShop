# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
from database import *
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout, QCheckBox
from PyQt5.QtWidgets import QComboBox
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
    "timetable_widget_1": [],
    "position_1_label": [],
    "position_2_label": [],
    "timetable_widget_2": [],
    "add_order_label": [],
    "registration_number_combo": [],
    "service_1": [],
    "service_2": [],
    "service_3": [],
    "service_4": [],
    "service_5": [],
    "service_6": [],
    "service_7": [],
    "service_8": [],
    "add_order_to_database": [],
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


def display_logo(image_name):
    # display logo
    image = QPixmap(str(image_name) + ".png")
    logo = QLabel()  # logo label
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignHCenter)
    logo.setStyleSheet("margin-top: 50px;")
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


def add_order_button_button_on_click():
    clear_widgets()
    add_order_frame()


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
    display_logo("logo")

    # button widget
    next_button = create_button("Dalej")
    widgets["next_button"].append(next_button)

    grid.addWidget(widgets["logo"][-1], 0, 0, 1, 3)  # (row, column, row_span, column_span)
    grid.addWidget(widgets["next_button"][-1], 1, 1, 1, 1)  # -1 is index

    next_button.clicked.connect(next_on_click)


def menu_frame():
    set_content_margins(0, 0, 0, 100)
    display_logo("logo")

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
    add_order_button.clicked.connect(add_order_button_button_on_click)


def timetable_frame():
    position_1_label = QLabel()
    position_1_label.setText("Stanowisko 1")
    widgets["position_1_label"].append(position_1_label)
    position_1_label.setStyleSheet("font-size: 35px; font-weight: bold;")
    grid.addWidget(widgets["position_1_label"][-1], 1, 1, 1, 3)

    timetable_widget_1 = QtWidgets.QTableWidget()

    # timetable_widget.setGeometry(QtCore.QRect(100, 100, 660, 660))  # (x, y, width, height )
    timetable_widget_1.setColumnCount(5)
    timetable_widget_1.setRowCount(8)
    timetable_widget_1.setHorizontalHeaderLabels(["Dzień 1", "Dzień 2", "Dzień 3", "Dzień 4", "Dzień 5"])
    timetable_widget_1.setItem(0, 0, QTableWidgetItem("Name"))
    timetable_widget_1.setItem(0, 1, QTableWidgetItem("2222"))

    widgets["timetable_widget_1"].append(timetable_widget_1)
    grid.addWidget(widgets["timetable_widget_1"][-1], 2, 1, 1, 3)
    set_content_margins(0, 50, 0, 0)

    position_2_label = QLabel()
    position_2_label.setText("Stanowisko 2")
    widgets["position_2_label"].append(position_2_label)
    position_2_label.setStyleSheet("font-size: 35px; font-weight: bold;")
    grid.addWidget(widgets["position_2_label"][-1], 3, 1, 1, 3)

    timetable_widget_2 = QtWidgets.QTableWidget()

    # timetable_widget.setGeometry(QtCore.QRect(100, 100, 660, 660))  # (x, y, width, height )
    timetable_widget_2.setColumnCount(5)
    timetable_widget_2.setRowCount(8)
    timetable_widget_2.setHorizontalHeaderLabels(["Dzień 1", "Dzień 2", "Dzień 3", "Dzień 4", "Dzień 5"])
    timetable_widget_2.setItem(0, 0, QTableWidgetItem("Name"))
    timetable_widget_2.setItem(0, 1, QTableWidgetItem("2222"))

    widgets["timetable_widget_2"].append(timetable_widget_2)
    grid.addWidget(widgets["timetable_widget_2"][-1], 4, 1, 1, 3)


def add_order_frame():
    set_content_margins(0, 0, 100, 300)

    add_order_label = QLabel()
    add_order_label.setText("Dodaj zamówienie:")
    widgets["add_order_label"].append(add_order_label)
    add_order_label.setStyleSheet("font-size: 35px; font-weight: bold;")
    grid.addWidget(widgets["add_order_label"][-1], 0, 1, 1, 1)  # (row, column, row_span, column_span)

    display_logo("small_logo")
    grid.addWidget(widgets["logo"][-1], 0, 3, 1, 1)  # (row, column, row_span, column_span)

    registration_number_combo = QComboBox()
    registration_number_combo.addItems(["DW65152", "DW66666"])
    widgets["registration_number_combo"].append(registration_number_combo)
    grid.addWidget(widgets["registration_number_combo"][-1], 1, 1, 1, 1)

    service_1 = QCheckBox("usluga_1")
    service_2 = QCheckBox("usluga_2")
    service_3 = QCheckBox("usluga_3")
    service_4 = QCheckBox("usluga_4")
    service_5 = QCheckBox("usluga_5")
    service_6 = QCheckBox("usluga_6")
    service_7 = QCheckBox("usluga_7")
    service_8 = QCheckBox("usluga_8")

    widgets["service_1"].append(service_1)
    widgets["service_2"].append(service_2)
    widgets["service_3"].append(service_3)
    widgets["service_4"].append(service_4)
    widgets["service_5"].append(service_5)
    widgets["service_6"].append(service_6)
    widgets["service_7"].append(service_7)
    widgets["service_8"].append(service_8)

    grid.addWidget(widgets["service_1"][-1], 2, 1, 1, 1)
    grid.addWidget(widgets["service_2"][-1], 3, 1, 1, 1)
    grid.addWidget(widgets["service_3"][-1], 4, 1, 1, 1)
    grid.addWidget(widgets["service_4"][-1], 5, 1, 1, 1)
    grid.addWidget(widgets["service_5"][-1], 6, 1, 1, 1)
    grid.addWidget(widgets["service_6"][-1], 7, 1, 1, 1)
    grid.addWidget(widgets["service_7"][-1], 8, 1, 1, 1)
    grid.addWidget(widgets["service_8"][-1], 9, 1, 1, 1)


init_frame()
# print_query()
# applying this grid on layout
window.setLayout(grid)

# displaying window
window.show()
# terminate app
sys.exit(app.exec())
