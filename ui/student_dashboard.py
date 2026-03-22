from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem

from backend.orar_service import get_orar_student

class StudentDashboard(QWidget):
    def __init__(self, grupa="A1"):
        super().__init__()
        
        self.setWindowTitle("Dashboard Student")

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Orar pentru grupa {grupa}"))

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Zi", "Ora", "Materie", "Profesor", "Sala"])

        layout.addWidget(self.table)
        self.setLayout(layout)
        self.load_data(grupa)

    def load_data(self, grupa):
        data = get_orar_student(grupa)
        self.table.setRowCount(len(data))

        for row, item in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(item["zi"]))
            self.table.setItem(row, 1, QTableWidgetItem(item["ora"]))
            self.table.setItem(row, 2, QTableWidgetItem(item["materie"]))
            self.table.setItem(row, 3, QTableWidgetItem(item["profesor"]))
            self.table.setItem(row, 4, QTableWidgetItem(item["sala"]))