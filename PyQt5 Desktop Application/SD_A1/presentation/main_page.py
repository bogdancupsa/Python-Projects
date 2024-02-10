from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QStackedWidget
from PyQt5.QtGui import QFont
from presentation.admin_login_page import AdminLoginPage
from presentation.cashier_login_page import CashierLoginPage

class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Festival Ticket Selling App")
        self.setGeometry(300, 300, 400, 200)

        # create the title label
        title_label = QLabel("Festival Ticket Selling App")
        title_label.setFont(QFont("Arial", 18))

        # create the admin and cashier buttons
        admin_button = QPushButton("Admin Login")
        cashier_button = QPushButton("Cashier Login")

        # create the horizontal layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(admin_button)
        button_layout.addWidget(cashier_button)

        # create the vertical layout for the page
        page_layout = QVBoxLayout()
        page_layout.addWidget(title_label)
        page_layout.addLayout(button_layout)

        # create the stacked widget and add the pages
        self.stacked_widget = QStackedWidget()
        self.admin_login_page = AdminLoginPage()
        self.cashier_login_page = CashierLoginPage()
        self.stacked_widget.addWidget(self.admin_login_page)           
        self.stacked_widget.addWidget(self.cashier_login_page)

        # add the stacked widget to the layout
        page_layout.addWidget(self.stacked_widget)

        # create the central widget for the page
        central_widget = QWidget()
        central_widget.setLayout(page_layout)

        # set the central widget for the main window
        self.setCentralWidget(central_widget)

        # connect the button signals to the slot functions
        admin_button.clicked.connect(self.show_admin_login_page)
        cashier_button.clicked.connect(self.show_cashier_login_page)

    def show_admin_login_page(self):
        self.stacked_widget.setCurrentWidget(self.admin_login_page)

    def show_cashier_login_page(self):
        self.stacked_widget.setCurrentWidget(self.cashier_login_page)