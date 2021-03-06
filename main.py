# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
import random
from database import *
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout, QCheckBox
from PyQt5.QtWidgets import QComboBox, QLineEdit, QPlainTextEdit
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QCursor
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox
# from fpdf import FPDF

widgets = {
    # init frame
    "logo": [],
    "next_button": [],
    # menu frame
    "add_order_button": [],
    "run_algorithm_button": [],
    "show_timetable_button": [],
    "check_order_button": [],
    "run_algorithm_x_times": [],
    # schedule frame
    "timetable_widget_1": [],
    "position_1_label": [],
    "position_2_label": [],
    "timetable_widget_2": [],
    "show_details_button": [],
    # add order frame
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
    # add order, schedule, check order
    "back_to_menu": [],
    # check order frame
    "find_order_textbox": [],
    "find_order_button": [],
    "table_label": [],
    "order_content_widget": [],
    # show details frame
    "position_1_qplane": [],
    "position_2_qplane": [],
}

services_names = []

# init, sys.argv -- command arguments
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Pimp My Ride")
# window.setFixedWidth(1200)
window.setFixedWidth(1500)
# window.setFixedHeight(900)
window.setFixedHeight(900)
window.setStyleSheet("background: 'black';")

# grid layout
grid = QGridLayout()


def info_message():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("Wykonano pomy??lnie")
    msg.setWindowTitle("informacja")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


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


def back_to_menu_on_click():
    clear_widgets()
    menu_frame()


def show_details_on_click():
    clear_widgets()
    show_details_frame()


def show_timetable_button_on_click():
    clear_widgets()
    timetable_frame()


def add_order_button_button_on_click():
    clear_widgets()
    add_order_frame()


def check_order_button_on_click():
    clear_widgets()
    check_order_content_frame()


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
        print("dodaj?? zam??wienie dla samochodu: " + str(car_id))

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
    info_message()


def save_to_database(position_orders, position_number):
    for i in range(0, 5):
        counter = 1
        for j in range(1, len(position_orders[i])):
            sql_query = f"""UPDATE zamowienie SET data_plan_wyk = '{i + 1}', nr_w_kolejce = '{counter}',
            nr_stanowiska = '{position_number}' WHERE zamowienie_id = '{position_orders[i][j]}'"""
            db.execute_query(sql_query)
            counter = counter + 1


def add_order_to_pos(day, position, pos_hours, orders):
    counter = 0
    for order in orders:
        if order[1] <= pos_hours[0]:
            position[day].append(order[0])    # add order to specific day
            orders.pop(counter)  # remove order from the list of orders
            order_time = pos_hours[0] - order[1]
            pos_hours = [order_time, False]
            return pos_hours
        counter = counter + 1
    pos_hours = [pos_hours[0], True]
    return pos_hours


def run_algorithm_button_on_click(run_x_times_textbox_value):
    run_x_times = int(run_x_times_textbox_value.text())
    position_1 = [[]]
    position_2 = [[]]
    solution = 8  # amount of left free hours

    for i in range(0, int(run_x_times)):
        new_position_1 = [[1], [2], [3], [4], [5]]
        new_position_2 = [[1], [2], [3], [4], [5]]
        new_solution = 0

        query = "SELECT zamowienie_id, czas_razem FROM zamowienie ORDER BY data_mod ASC"
        orders = db.db_data_to_list(query)

        # iteration over available 5 days
        for day in range(0, 5):
            pos_1_hours = [8, False]  # position, no_solution (True if no solution)
            pos_2_hours = [8, False]

            while pos_1_hours[1] is False or pos_2_hours[1] is False:  #
                if orders:
                    if pos_1_hours[1] is False and pos_2_hours[1] is False:
                        rand_num = random.randint(0, 9)
                        if rand_num % 2 != 0:
                            if pos_1_hours[1] is False:
                                # add order to position 1 on day {i}
                                pos_1_hours = add_order_to_pos(day, new_position_1, pos_1_hours, orders)
                                if pos_1_hours[0] == 0:
                                    pos_1_hours = [0, True]
                            else:
                                continue
                        else:
                            if pos_2_hours[1] is False:
                                # add order to position 2 on day {i}
                                pos_2_hours = add_order_to_pos(day, new_position_2, pos_2_hours, orders)
                                if pos_2_hours[0] == 0:
                                    pos_2_hours = [0, True]
                            else:
                                continue
                    elif pos_2_hours[1] is True:
                        if pos_1_hours[1] is False:
                            pos_1_hours = add_order_to_pos(day, new_position_1, pos_1_hours, orders)
                            if pos_1_hours[0] == 0:
                                pos_1_hours = [0, True]
                            # add order to position 1 on day {i}
                        else:
                            continue
                    else:
                        if pos_2_hours[1] is False:
                            pos_2_hours = add_order_to_pos(day, new_position_2, pos_2_hours, orders)
                            if pos_2_hours[0] == 0:
                                pos_2_hours = [0, True]
                            # add order to position 2 on day {i}
                        else:
                            continue
                else:
                    break
            new_solution = new_solution + pos_1_hours[0] + pos_2_hours[0]
        print(new_solution)
        position_1 = new_position_1
        position_2 = new_position_2
        if new_solution < solution:
            solution = new_solution
            position_1 = new_position_1
            position_2 = new_position_2

    save_to_database(position_1, 1)
    save_to_database(position_2, 2)
    set_dates(1)
    set_dates(2)
    data_to_file(1)
    data_to_file(2)
    # print_to_pdf("stanowisko", 1)
    # print_to_pdf("stanowisko", 2)
    info_message()


