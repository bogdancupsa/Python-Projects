from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont

import base64
import sys

from model.user_repository import UserRepository
from presentation.admin_page import AdminPage
from model.user import User
from logic.controller import Controller

class AdminLoginPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Login")
        self.setGeometry(300, 300, 400, 200)

        # Set the controller
        self.controller = Controller()

        # Create the title label
        title_label = QLabel("Admin Login")
        title_label.setFont(QFont("Arial", 18))

        # Create the user and password labels and line edits
        user_label = QLabel("Username:")
        self.user_edit = QLineEdit()
        password_label = QLabel("Password:")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)

        # Create the login and register buttons
        login_button = QPushButton("Login")
        register_button = QPushButton("Register")

        # Create the vertical layout for the page
        page_layout = QVBoxLayout()
        page_layout.addWidget(title_label)
        page_layout.addWidget(user_label)
        page_layout.addWidget(self.user_edit)
        page_layout.addWidget(password_label)
        page_layout.addWidget(self.password_edit)
        page_layout.addWidget(login_button)
        page_layout.addWidget(register_button)

        # Create the central widget for the page
        central_widget = QWidget()
        central_widget.setLayout(page_layout)

        # Set the central widget for the main window
        self.setCentralWidget(central_widget)

        # Connect the button signals to the slot functions
        login_button.clicked.connect(self.login)
        register_button.clicked.connect(self.register)

    def login(self):
        # Get the username and password inputs from the user
        username = self.user_edit.text()
        password = self.password_edit.text()

        # Encode the password using base64 encoding
        encoded_password = base64.b64encode(password.encode('utf-8')).decode('utf-8')

        # Check if the username and password are correct
        user = self.controller.get_user(username)
        if user is None:
            # If the username or password is incorrect, display an error message
            error_message = QLabel("Incorrect username or password.")
            error_message.setStyleSheet("color: red")
            page_layout = self.centralWidget().layout()
            page_layout.addWidget(error_message)
        else:
            # Compare the encoded password provided by the user with the encoded password stored in the User object
            if encoded_password == user.password:
                # Create an instance of the AdminPage and set it as the central widget
                admin_page = AdminPage()
                self.setCentralWidget(admin_page)
            else:
                # If the password is incorrect, display an error message
                error_message = QLabel("Incorrect username or password.")
                error_message.setStyleSheet("color: red")
                page_layout = self.centralWidget().layout()
                page_layout.addWidget(error_message)

    def register(self):
        # Get the username and password inputs from the user
        username = self.user_edit.text()
        password = self.password_edit.text()

        # Encode the password using base64 encoding
        encoded_password = base64.b64encode(password.encode('utf-8')).decode('utf-8')

        # Add the new user to the database
        user = User(username, encoded_password, "admin")
        self.controller.add_user(user.username, user.password, user.role)

        # Create an instance of the AdminPage and set it as the central widget
        admin_page = AdminPage()
        self.setCentralWidget(admin_page)
