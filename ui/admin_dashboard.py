from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from backend.data_service import (
    add_professor,
    add_room,
    add_student,
    add_subject,
    delete_professor,
    delete_room,
    delete_student,
    delete_subject,
    list_professors,
    list_rooms,
    list_students,
    list_subjects,
)
from backend.orar_service import get_dashboard_stats
from ui.management_page import ManagementPage
from ui.orar_page import OrarPage


class AdminDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panou Administrare")
        self.setMinimumSize(1100, 700)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("panel")
        sidebar.setFixedWidth(260)
        menu_layout = QVBoxLayout(sidebar)
        menu_layout.setContentsMargins(18, 22, 18, 22)
        menu_layout.setSpacing(8)

        title = QLabel("Orar Universitar")
        title.setObjectName("title")
        menu_layout.addWidget(title)

        subtitle = QLabel("Panou administrare")
        subtitle.setObjectName("muted")
        menu_layout.addWidget(subtitle)

        self.pages = QStackedWidget()
        self.menu_buttons = []

        pages = [
            ("Dashboard", DashboardPage()),
            ("Profesori", self._professors_page()),
            ("Studenti", self._students_page()),
            ("Materii", self._subjects_page()),
            ("Sali", self._rooms_page()),
            ("Orar", OrarPage()),
        ]

        for index, (name, page) in enumerate(pages):
            button = QPushButton(name)
            button.setObjectName("menuButton")
            button.setCheckable(True)
            button.clicked.connect(lambda checked=False, page_index=index: self.show_page(page_index))
            menu_layout.addWidget(button)
            self.menu_buttons.append(button)
            self.pages.addWidget(page)

        menu_layout.addStretch()
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages, 1)
        self.show_page(0)

    def show_page(self, index):
        self.pages.setCurrentIndex(index)
        for button_index, button in enumerate(self.menu_buttons):
            button.setChecked(button_index == index)

        page = self.pages.widget(index)
        refresh = (
            getattr(page, "refresh", None)
            or getattr(page, "refresh_all", None)
            or getattr(page, "load_data", None)
        )
        if callable(refresh):
            refresh()

    def _professors_page(self):
        return ManagementPage(
            "Gestionare profesori",
            [
                {"key": "name", "label": "Nume", "type": "text", "placeholder": "Ex: Popescu Andrei"},
                {"key": "email", "label": "Email", "type": "text", "placeholder": "nume@universitate.ro"},
            ],
            [("id", "ID"), ("name", "Nume"), ("email", "Email")],
            list_professors,
            add_professor,
            delete_professor,
        )

    def _students_page(self):
        return ManagementPage(
            "Gestionare studenti",
            [
                {"key": "name", "label": "Nume", "type": "text", "placeholder": "Ex: Student Exemplu"},
                {"key": "an", "label": "An", "type": "combo", "values": [1, 2, 3]},
                {"key": "email", "label": "Email", "type": "text", "placeholder": "student@universitate.ro"},
            ],
            [("id", "ID"), ("name", "Nume"), ("an", "An"), ("email", "Email")],
            list_students,
            add_student,
            delete_student,
        )

    def _subjects_page(self):
        return ManagementPage(
            "Gestionare materii",
            [
                {"key": "name", "label": "Materie", "type": "text", "placeholder": "Ex: Algoritmi"},
                {"key": "an", "label": "An", "type": "combo", "values": [1, 2, 3]},
                {"key": "semester", "label": "Semestru", "type": "combo", "values": [1, 2]},
            ],
            [("id", "ID"), ("name", "Materie"), ("an", "An"), ("semester", "Semestru")],
            list_subjects,
            add_subject,
            delete_subject,
        )

    def _rooms_page(self):
        return ManagementPage(
            "Gestionare sali",
            [
                {"key": "name", "label": "Sala", "type": "text", "placeholder": "Ex: C401"},
                {"key": "capacity", "label": "Capacitate", "type": "spin", "min": 1, "max": 400, "value": 30},
            ],
            [("id", "ID"), ("name", "Sala"), ("capacity", "Capacitate")],
            list_rooms,
            add_room,
            delete_room,
        )


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Dashboard")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        subtitle = QLabel("Rezumat rapid pentru datele aplicatiei.")
        subtitle.setObjectName("muted")
        layout.addWidget(subtitle)

        self.grid = QGridLayout()
        self.grid.setSpacing(14)
        layout.addLayout(self.grid)
        layout.addStretch()

        self.cards = {}
        for index, key in enumerate(["orar", "profesori", "studenti", "materii", "sali"]):
            card = StatCard(key.capitalize())
            self.cards[key] = card
            self.grid.addWidget(card, index // 3, index % 3)

        self.refresh()

    def refresh(self):
        stats = get_dashboard_stats()
        for key, value in stats.items():
            self.cards[key].set_value(value)


class StatCard(QFrame):
    def __init__(self, label):
        super().__init__()
        self.setObjectName("statCard")
        self.setMinimumHeight(120)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)

        title = QLabel(label)
        title.setObjectName("muted")
        self.value = QLabel("0")
        self.value.setObjectName("title")

        layout.addWidget(title)
        layout.addWidget(self.value)
        layout.addStretch()

    def set_value(self, value):
        self.value.setText(str(value))
