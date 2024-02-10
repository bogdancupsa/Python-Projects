from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem

from model.show import Show
from model.show_repository import ShowRepository
from logic.controller import Controller

import sys

from datetime import datetime

class CashierPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # add the controller
        self.controller = Controller()

        # create the main layout
        main_layout = QVBoxLayout()

        # create the table widget for the shows
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        
        self.table_widget.setHorizontalHeaderLabels(['Name', 'Singer', 'Date', 'Available Tickets', 'Genre'])
        self.table_widget.horizontalHeader().setStretchLastSection(True)

        # create the layout for the buttons
        button_layout = QHBoxLayout()

        # create the 'sell ticket' button
        self.sell_ticket_button = QPushButton('Sell Ticket')
        button_layout.addWidget(self.sell_ticket_button)

        # add the button layout to the main layout
        main_layout.addLayout(button_layout)

        # add the table widget to the main layout
        main_layout.addWidget(self.table_widget)

        # set the main layout
        self.setLayout(main_layout)

        # connect the 'sell ticket' button to its handler
        self.sell_ticket_button.clicked.connect(self.sell_ticket)

        # populate the table widget with the shows
        self.populate_table()

    def populate_table(self):
        # get all the shows
        shows = self.controller.get_all_shows()

        # set the row count of the table widget
        self.table_widget.setRowCount(len(shows))

        # populate the table widget with the shows
        for i, show in enumerate(shows):
            
            name_item = QTableWidgetItem(show.name)
            singer_item = QTableWidgetItem(show.singer)
            
            date_obj = datetime.strptime(show.date, '%Y-%m-%d')
            date_item = QTableWidgetItem(date_obj.strftime('%d/%m/%Y'))
            
            available_tickets_item = QTableWidgetItem(str(show.num_tickets))
            genre_item = QTableWidgetItem(show.genre)
            
            self.table_widget.setItem(i, 0, name_item)
            self.table_widget.setItem(i, 1, singer_item)
            self.table_widget.setItem(i, 2, date_item)
            self.table_widget.setItem(i, 3, available_tickets_item)
            self.table_widget.setItem(i, 4, genre_item)

            # add the 'sell ticket' button to the last column of the row
            sell_ticket_button = QPushButton('Sell Ticket')
            sell_ticket_button.clicked.connect(lambda _, show=show: self.sell_ticket_for_show(show))
            self.table_widget.setCellWidget(i, 5, sell_ticket_button)

    def sell_ticket_for_show(self, show):
        
        # decrement the available tickets for the show
        if show.num_tickets >= 1:
            show.num_tickets -= 1

        # update show with the new tickets number value
        self.controller.update_show(show.name, show.singer, show.date, show.num_tickets, show.genre)

        # refresh the table widget
        self.populate_table()


    def sell_ticket(self):
        
        # get the currently selected row
        selected_row = self.table_widget.currentRow()

        if selected_row != -1:
            # get the show for the selected row
            show = self.controller.get_all_shows()[selected_row]

            # sell a ticket for the show
            self.sell_ticket_for_show(show)
