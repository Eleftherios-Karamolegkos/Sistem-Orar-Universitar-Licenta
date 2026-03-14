from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox
)

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

        if user == "admin" and password == "admin":
            QMessageBox.information(self, "Succes", "Login Admin reusit")
        else:
            QMessageBox.warning(self, "Eroare", "Date incorecte")