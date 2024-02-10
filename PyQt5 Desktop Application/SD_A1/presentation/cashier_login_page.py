from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont

from model.user import User
from model.user_repository import UserRepository
from presentation.cashier_page import CashierPage
from logic.controller import Controller

import sys
import base64

class CashierLoginPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cashier Login")
        self.setGeometry(300, 300, 400, 200)

        # set the controller
        self.controller = Controller()

        # create the title label
        title_label = QLabel("Cashier Login")
        title_label.setFont(QFont("Arial", 18))

        # create the user and password labels and line edits
        user_label = QLabel("Username:")
        self.user_edit = QLineEdit()
        password_label = QLabel("Password:")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)

        # create the login and register buttons
        login_button = QPushButton("Login")
        register_button = QPushButton("Register")

        # create the vertical layout for the page
        page_layout = QVBoxLayout()
        page_layout.addWidget(title_label)
        page_layout.addWidget(user_label)
        page_layout.addWidget(self.user_edit)
        
        page_layout.addWidget(password_label)
        page_layout.addWidget(self.password_edit)
        page_layout.addWidget(login_button)
        page_layout.addWidget(register_button)

        # create the central widget for the page
        central_widget = QWidget()
        central_widget.setLayout(page_layout)

        # set the central widget for the main window
        self.setCentralWidget(central_widget)

        # connect the button signals to the slot functions
        login_button.clicked.connect(self.login)
        register_button.clicked.connect(self.register)

    def login(self):
        
        # get the username and password inputs from the user
        username = self.user_edit.text()
        password = self.password_edit.text()

        # encode the password using base64 encoding
        encoded_password = base64.b64encode(password.encode('utf-8')).decode('utf-8')

        # check if the username and password are correct
        user = self.controller.get_user(username)
        
        if user is None:
            # if the username or password is incorrect, display an error message
            error_message = QLabel("Incorrect username or password.")
            error_message.setStyleSheet("color: red")
            page_layout = self.centralWidget().layout()
            page_layout.addWidget(error_message)
        
        else:
            # compare the encoded password provided by the user with the encoded password stored in the User object
            if encoded_password == user.password:
                # create an instance of the CashierPage and set it as the central widget
                cashier_page = CashierPage()
                self.setCentralWidget(cashier_page)

            else:
                # if the password is incorrect, display an error message
                error_message = QLabel("Incorrect username or password.")
                error_message.setStyleSheet("color: red")
                page_layout = self.centralWidget().layout()
                page_layout.addWidget(error_message)

    def register(self):

        # get the username and password inputs from the user
        username = self.user_edit.text()
        password = self.password_edit.text()

        # encode the password using base64 encoding
        encoded_password = base64.b64encode(password.encode('utf-8')).decode('utf-8')

        # add the new user to the database
        user = User(username, encoded_password, "cashier")
        self.controller.add_user(user.username, user.password, user.role)

        # create an instance of the CashierPage and set it as the central widget
        cashier_page = CashierPage()
        self.setCentralWidget(cashier_page)
