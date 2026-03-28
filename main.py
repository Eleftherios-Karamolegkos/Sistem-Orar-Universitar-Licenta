import sys
from PyQt6.QtWidgets import QApplication
from ui.login_window import LoginWindow

app = QApplication(sys.argv)

window = LoginWindow()
window.show()

sys.exit(app.exec())

app.setStyleSheet("""
            QWidget {
                  background-color: #121212;
                  color: #ffffff;
                  font-family: Segoe UI;
                  font-size: 14px;
                  }
            QPushButton {
                  background-color: #1f1f1f;
                  border: 1px solid #333;
                  padding: 8px;
                  border-radius: 8px;
                  }
            QPushButton:hover {
                  background-color: #2a2a2a;
                  }
            QLineEdit, QComboBox {
                  background-color: #1f1f1f;
                  border: 1px solid #333;
                  padding: 6px;
                  border-radius: 6px;
                  }
            QTableWidget {
                  background-color: #1a1a1a;
                  gridine-color: #333;
                  }
            QHeaderView::section {
                  background-color: #222;
                  padding: 5px;
                  boeder: none;
                  }
                  """)