import sys

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication

from backend.database.db import initialize_database
from ui.login_window import LoginWindow


APP_STYLE = """
QWidget {
    background-color: #f4f6f8;
    color: #17202a;
    font-family: "Segoe UI";
    font-size: 14px;
}
QLabel {
    background-color: transparent;
}
QStackedWidget {
    background-color: #f4f6f8;
    border: 0;
}
QFrame#sidebar {
    background-color: #18202a;
    border: 0;
}
QFrame#loginCard,
QFrame#panel,
QFrame#statCard {
    background-color: #ffffff;
    border: 1px solid #dde4ec;
    border-radius: 8px;
}
QFrame#statCard {
    border-left: 4px solid #14b8a6;
}
QLabel#brandBadge {
    background-color: #14b8a6;
    border-radius: 8px;
    color: #042f2e;
    font-size: 15px;
    font-weight: 800;
}
QLabel#title {
    color: #111827;
    font-size: 24px;
    font-weight: 700;
}
QFrame#sidebar QLabel#title {
    color: #ffffff;
}
QLabel#sectionTitle {
    color: #111827;
    font-size: 20px;
    font-weight: 700;
}
QLabel#muted {
    color: #6b7280;
}
QFrame#sidebar QLabel#muted {
    color: #a7b2c1;
}
QLabel#statLabel {
    color: #64748b;
    font-size: 13px;
    font-weight: 700;
}
QLabel#statValue {
    color: #0f172a;
    font-size: 30px;
    font-weight: 800;
}
QLineEdit,
QComboBox,
QSpinBox {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 8px;
}
QLineEdit:focus,
QComboBox:focus,
QSpinBox:focus {
    border: 1px solid #14b8a6;
}
QPushButton {
    background-color: #0f766e;
    border: 1px solid #0f766e;
    border-radius: 6px;
    color: #ffffff;
    font-weight: 600;
    padding: 9px 12px;
}
QPushButton:hover {
    background-color: #0d9488;
    border-color: #0d9488;
}
QPushButton#secondary {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    color: #17202a;
}
QPushButton#secondary:hover {
    background-color: #edf7f5;
    border-color: #99f6e4;
}
QPushButton#danger {
    background-color: #e11d48;
    border-color: #e11d48;
}
QPushButton#danger:hover {
    background-color: #be123c;
    border-color: #be123c;
}
QPushButton#menuButton {
    background-color: transparent;
    border: 0;
    border-radius: 6px;
    color: #d8dee9;
    font-weight: 600;
    padding: 10px 12px;
    text-align: left;
}
QFrame#sidebar QPushButton#menuButton {
    background-color: transparent;
}
QPushButton#menuButton:hover,
QPushButton#menuButton:checked {
    background-color: #243447;
    color: #5eead4;
}
QTableWidget {
    background-color: #ffffff;
    border: 1px solid #dde4ec;
    border-radius: 6px;
    gridline-color: #edf2f7;
    selection-background-color: #ccfbf1;
    selection-color: #111827;
}
QHeaderView::section {
    background-color: #eef7f5;
    border: 0;
    color: #334155;
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