def set_dates(position):
    month = 'jan'
    year = '2022'
    time = ':00:00'
    day = 13

    for i in range(1, 6):
        query = f"""SELECT zamowienie_id, czas_razem FROM zamowienie WHERE nr_stanowiska = '{position}'
        AND data_plan_wyk = '{i}' ORDER BY nr_w_kolejce ASC"""  # get orders data
        orders = db.db_data_to_list(query)
        counter = 0
        hours_to_add = 8
        data = month + " " + str(day) + " " + year + " " + str(hours_to_add) + time

        for order in orders:
            if counter == 0:
                data_2 = month + " " + str(day) + " " + year + " " + str(hours_to_add + order[1]) + time
                sql_query = f"""UPDATE zamowienie SET data_rozp = '{data}', data_zak = '{data_2}'
                WHERE zamowienie_id = '{order[0]}'"""
                db.execute_query(sql_query)

                hours_to_add = hours_to_add + order[1]
                counter = 1
            else:
                data = month + " " + str(day) + " " + year + " " + str(hours_to_add) + time
                data_2 = month + " " + str(day) + " " + year + " " + str(hours_to_add + order[1]) + time
                sql_query = f"""UPDATE zamowienie SET data_rozp = '{data}', data_zak = '{data_2}'
                WHERE zamowienie_id = '{order[0]}'"""
                db.execute_query(sql_query)

                hours_to_add = hours_to_add + order[1]
        day = day + 1


def data_to_file(position):
    text_file = open("C:/Users/grzes/PycharmProjects/CarRepairShop/stanowisko" + str(position) + ".txt", "w")
    query = f"""SELECT imie, nazwisko, model.nazwa AS 'model',
            marka.nazwa AS 'marka', samochod.nr_rejestracyjny, zamowienie.data_rozp,
            zamowienie.data_zak, zamowienie.zamowienie_id
            FROM klient
            JOIN samochod ON klient.samochod_id = samochod.samochod_id
            JOIN model ON samochod.model_id = model.model_id
            JOIN marka ON model.marka_id = marka.marka_id
            JOIN zamowienie ON samochod.samochod_id = zamowienie.samochod_id
            WHERE zamowienie.nr_stanowiska = '{position}' ORDER BY zamowienie.data_rozp ASC"""  # get orders data
    orders = db.db_data_to_list(query)
    text_file.write('Stanowisko: ' + str(position) + '\n\n')

    for order in orders:
        text_file.write('***************************\n')
        text_file.write('^^^^^ Nr zamowienia: ' + str(order[7]) + ' ^^^^^\n')
        # text_file.write('--------------------------\n')
        text_file.write('Imie i nazwisko klienta: ' + str(order[0]) + " " + str(order[1]) + '\n')
        # text_file.write('--------------------------\n')
        text_file.write('data_rozpoczecia: ' + str(order[5]) + '\n')
        text_file.write('--------------------------\n')
        text_file.write('uslugi: \n')
        query = f"""SELECT nazwa
                    FROM usluga
                    JOIN zawartosc_zamowienia ON usluga.usluga_id = zawartosc_zamowienia.usluga_id
                    JOIN zamowienie ON zawartosc_zamowienia.zamowienie_id = zamowienie.zamowienie_id
                    WHERE zamowienie.zamowienie_id = '{order[7]}';"""
        services = db.db_data_to_list(query)
        for service in services:
            text_file.write(str(service[0]) + '\n')

        text_file.write('--------------------------\n')
        text_file.write('data_zakonczenia: ' + str(order[6]) + '\n')
        text_file.write('***************************\n\n\n')

    text_file.close()


