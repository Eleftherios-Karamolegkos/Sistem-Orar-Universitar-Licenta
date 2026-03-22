from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem

from backend.orar_service import get_orar_profesor

class ProfesorDashboard(QWidget):
    def __init__(self, nume="Popescu"):
        super().__init__()

        self.setWindowTitle("Dashboard Profesor")

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Orar pentru profesor: {nume}"))
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Zi", "Ora", "Materie", "Profesor", "Sala"])

        layout.addWidget(self.table)
        self.setLayout(layout)
        self.load_data(nume)

    def load_data(self, nume):
        data = get_orar_profesor(nume)
        self.table.setRowCount(len(data))

        for row, item in enumerate(data):
            self.table.setItem(row, 0 , QTableWidgetItem(item["zi"]))
            self.table.setItem(row, 1 , QTableWidgetItem(item["ora"]))
            self.table.setItem(row, 2 , QTableWidgetItem(item["materie"]))
            self.table.setItem(row, 3 , QTableWidgetItem(item["profesor"]))
            self.table.setItem(row, 4 , QTableWidgetItem(item["sala"]))

        