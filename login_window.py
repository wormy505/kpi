from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox, QComboBox
from db_handler import fetch_user_credentials, get_user_password

class LoginWindow(QWidget):
    def __init__(self, role, on_login):
        super().__init__()
        self.role = role
        self.on_login = on_login
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login")
        self.setGeometry(300, 300, 300, 200)

        layout = QVBoxLayout()

        self.username_label = QLabel("Username:")
        layout.addWidget(self.username_label)
        self.username_input = QComboBox()
        self.username_input.addItems(sorted(fetch_user_credentials(self.role), reverse=False))
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Password:")
        layout.addWidget(self.password_label)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.currentText()
        password = self.password_input.text()

        if self.validate_credentials(username, password):
            self.on_login(self.role, username)
            self.close()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def validate_credentials(self, username, password):
        stored_password = get_user_password(self.role, username)
        return stored_password == password