# def print_to_pdf(name, position):
#     pdf = FPDF()
#
#     # Add a page
#     pdf.add_page()
#
#     # set style and size of font
#     # that you want in the pdf
#     pdf.set_font("Arial", size=15)
#
#     # open the text file in read mode
#     f = open(name + str(position) + ".txt", "r")
#
#     # insert the texts in pdf
#     for x in f:
#         pdf.cell(200, 10, txt=x, ln=1, align='C')
#
#     # save the pdf with name .pdf
#     pdf.output(name + str(position) + ".pdf")


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


def set_timetable_cell_value(widget_name, workplace_number):
    for day in range(0, 5):
        sql_query = f"""SELECT zamowienie_id, czas_razem FROM zamowienie WHERE nr_stanowiska = '{workplace_number}' 
        AND data_plan_wyk = '{day + 1}' ORDER BY nr_w_kolejce ASC"""
        result = db.db_data_to_list(sql_query)

        start_row = 0
        for i in range(0, len(result)):  # iterations through rows
            repeat_number = result[i][1]
            last_row = repeat_number
            if i > 0:
                start_row = start_row + result[i-1][1]
                last_row = start_row + repeat_number

            for r in range(start_row, last_row):
                widget_name.setItem(r, day, QTableWidgetItem(str(result[i][0])))


def find_order_button_on_click(label, textbox, table_name):
    textbox_value = textbox.text()
    label.setText(f"zawarto???? zam??wienia nr: {textbox_value}")

    sql_query = f"""SELECT nazwa
                FROM usluga
                JOIN zawartosc_zamowienia ON usluga.usluga_id = zawartosc_zamowienia.usluga_id
                JOIN zamowienie ON zawartosc_zamowienia.zamowienie_id = zamowienie.zamowienie_id
                WHERE zamowienie.zamowienie_id = '{textbox_value}';"""

    rows = db.db_data_to_list(sql_query)
    i = 0
    for row in rows:
        table_name.setItem(i, 0, QTableWidgetItem(row[0]))
        i = i + 1


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
    set_content_margins(0, 0, 0, 25)

    display_logo("logo")
    grid.addWidget(widgets["logo"][-1], 0, 0, 3, 5)  # (row, column, row_span, column_span)

    add_order_button = create_button("Dodaj zam??wienie")
    run_algorithm_button = create_button("Uruchom algorytm")
    show_timetable_button = create_button("Poka?? harmonogram")
    check_order_button = create_button("Sprawd?? zam??wienie")

    widgets["add_order_button"].append(add_order_button)
    widgets["run_algorithm_button"].append(run_algorithm_button)
    widgets["show_timetable_button"].append(show_timetable_button)
    widgets["check_order_button"].append(check_order_button)

    grid.addWidget(widgets["add_order_button"][-1], 3, 2, 2, 1)
    grid.addWidget(widgets["run_algorithm_button"][-1], 5, 2, 2, 1)
    grid.addWidget(widgets["show_timetable_button"][-1], 7, 2, 2, 1)
    grid.addWidget(widgets["check_order_button"][-1], 9, 2, 2, 1)

    # textbox
    run_algorithm_x_times = QLineEdit()
    run_algorithm_x_times.setStyleSheet("font-size: 20px; font-weight: bold; color: 'black'; background: 'white'")
    run_algorithm_x_times.setPlaceholderText("Ile razy uruchomi?? algorytm?")
    widgets["run_algorithm_x_times"].append(run_algorithm_x_times)
    grid.addWidget(widgets["run_algorithm_x_times"][-1], 11, 2, 1, 1)

    run_algorithm_x_times.setFixedWidth(400)
    # size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
    # run_algorithm_x_times.setSizePolicy(size_policy)

    # buttons functions
    show_timetable_button.clicked.connect(show_timetable_button_on_click)
    add_order_button.clicked.connect(add_order_button_button_on_click)
    run_algorithm_button.clicked.connect(lambda: run_algorithm_button_on_click(run_algorithm_x_times))
    check_order_button.clicked.connect(check_order_button_on_click)


