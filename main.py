import sys
from PySide6.QtWidgets import QApplication
from initial_window import InitialWindow
from login_window import LoginWindow
from excel_handler import start_excel_with_data

class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.show_initial_window()

    def show_initial_window(self):
        self.initial_window = InitialWindow(self.on_role_selected)
        self.initial_window.show()

    def on_role_selected(self, role):
        self.role = role
        self.show_login_window()

    def show_login_window(self):
        self.initial_window.close()
        self.login_window = LoginWindow(self.role, self.on_login)
        self.login_window.show()

    def on_login(self, role, username):
        self.login_window.close()
        start_excel_with_data(role, username)

    def run(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":
    app = App()
    app.run()
