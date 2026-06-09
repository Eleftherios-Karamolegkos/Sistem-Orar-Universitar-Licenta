from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from backend.auth_service import authenticate
from ui.admin_dashboard import AdminDashboard
from ui.profesor_dashboard import ProfesorDashboard
from ui.student_dashboard import StudentDashboard


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistem Gestionare Orar Universitar")
        self.setMinimumSize(900, 600)

        outer_layout = QVBoxLayout(self)
        outer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setObjectName("loginCard")
        card.setFixedWidth(440)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(14)

        title = QLabel("Autentificare")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Sistem de gestionare orar universitar")
        subtitle.setObjectName("muted")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Utilizator")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Parola")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.returnPressed.connect(self.login)

        login_button = QPushButton("Autentificare")
        login_button.setDefault(True)
        login_button.clicked.connect(self.login)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(login_button)
        outer_layout.addWidget(card)

    def login(self):
        username = self.username.text().strip()
        password = self.password.text()

        if not username or not password:
            QMessageBox.warning(self, "Validare", "Completeaza utilizatorul si parola.")
            return

        result = authenticate(username, password)
        if result:
            try:
                role = result["role"]

                if role == "admin":
                    self.dashboard = AdminDashboard()
                elif role == "profesor":
                    self.dashboard = ProfesorDashboard(result["full_name"])
                elif role == "student":
                    an = result["an"]
                    if an is None:
                        QMessageBox.critical(self, "Eroare", "Student fara an configurat.")
                        return
                    self.dashboard = StudentDashboard(an)
                else:
                    QMessageBox.critical(self, "Eroare", "Rol necunoscut.")
                    return

                self.dashboard.showMaximized()
                self.close()

            except Exception as error:
                QMessageBox.critical(self, "Eroare", str(error))

        else:
            QMessageBox.warning(self, "Eroare", "Date de autentificare incorecte.")