def show_details_frame():
    set_content_margins(50, 5, 50, 0)

    # position 1
    position_1_qplane = QPlainTextEdit()
    position_1_qplane.setStyleSheet("color: 'black'; background: 'white';")
    widgets["position_1_qplane"].append(position_1_qplane)
    grid.addWidget(widgets["position_1_qplane"][-1], 0, 1, 1, 1)

    # position 2
    position_2_qplane = QPlainTextEdit()
    position_2_qplane.setStyleSheet("color: 'black'; background: 'white';")
    widgets["position_2_qplane"].append(position_2_qplane)
    grid.addWidget(widgets["position_2_qplane"][-1], 0, 3, 1, 1)

    # button back to menu
    back_to_menu = create_button("Menu")
    widgets["back_to_menu"].append(back_to_menu)
    grid.addWidget(widgets["back_to_menu"][-1], 3, 0, 1, 1)

    back_to_menu.setFixedWidth(120)
    back_to_menu.setFixedHeight(90)

    back_to_menu.clicked.connect(back_to_menu_on_click)

    # logo
    display_logo("small_logo")
    grid.addWidget(widgets["logo"][-1], 3, 4, 1, 1)  # (row, column, row_span, column_span)

    # display data from files
    file_1 = open('stanowisko1.txt', 'r')
    contents_1 = file_1.read()

    file_2 = open('stanowisko2.txt', 'r')
    contents_2 = file_2.read()

    position_1_qplane.insertPlainText(contents_1)
    position_2_qplane.insertPlainText(contents_2)


def timetable_frame():
    set_content_margins(50, 5, 50, 0)

    position_1_label = QLabel()
    position_1_label.setText("Stanowisko 1")
    widgets["position_1_label"].append(position_1_label)
    position_1_label.setStyleSheet("font-size: 40px; font-weight: bold; color: 'white';")
    grid.addWidget(widgets["position_1_label"][-1], 1, 0, 1, 1)

    timetable_widget_1 = QtWidgets.QTableWidget()
    timetable_widget_1.setStyleSheet("color: 'black'; background: 'white';")

    # timetable_widget.setGeometry(QtCore.QRect(100, 100, 660, 660))  # (x, y, width, height ) nie dziala
    timetable_widget_1.setColumnCount(5)
    timetable_widget_1.setRowCount(8)
    timetable_widget_1.setHorizontalHeaderLabels(["Dzie?? 1", "Dzie?? 2", "Dzie?? 3", "Dzie?? 4", "Dzie?? 5"])
    set_timetable_cell_value(timetable_widget_1, 1)

    widgets["timetable_widget_1"].append(timetable_widget_1)
    grid.addWidget(widgets["timetable_widget_1"][-1], 1, 1, 1, 3)

    # timetable_widget_1.setFixedWidth(520)     # screen 24''
    # timetable_widget_1.setFixedHeight(270)
    timetable_widget_1.setFixedWidth(650)
    timetable_widget_1.setFixedHeight(330)

    position_2_label = QLabel()
    position_2_label.setText("Stanowisko 2")
    widgets["position_2_label"].append(position_2_label)
    position_2_label.setStyleSheet("font-size: 40px; font-weight: bold; color: 'white';")
    grid.addWidget(widgets["position_2_label"][-1], 2, 0, 1, 1)

    timetable_widget_2 = QtWidgets.QTableWidget()
    timetable_widget_2.setStyleSheet("color: 'black'; background: 'white';")

    # timetable_widget.setGeometry(QtCore.QRect(100, 100, 660, 660))  # (x, y, width, height )
    timetable_widget_2.setColumnCount(5)
    timetable_widget_2.setRowCount(8)
    timetable_widget_2.setHorizontalHeaderLabels(["Dzie?? 1", "Dzie?? 2", "Dzie?? 3", "Dzie?? 4", "Dzie?? 5"])
    set_timetable_cell_value(timetable_widget_2, 2)

    widgets["timetable_widget_2"].append(timetable_widget_2)
    grid.addWidget(widgets["timetable_widget_2"][-1], 2, 1, 1, 3)

    # timetable_widget_2.setFixedWidth(520)     # screen 24''
    # timetable_widget_2.setFixedHeight(270)
    timetable_widget_2.setFixedWidth(650)
    timetable_widget_2.setFixedHeight(330)

    back_to_menu = create_button("Menu")
    widgets["back_to_menu"].append(back_to_menu)
    grid.addWidget(widgets["back_to_menu"][-1], 3, 0, 1, 1)

    back_to_menu.setFixedWidth(120)
    back_to_menu.setFixedHeight(90)

    show_details_button = create_button("szczeg????y")
    widgets["show_details_button"].append(show_details_button)
    grid.addWidget(widgets["show_details_button"][-1], 3, 4, 1, 1)

    # display_logo("small_logo")
    # grid.addWidget(widgets["logo"][-1], 3, 4, 1, 1)  # (row, column, row_span, column_span)

    back_to_menu.clicked.connect(back_to_menu_on_click)
    show_details_button.clicked.connect(show_details_on_click)


