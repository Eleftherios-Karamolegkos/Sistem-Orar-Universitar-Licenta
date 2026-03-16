from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class StudentDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard Student")
        self.setGeometry(400,200,600,400)
        layout = QVBoxLayout()
        title = QLabel("Orarul Studentului")
        title.setStyleSheet("font-size:20px; font-weight:bold;")
        layout.addWidget(title)
        self.setLayout(layout)