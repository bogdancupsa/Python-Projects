from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QDateEdit, QSpinBox, QDialogButtonBox, QDialog, QPushButton, QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox, QLineEdit

from model.user import User
from model.show import Show
from model.show_repository import ShowRepository
from model.user_repository import UserRepository
from logic.controller import Controller

import csv
import sys

from datetime import datetime

class AdminPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # call the Controller
        self.controller = Controller()

        # create the main layout
        main_layout = QVBoxLayout()

        # create the table widget for the shows
        self.show_table_widget = QTableWidget()
        self.show_table_widget.setColumnCount(5)
        
        self.show_table_widget.setHorizontalHeaderLabels(['Name', 'Singer', 'Date', 'Num Tickets', 'Genre'])
        self.show_table_widget.horizontalHeader().setStretchLastSection(True)

        # create the layout for the buttons
        show_button_layout = QHBoxLayout()

        # create the 'delete show' button
        self.delete_show_button = QPushButton('Delete Show')
        show_button_layout.addWidget(self.delete_show_button)

        # create the 'export shows' button
        self.export_shows_button = QPushButton('Export Shows')
        show_button_layout.addWidget(self.export_shows_button)

        # create the 'add show' button
        self.add_show_button = QPushButton('Add Show')
        show_button_layout.addWidget(self.add_show_button)

        # add the button layout to the main layout
        main_layout.addLayout(show_button_layout)

        # add the table widget to the main layout
        main_layout.addWidget(self.show_table_widget)

        # set the main layout
        self.setLayout(main_layout)

        # connect the 'delete show' button to its handler
        self.delete_show_button.clicked.connect(self.delete_show)

        # connect the 'export shows' button to its handler
        self.export_shows_button.clicked.connect(self.export_shows)

        # connect the 'add show' button to its handler
        self.add_show_button.clicked.connect(self.add_show)

        # populate the table widget with the shows
        self.populate_show_table()

        # create the table widget for the cashiers
        self.cashier_table_widget = QTableWidget()
        self.cashier_table_widget.setColumnCount(2)
        
        self.cashier_table_widget.setHorizontalHeaderLabels(['Username', 'Name'])
        self.cashier_table_widget.horizontalHeader().setStretchLastSection(True)

        # create the layout for the buttons
        cashier_button_layout = QHBoxLayout()

        # create the 'delete cashier' button
        self.delete_cashier_button = QPushButton('Delete Cashier')
        cashier_button_layout.addWidget(self.delete_cashier_button)

        # add the button layout to the main layout
        main_layout.addLayout(cashier_button_layout)

        # add the table widget to the main layout
        main_layout.addWidget(self.cashier_table_widget)

        # connect the 'delete cashier' button to its handler
        self.delete_cashier_button.clicked.connect(self.delete_cashier)

        # populate the table widget with the cashiers
        self.populate_cashier_table()

    def populate_cashier_table(self):
        # get all the cashiers
        cashiers = self.controller.get_all_cashiers()

        # set the row count of the table widget
        self.cashier_table_widget.setRowCount(len(cashiers))

        # populate the table widget with the cashiers
        for i, cashier in enumerate(cashiers):
            username_item = QTableWidgetItem(cashier.username)
            self.cashier_table_widget.setItem(i, 0, username_item)

    def populate_show_table(self):
        shows = self.controller.get_all_shows()
        self.show_table_widget.setRowCount(len(shows))
        
        for row, show in enumerate(shows):

            name_item = QTableWidgetItem(show.name)
            singer_item = QTableWidgetItem(show.singer)
            date_item = QTableWidgetItem(datetime.strptime(show.date, '%Y-%m-%d').strftime('%d/%m/%Y'))
            num_tickets_item = QTableWidgetItem(str(show.num_tickets))
            genre_item = QTableWidgetItem(show.genre)

            self.show_table_widget.setItem(row, 0, name_item)
            self.show_table_widget.setItem(row, 1, singer_item)
            self.show_table_widget.setItem(row, 2, date_item)
            self.show_table_widget.setItem(row, 3, num_tickets_item)
            self.show_table_widget.setItem(row, 4, genre_item)


    def add_show(self):
        # create a QDialog for the add show form
        dialog = QDialog(self)
        dialog.setWindowTitle('Add Show')
        dialog.setWindowModality(Qt.ApplicationModal)

        # create the form layout
        form_layout = QFormLayout()

        # create the line edit widgets for the show form
        name_edit = QLineEdit()
        form_layout.addRow('Name:', name_edit)

        singer_edit = QLineEdit()
        form_layout.addRow('Singer:', singer_edit)

        date_edit = QDateEdit()
        date_edit.setDate(QDate.currentDate())
        form_layout.addRow('Date:', date_edit)

        num_tickets_edit = QSpinBox()
        num_tickets_edit.setMinimum(1)
        num_tickets_edit.setMaximum(1000)
        form_layout.addRow('Number of Tickets:', num_tickets_edit)

        genre_edit = QLineEdit()
        form_layout.addRow('Genre:', genre_edit)

        # create the button box
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        form_layout.addWidget(button_box)

        # create the signal connections for the button box
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        # set the layout for the dialog
        dialog.setLayout(form_layout)

        # show the dialog and wait for user input
        if dialog.exec() == QDialog.Accepted:
            # get the form values
            name = name_edit.text()
            singer = singer_edit.text()
            date = date_edit.date().toPyDate()
            num_tickets = num_tickets_edit.value()
            genre = genre_edit.text()

            # add the show data to the show repository
            self.controller.add_show(name, singer, date, num_tickets, genre)

            # refresh the table widget
            self.populate_show_table()

    def delete_show(self):
        # get the currently selected row
        selected_row = self.show_table_widget.currentRow()

        if selected_row != -1:
            # get the show for the selected row
            show = self.controller.get_all_shows()[selected_row]

            # delete the show from the repository
            self.controller.delete_show(show.name)

            # refresh the table widget
            self.populate_show_table()

    def delete_cashier(self):
        # get the currently selected row
        selected_row = self.cashier_table_widget.currentRow()

        if selected_row != -1:
            # get the cashier for the selected row
            cashier = self.controller.get_all_cashiers()[selected_row]

            # delete the cashier
            self.controller.delete_user(cashier.username)

            # refresh the table widget
            self.populate_cashier_table()


    def export_shows(self):
        # get all the shows
        shows = self.controller.get_all_shows()

        # open a file dialog to get the path to save the file
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Shows", "", "CSV Files (*.csv)")

        if file_path:
            # write the shows to a CSV file
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Name', 'Singer', 'Date', 'Number of Tickets', 'Genre'])
                
                for show in shows:
                    date_obj = datetime.strptime(show.date, '%Y-%m-%d')
                    date_str = date_obj.strftime('%d/%m/%Y')
                    writer.writerow([show.name, show.singer, date_str, show.num_tickets, show.genre])

