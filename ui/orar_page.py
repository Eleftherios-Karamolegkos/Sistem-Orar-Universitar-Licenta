from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem,
    QLineEdit, QLabel, QComboBox, QMessageBox
)

from backend.orar_service import get_orar, add_orar
from backend.orar_service import check_conflict
from backend.orar_service import generate_orar


class OrarPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        self.zi = QComboBox()
        self.zi.addItems(["Luni", "Marti", "Miercuri", "Joi", "Vineri"])
    
        self.ora = QLineEdit()
        self.ora.setPlaceholderText("Ex: 09:00-11:00")
    
        self.materie = QLineEdit()
        self.materie.setPlaceholderText("Materie")
    
        self.profesor = QLineEdit()
        self.profesor.setPlaceholderText("Profesor")
    
        self.sala = QLineEdit()
        self.sala.setPlaceholderText("Sala")
    
        add_btn = QPushButton("Adauga Orar")
        add_btn.clicked.connect(self.adauga)

        gen_btn = QPushButton("Genereaza Orar Automat")
        gen_btn.clicked.connect(self.genereaza_orar)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Zi", "Ora", "Materie", "Profesor", "Sala"])

        layout.addWidget(QLabel("Creare Orar"))
        layout.addWidget(self.zi)
        layout.addWidget(self.ora)
        layout.addWidget(self.materie)
        layout.addWidget(self.profesor)
        layout.addWidget(self.sala)
        layout.addWidget(add_btn)
        layout.addWidget(self.table)
        layout.addWidget(gen_btn)

        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        data = get_orar()
        self.table.setRowCount(len(data))
        for row, item in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(item["zi"]))
            self.table.setItem(row, 1, QTableWidgetItem(item["ora"]))
            self.table.setItem(row, 2, QTableWidgetItem(item["materie"]))
            self.table.setItem(row, 3, QTableWidgetItem(item["profesor"]))
            self.table.setItem(row, 4, QTableWidgetItem(item["sala"]))

    def adauga(self):
        zi = self.zi.currentText()
        ora = self.ora.text()
        materie = self.materie.text()
        profesor = self.profesor.text()
        sala = self.sala.text()

        conflict = check_conflict(zi, ora, profesor, sala)
        if conflict:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Eroare", "Conflict: Profesor sau Sala acupata!")
            return

        add_orar(zi, ora, materie, profesor, sala)
        self.load_data()

    def genereaza_orar(self):
        generate_orar()
        self.load_data()
        QMessageBox.information(self, "Succes", "Orarul a fost generat automat!")

