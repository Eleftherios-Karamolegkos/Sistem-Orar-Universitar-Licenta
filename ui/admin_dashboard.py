from turtle import title

from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QHBoxLayout, QVBoxLayout, QStackedWidget
)
from ui.orar_page import OrarPage

class AdminDashboard(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panou Administrare")
        self.setGeometry(300,150,1000,600)
        main_layout = QHBoxLayout()

        # meniu stanga
        menu_layout = QVBoxLayout()
        title = QLabel("Sistem Management Orar Universitar")
        title.setStyleSheet("font-size:18px; font-weight:bold; padding:10px;")
        menu_layout.addWidget(title)

        btn_dashboard = QPushButton("Dashboard")
        btn_dashboard.setStyleSheet("text-align:left; padding:10px;")
        btn_profesori = QPushButton("Profesori")
        btn_profesori.setStyleSheet("text-align:left; padding:10px;")
        btn_studenti = QPushButton("Studenti")
        btn_studenti.setStyleSheet("text-align:left; padding:10px;")
        btn_materii = QPushButton('Materii')
        btn_materii.setStyleSheet("text-align:left; padding:10px;")
        btn_sali = QPushButton("Sali")
        btn_sali.setStyleSheet("text-align:left; padding:10px;")
        btn_orar = QPushButton("Orar")
        btn_orar.setStyleSheet("text-align:left; padding:10px;")

        menu_layout.addWidget(btn_dashboard)
        menu_layout.addWidget(btn_profesori)
        menu_layout.addWidget(btn_studenti)
        menu_layout.addWidget(btn_materii)
        menu_layout.addWidget(btn_sali)
        menu_layout.addWidget(btn_orar)

        main_layout.addStretch()

        # zona continut
        self.pages = QStackedWidget()

        page_dashboard = QLabel("Dashboard Administrare")
        page_profesori = QLabel("Gestionare Profesori")
        page_studenti = QLabel("Gestionare Studenti")
        page_materii = QLabel("Gestionare Materii")
        page_sali = QLabel("Gestionare Sali")
        page_orar = OrarPage()

        self.pages.addWidget(page_dashboard)
        self.pages.addWidget(page_profesori)
        self.pages.addWidget(page_studenti)
        self.pages.addWidget(page_materii)
        self.pages.addWidget(page_sali)
        self.pages.addWidget(page_orar)

        btn_dashboard.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        btn_profesori.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        btn_studenti.clicked.connect(lambda: self.pages.setCurrentIndex(2))
        btn_materii.clicked.connect(lambda: self.pages.setCurrentIndex(3))
        btn_sali.clicked.connect(lambda: self.pages.setCurrentIndex(4))
        btn_orar.clicked.connect(lambda: self.pages.setCurrentIndex(5))

        main_layout.addLayout(menu_layout)
        main_layout.addWidget(self.pages)
        self.setLayout(main_layout)
