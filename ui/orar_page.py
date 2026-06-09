from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QAbstractItemView,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from backend.data_service import list_professors, list_rooms, list_subjects
from backend.orar_service import DAYS, HOURS, add_orar, delete_orar, generate_orar, get_orar


class OrarPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("Gestionare orar")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        form_grid = QGridLayout()
        form_grid.setHorizontalSpacing(16)
        form_grid.setVerticalSpacing(10)

        self.an = QComboBox()
        self.an.addItems(["1", "2", "3"])
        self.an.currentTextChanged.connect(self.refresh_subjects)

        self.zi = QComboBox()
        self.zi.addItems(DAYS)

        self.ora = QComboBox()
        self.ora.addItems(HOURS)

        self.materie = QComboBox()
        self.profesor = QComboBox()
        self.sala = QComboBox()

        self._add_form_row(form_grid, 0, "An", self.an)
        self._add_form_row(form_grid, 1, "Zi", self.zi)
        self._add_form_row(form_grid, 2, "Ora", self.ora)
        self._add_form_row(form_grid, 3, "Materie", self.materie)
        self._add_form_row(form_grid, 4, "Profesor", self.profesor)
        self._add_form_row(form_grid, 5, "Sala", self.sala)
        layout.addLayout(form_grid)

        actions = QHBoxLayout()
        add_btn = QPushButton("Adauga in orar")
        add_btn.clicked.connect(self.adauga)
        gen_btn = QPushButton("Genereaza automat")
        gen_btn.setObjectName("secondary")
        gen_btn.clicked.connect(self.genereaza_orar)
        refresh_btn = QPushButton("Reincarca date")
        refresh_btn.setObjectName("secondary")
        refresh_btn.clicked.connect(self.refresh_all)
        delete_btn = QPushButton("Sterge selectia")
        delete_btn.setObjectName("danger")
        delete_btn.clicked.connect(self.sterge_orar)
        clear_btn = QPushButton("Goleste orarul")
        clear_btn.setObjectName("danger")
        clear_btn.clicked.connect(self.goleste_orar)
        actions.addWidget(add_btn)
        actions.addWidget(gen_btn)
        actions.addWidget(refresh_btn)
        actions.addStretch()
        actions.addWidget(delete_btn)
        actions.addWidget(clear_btn)
        layout.addLayout(actions)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "An", "Zi", "Ora", "Materie", "Profesor", "Sala"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

        self.subjects = []
        self.refresh_all()

    def _add_form_row(self, grid, column, label, widget):
        form = QFormLayout()
        form.addRow(label, widget)
        grid.addLayout(form, column // 3, column % 3)

    def refresh_all(self):
        self.refresh_options()
        self.load_data()

    def refresh_options(self):
        self.subjects = list_subjects()

        self.profesor.clear()
        self.profesor.addItems([item["name"] for item in list_professors()])

        self.sala.clear()
        self.sala.addItems([item["name"] for item in list_rooms()])

        self.refresh_subjects()

    def refresh_subjects(self):
        selected_year = int(self.an.currentText())
        self.materie.clear()
        self.materie.addItems(
            [item["name"] for item in self.subjects if int(item["an"]) == selected_year]
        )

    def load_data(self):
        data = get_orar()
        self.table.setRowCount(len(data))
        columns = ["id", "an", "zi", "ora", "materie", "profesor", "sala"]
        for row, item in enumerate(data):
            for column, key in enumerate(columns):
                cell = QTableWidgetItem(str(item[key]))
                cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, column, cell)
        self.table.hideColumn(0)

    def adauga(self):
        try:
            add_orar(
                self.zi.currentText(),
                self.ora.currentText(),
                self.materie.currentText(),
                self.profesor.currentText(),
                self.sala.currentText(),
                self.an.currentText(),
            )
            self.load_data()
        except Exception as error:
            QMessageBox.warning(self, "Eroare", str(error))

    def genereaza_orar(self):
        try:
            generate_orar()
            self.load_data()
            QMessageBox.information(self, "Succes", "Orarul a fost generat automat.")
        except Exception as error:
            QMessageBox.critical(self, "Eroare", str(error))

    def sterge_orar(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Selectie", "Selecteaza un rand din tabel.")
            return

        entry_id = self.table.item(row, 0).text()
        answer = QMessageBox.question(self, "Confirmare", "Stergi intrarea selectata?")
        if answer != QMessageBox.StandardButton.Yes:
            return

        delete_orar(entry_id)
        self.load_data()

    def goleste_orar(self):
        answer = QMessageBox.question(self, "Confirmare", "Stergi tot orarul?")
        if answer != QMessageBox.StandardButton.Yes:
            return

        delete_orar()
        self.load_data()