def add_order_frame():
    set_content_margins(50, 50, 100, 100)

    add_order_label = QLabel()
    add_order_label.setText("Dodaj zam??wienie:")
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

    service_1 = create_checkbox("zmiana lakieru")
    service_2 = create_checkbox("monta?? spoilera")
    service_3 = create_checkbox("modyfikacja pod??o??a i zderzak??w")
    service_4 = create_checkbox("monta?? wysokoenergetycznych ??wiec zap??onowych")
    service_5 = create_checkbox("wymiana t??ok??w silnika")
    service_6 = create_checkbox("zmiana felg")
    service_7 = create_checkbox("zastosowanie sportowego wa??ka rozrz??du")
    service_8 = create_checkbox("Wymiana skrzyni bieg??w i wzmocnienie sprz??g??a")

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

    add_order_to_database = create_button("Dodaj zam??wienie")
    widgets["add_order_to_database"].append(add_order_to_database)
    grid.addWidget(widgets["add_order_to_database"][-1], 12, 3, 1, 1)

    add_order_to_database.clicked.connect(lambda: add_order_to_database_on_click(
        service_1.isChecked(), service_2.isChecked(), service_3.isChecked(), service_4.isChecked(),
        service_5.isChecked(), service_6.isChecked(), service_7.isChecked(), service_8.isChecked(),
        str(registration_number_combo.currentText())
    ))

    back_to_menu = create_button("Menu")
    widgets["back_to_menu"].append(back_to_menu)
    grid.addWidget(widgets["back_to_menu"][-1], 12, 0, 1, 1)

    back_to_menu.setFixedWidth(120)
    back_to_menu.setFixedHeight(90)

    back_to_menu.clicked.connect(back_to_menu_on_click)


def check_order_content_frame():
    set_content_margins(50, 50, 50, 50)

    find_order_textbox = QLineEdit()
    find_order_textbox.setStyleSheet("font-size: 30px; font-weight: bold; color: 'black'; background: 'white'")
    find_order_textbox.setPlaceholderText("nr zam??wienia")
    widgets["find_order_textbox"].append(find_order_textbox)
    grid.addWidget(widgets["find_order_textbox"][-1], 0, 0, 1, 4)

    size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
    find_order_textbox.setSizePolicy(size_policy)

    # button
    find_order_button = create_button("Znajd?? zam??wienie")
    widgets["find_order_button"].append(find_order_button)
    grid.addWidget(widgets["find_order_button"][-1], 0, 4, 1, 1)

    # table
    table_label = QLabel()
    widgets["table_label"].append(table_label)
    table_label.setStyleSheet("font-size: 40px; font-weight: bold; color: 'white';")
    grid.addWidget(widgets["table_label"][-1], 1, 0, 1, 1)

    order_content_widget = QtWidgets.QTableWidget()
    order_content_widget.setStyleSheet("color: 'black'; background: 'white';")

    order_content_widget.setColumnCount(1)
    order_content_widget.setRowCount(8)
    order_content_widget.setHorizontalHeaderLabels(["Us??uga"])

    widgets["order_content_widget"].append(order_content_widget)
    grid.addWidget(widgets["order_content_widget"][-1], 2, 0, 5, 1)

    # order_content_widget.setFixedWidth(300)   # screen 24''
    # order_content_widget.setFixedHeight(270)
    order_content_widget.setFixedWidth(350)
    order_content_widget.setFixedHeight(400)

    # back to menu button
    back_to_menu = create_button("Menu")
    widgets["back_to_menu"].append(back_to_menu)
    grid.addWidget(widgets["back_to_menu"][-1], 9, 0, 1, 1)

    back_to_menu.setFixedWidth(120)
    back_to_menu.setFixedHeight(95)

    display_logo("small_logo")
    grid.addWidget(widgets["logo"][-1], 9, 4, 1, 1)  # (row, column, row_span, column_span)

    back_to_menu.clicked.connect(back_to_menu_on_click)
    find_order_button.clicked.connect(
        lambda: find_order_button_on_click(table_label, find_order_textbox, order_content_widget)
    )


init_frame()
# print_query()
# applying this grid on layout
window.setLayout(grid)

# displaying window
window.show()
# terminate app
sys.exit(app.exec())
