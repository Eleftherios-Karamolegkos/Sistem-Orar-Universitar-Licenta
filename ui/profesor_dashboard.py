from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from backend.orar_service import get_orar_profesor


class ProfesorDashboard(QWidget):
    def __init__(self, nume="Popescu"):
        super().__init__()
        self.nume = nume

        self.setWindowTitle("Dashboard Profesor")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        title = QLabel(f"Orar pentru profesor: {nume}")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        refresh_btn = QPushButton("Reincarca orarul")
        refresh_btn.setObjectName("secondary")
        refresh_btn.clicked.connect(self.load_data)
        layout.addWidget(refresh_btn)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Zi", "Ora", "Materie", "Profesor", "Sala"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)

        layout.addWidget(self.table)
        self.load_data()

    def load_data(self):
        data = get_orar_profesor(self.nume)
        self.table.setRowCount(len(data))

        for row, item in enumerate(data):
            values = [item["zi"], item["ora"], item["materie"], item["profesor"], item["sala"]]
            for column, value in enumerate(values):
                cell = QTableWidgetItem(str(value))
                cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, column, cell)
