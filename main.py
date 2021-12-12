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
from PyQt5.QtGui import *
from PyQt5.QtCore import *
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

services_names = []

# init, sys.argv -- command arguments
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Pimp My Ride")
window.setFixedWidth(1200)
window.setFixedHeight(900)
window.setStyleSheet("background: 'black';")

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
        if widgets[widget]:  # if not empty -> hide widget
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


def sum_duration_of_the_service(services, order_id):
    sum_time = 0
    for service in range(0, len(services)):
        sql_query = f"SELECT czas_trwania FROM usluga WHERE usluga_id = '{services[service][0]}'"
        time = db.db_data_to_list(sql_query)
        sum_time = sum_time + time[0][0]

    sql_query = f"UPDATE zamowienie SET czas_razem = '{sum_time}' WHERE zamowienie_id = '{order_id}'"
    db.execute_query(sql_query)


def swap(services, idx_1, idx_2, priorities):
    services[idx_1], services[idx_2] = services[idx_2], services[idx_1]
    priorities[idx_1], priorities[idx_2] = priorities[idx_2], priorities[idx_1]


def sort_services(order_id):
    sql_query = f"SELECT usluga_id FROM zawartosc_zamowienia WHERE zamowienie_id = '{order_id}'"
    services = db.db_data_to_list(sql_query)
    priorities = []

    # getting service priority
    for service in range(0, len(services)):
        sql_query = f"SELECT priorytet FROM usluga WHERE usluga_id = '{services[service][0]}'"
        priority = db.db_data_to_list(sql_query)
        priorities.append(priority)

    # bubble-sort
    for j in range(0, len(priorities) - 1):
        for i in range(0, len(priorities) - 1):
            if priorities[i] > priorities[i + 1]:
                swap(services, i, i + 1, priorities)

    # save data to database
    i = 1
    for service in range(0, len(services)):
        sql_query = f"""UPDATE zawartosc_zamowienia SET nr_w_kolejce = '{i}' 
        WHERE usluga_id = '{services[service][0]}' AND zamowienie_id = '{order_id}'"""
        db.execute_query(sql_query)
        i = i + 1

    sum_duration_of_the_service(services, order_id)


def add_order_to_database_on_click(s_1, s_2, s_3, s_4, s_5, s_6, s_7, s_8, combo_value):
    # checking car_id depending on registration number (combobox)
    sql_query = f"SELECT * FROM samochod WHERE nr_rejestracyjny = '{combo_value}'"
    car_id = db.db_data_to_list(sql_query)[0][0]
    print("car_id: " + str(car_id))

    # adding order to database
    if s_1 or s_2 or s_3 or s_4 or s_5 or s_6 or s_7 or s_8:
        query = f"INSERT INTO zamowienie(samochod_id) VALUES ('{car_id}')"
        db.execute_query(query)
        print("dodaję zamówienie dla samochodu: " + str(car_id))

    # # adding services to order depending on checked checkboxes
    queries = []
    order_id = db.cur.lastrowid  # returns last added row id
    print(order_id)
    if s_1:
        queries.append(f"INSERT INTO zawartosc_zamowienia(zamowienie_id, usluga_id) VALUES ('{order_id}', '1')")
    if s_2:
        queries.append(f"INSERT INTO zawartosc_zamowienia(zamowienie_id, usluga_id) VALUES ('{order_id}', '2')")
    if s_3:
        queries.append(f"INSERT INTO zawartosc_zamowienia(zamowienie_id, usluga_id) VALUES ('{order_id}', '3')")
    if s_4:
        queries.append(f"INSERT INTO zawartosc_zamowienia(zamowienie_id, usluga_id) VALUES ('{order_id}', '4')")
    if s_5:
        queries.append(f"INSERT INTO zawartosc_zamowienia(zamowienie_id, usluga_id) VALUES ('{order_id}', '5')")
    if s_6:
        queries.append(f"INSERT INTO zawartosc_zamowienia(zamowienie_id, usluga_id) VALUES ('{order_id}', '6')")
    if s_7:
        queries.append(f"INSERT INTO zawartosc_zamowienia(zamowienie_id, usluga_id) VALUES ('{order_id}', '7')")
    if s_8:
        queries.append(f"INSERT INTO zawartosc_zamowienia(zamowienie_id, usluga_id) VALUES ('{order_id}', '8')")

    for query in queries:
        db.execute_query(query)

    sort_services(order_id)


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


def create_checkbox(name):
    checkbox = QCheckBox(name)
    checkbox.setStyleSheet("QCheckBox::indicator:unchecked {image: url(checkbox_1.png);}" +
                           "QCheckBox::indicator:unchecked:hover {image: url(hover_1.png);}" +
                           "QCheckBox::indicator:checked {image: url(checked_1.png);}" +
                           "*{font-size: 20px; font-weight: bold; color: 'white';}")
    return checkbox


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
    set_content_margins(0, 0, 100, 100)

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
    set_content_margins(0, 0, 100, 100)

    add_order_label = QLabel()
    add_order_label.setText("Dodaj zamówienie:")
    widgets["add_order_label"].append(add_order_label)
    add_order_label.setStyleSheet("font-size: 35px; font-weight: bold;")
    grid.addWidget(widgets["add_order_label"][-1], 0, 1, 1, 1)  # (row, column, row_span, column_span)
    add_order_label.setStyleSheet("font-size: 35px; font-weight: bold; color: 'white';")

    display_logo("small_logo")
    grid.addWidget(widgets["logo"][-1], 0, 3, 1, 1)  # (row, column, row_span, column_span)

    registration_number_combo = QComboBox()
    registration_number_combo.setStyleSheet("font-size: 20px; font-weight: bold; color: 'black'; background: 'white'")
    registration_number_combo.addItems(["DSA2432", "FSD2318", "SI3M4", "TU432", "RWH313", "ERA212"])
    widgets["registration_number_combo"].append(registration_number_combo)
    grid.addWidget(widgets["registration_number_combo"][-1], 1, 1, 1, 1)
    # print(str(registration_number_combo.currentText()))

    service_1 = create_checkbox("usluga_1")
    service_2 = create_checkbox("usluga_2")
    service_3 = create_checkbox("usluga_3")
    service_4 = create_checkbox("usluga_4")
    service_5 = create_checkbox("usluga_5")
    service_6 = create_checkbox("usluga_6")
    service_7 = create_checkbox("usluga_7")
    service_8 = create_checkbox("usluga_8")

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

    add_order_to_database = create_button("Dodaj zamówienie")
    widgets["add_order_to_database"].append(add_order_to_database)
    grid.addWidget(widgets["add_order_to_database"][-1], 12, 3, 1, 1)

    add_order_to_database.clicked.connect(lambda: add_order_to_database_on_click(
        service_1.isChecked(), service_2.isChecked(), service_3.isChecked(), service_4.isChecked(),
        service_5.isChecked(), service_6.isChecked(), service_7.isChecked(), service_8.isChecked(),
        str(registration_number_combo.currentText())
    ))


init_frame()
# print_query()
# applying this grid on layout
window.setLayout(grid)

# displaying window
window.show()
# terminate app
sys.exit(app.exec())
