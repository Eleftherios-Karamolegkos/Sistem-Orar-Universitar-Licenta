from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QAbstractItemView,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class ManagementPage(QWidget):
    def __init__(self, title, fields, columns, loader, creator, deleter):
        super().__init__()
        self.fields = fields
        self.columns = columns
        self.loader = loader
        self.creator = creator
        self.deleter = deleter
        self.inputs = {}

        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(24, 24, 24, 24)

        page_title = QLabel(title)
        page_title.setObjectName("sectionTitle")
        layout.addWidget(page_title)

        form = QFormLayout()
        form.setSpacing(10)
        for field in self.fields:
            widget = self._build_input(field)
            self.inputs[field["key"]] = widget
            form.addRow(field["label"], widget)
        layout.addLayout(form)

        actions = QHBoxLayout()
        add_btn = QPushButton("Adauga")
        add_btn.clicked.connect(self.add_record)
        delete_btn = QPushButton("Sterge selectia")
        delete_btn.setObjectName("danger")
        delete_btn.clicked.connect(self.delete_selected)
        refresh_btn = QPushButton("Reincarca")
        refresh_btn.setObjectName("secondary")
        refresh_btn.clicked.connect(self.load_data)
        actions.addWidget(add_btn)
        actions.addWidget(delete_btn)
        actions.addWidget(refresh_btn)
        actions.addStretch()
        layout.addLayout(actions)

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels([header for _, header in self.columns])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

        self.load_data()

    def _build_input(self, field):
        if field["type"] == "combo":
            combo = QComboBox()
            combo.addItems([str(value) for value in field["values"]])
            return combo

        if field["type"] == "spin":
            spin = QSpinBox()
            spin.setRange(field.get("min", 1), field.get("max", 500))
            spin.setValue(field.get("value", 30))
            return spin

        line = QLineEdit()
        line.setPlaceholderText(field.get("placeholder", ""))
        return line

    def add_record(self):
        payload = {}
        for field in self.fields:
            widget = self.inputs[field["key"]]
            if isinstance(widget, QComboBox):
                payload[field["key"]] = widget.currentText()
            elif isinstance(widget, QSpinBox):
                payload[field["key"]] = widget.value()
            else:
                payload[field["key"]] = widget.text().strip()

        if any(value == "" for value in payload.values()):
            QMessageBox.warning(self, "Validare", "Completeaza toate campurile.")
            return

        try:
            credentials = self.creator(**payload)
            self._clear_inputs()
            self.load_data()
            if isinstance(credentials, dict) and credentials.get("username"):
                QMessageBox.information(
                    self,
                    "Cont creat",
                    "Contul de login a fost creat automat.\n\n"
                    f"Username: {credentials['username']}\n"
                    f"Parola: {credentials['password']}",
                )
        except Exception as error:
            QMessageBox.critical(self, "Eroare", str(error))

    def delete_selected(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Selectie", "Selecteaza un rand din tabel.")
            return

        record_id = self.table.item(row, 0).text()
        answer = QMessageBox.question(
            self,
            "Confirmare",
            "Stergi inregistrarea selectata?",
        )
        if answer != QMessageBox.StandardButton.Yes:
            return

        try:
            self.deleter(record_id)
            self.load_data()
        except Exception as error:
            QMessageBox.critical(self, "Eroare", str(error))

    def load_data(self):
        data = self.loader()
        self.table.setRowCount(len(data))
        for row_index, item in enumerate(data):
            for column_index, (key, _) in enumerate(self.columns):
                value = str(item.get(key, ""))
                cell = QTableWidgetItem(value)
                cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_index, column_index, cell)
        self.table.hideColumn(0)

    def _clear_inputs(self):
        for widget in self.inputs.values():
            if isinstance(widget, QLineEdit):
                widget.clear()
