from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox
)

from backend.auth_service import authenticate
from ui.admin_dashboard import AdminDashboard
from ui.profesor_dashboard import ProfesorDashboard
from ui.student_dashboard import StudentDashboard

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
    
        self.setWindowTitle("Sistem Gestionare Orar Universitar")
        self.setGeometry(500, 200, 350, 250)
    
        layout = QVBoxLayout()
        
        title = QLabel("Autentificare")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Utilizator")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Parola")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        
        login_button = QPushButton("Autentificare")
        login_button.clicked.connect(self.login)

        layout.addWidget(title)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def login(self):

        user = self.username.text()
        password = self.password.text()

        result = authenticate(user, password)

        if result:
            role = result["role"]

            if role == "admin":
                self.dashboard = AdminDashboard()

            elif role == "profesor":
                self.dashboard = ProfesorDashboard(user)

            else:
                self.dashboard = StudentDashboard("A1")

            self.dashboard.show()
            self.close()

        else:
            QMessageBox.warning(self, "Eroare", "Date incorecte")