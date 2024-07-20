from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton

class InitialWindow(QMainWindow):
    def __init__(self, on_role_selected):
        super().__init__()
        self.on_role_selected = on_role_selected
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Role Selection")
        self.setMinimumSize(400, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.department_button = QPushButton("Department")
        self.department_button.clicked.connect(lambda: self.on_role_selected("Department"))
        layout.addWidget(self.department_button)

        self.appraiser_button = QPushButton("Appraiser")
        self.appraiser_button.clicked.connect(lambda: self.on_role_selected("Appraiser"))
        layout.addWidget(self.appraiser_button)

        self.admin_button = QPushButton("Admin")
        self.admin_button.clicked.connect(lambda: self.on_role_selected("Admin"))
        layout.addWidget(self.admin_button)
