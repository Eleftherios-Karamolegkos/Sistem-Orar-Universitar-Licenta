import sys

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication

from backend.database.db import initialize_database
from ui.login_window import LoginWindow


APP_STYLE = """
QWidget {
    background-color: #f5f7fb;
    color: #172033;
    font-family: "Segoe UI";
    font-size: 14px;
}
QFrame#loginCard,
QFrame#panel,
QFrame#statCard {
    background-color: #ffffff;
    border: 1px solid #dfe5ef;
    border-radius: 8px;
}
QLabel#title {
    color: #101828;
    font-size: 24px;
    font-weight: 700;
}
QLabel#sectionTitle {
    color: #101828;
    font-size: 20px;
    font-weight: 700;
}
QLabel#muted {
    color: #667085;
}
QLineEdit,
QComboBox,
QSpinBox {
    background-color: #ffffff;
    border: 1px solid #cfd8e3;
    border-radius: 6px;
    padding: 8px;
}
QLineEdit:focus,
QComboBox:focus,
QSpinBox:focus {
    border: 1px solid #2563eb;
}
QPushButton {
    background-color: #2563eb;
    border: 1px solid #2563eb;
    border-radius: 6px;
    color: #ffffff;
    font-weight: 600;
    padding: 9px 12px;
}
QPushButton:hover {
    background-color: #1d4ed8;
}
QPushButton#secondary {
    background-color: #ffffff;
    border: 1px solid #cfd8e3;
    color: #172033;
}
QPushButton#secondary:hover {
    background-color: #eef2f7;
}
QPushButton#danger {
    background-color: #dc2626;
    border-color: #dc2626;
}
QPushButton#danger:hover {
    background-color: #b91c1c;
}
QPushButton#menuButton {
    background-color: transparent;
    border: 0;
    border-radius: 6px;
    color: #344054;
    font-weight: 600;
    padding: 10px 12px;
    text-align: left;
}
QPushButton#menuButton:hover,
QPushButton#menuButton:checked {
    background-color: #e8f0ff;
    color: #1d4ed8;
}
QTableWidget {
    background-color: #ffffff;
    border: 1px solid #dfe5ef;
    border-radius: 6px;
    gridline-color: #eef2f7;
    selection-background-color: #dbeafe;
    selection-color: #101828;
}
QHeaderView::section {
    background-color: #eef2f7;
    border: 0;
    color: #344054;
    font-weight: 700;
    padding: 8px;
}
"""


def main():
    initialize_database()

    app = QApplication(sys.argv)
    app.setApplicationName("Sistem Orar Universitar")
    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet(APP_STYLE)

    window = LoginWindow()
    window.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
