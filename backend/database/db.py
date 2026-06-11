import hashlib
import os
import sqlite3
from pathlib import Path


DB_PATH = Path(os.environ.get("ORAR_DB_PATH", Path(__file__).with_name("orar.db")))


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    initial_password TEXT NOT NULL DEFAULT '',
    role TEXT NOT NULL CHECK (role IN ('admin', 'profesor', 'student')),
    full_name TEXT NOT NULL,
    an INTEGER
);

CREATE TABLE IF NOT EXISTS professors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    an INTEGER NOT NULL CHECK (an BETWEEN 1 AND 3),
    email TEXT NOT NULL DEFAULT '',
    UNIQUE(name, an)
);

CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    an INTEGER NOT NULL CHECK (an BETWEEN 1 AND 3),
    semester INTEGER NOT NULL CHECK (semester BETWEEN 1 AND 2),
    UNIQUE(name, an)
);

CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    capacity INTEGER NOT NULL DEFAULT 30
);

CREATE TABLE IF NOT EXISTS orar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zi TEXT NOT NULL,
    ora TEXT NOT NULL,
    materie TEXT NOT NULL,
    profesor TEXT NOT NULL,
    sala TEXT NOT NULL,
    an INTEGER NOT NULL CHECK (an BETWEEN 1 AND 3)
);
"""


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    connection = get_connection()
    try:
        connection.executescript(SCHEMA)
        _migrate_database(connection)
        _seed_database(connection)
        connection.commit()
    finally:
        connection.close()


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def _migrate_database(connection):
    columns = {
        row["name"]
        for row in connection.execute("PRAGMA table_info(users)").fetchall()
    }
    if "initial_password" not in columns:
        connection.execute(
            "ALTER TABLE users ADD COLUMN initial_password TEXT NOT NULL DEFAULT ''"
        )


def _seed_database(connection):
    users = [
        ("admin", "admin123", "admin", "Administrator", None),
        ("popescu", "prof123", "profesor", "Popescu Andrei", None),
        ("ionescu", "prof123", "profesor", "Ionescu Maria", None),
        ("student1", "student123", "student", "Student Anul 1", 1),
        ("student2", "student123", "student", "Student Anul 2", 2),
        ("student3", "student123", "student", "Student Anul 3", 3),
    ]
    connection.executemany(
        """
        INSERT OR IGNORE INTO users
            (username, password_hash, initial_password, role, full_name, an)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [(u, hash_password(p), p, role, name, an) for u, p, role, name, an in users],
    )
    for username, password, _, _, _ in users:
        connection.execute(
            """
            UPDATE users
            SET initial_password = ?
            WHERE username = ?
              AND (initial_password IS NULL OR initial_password = '')
            """,
            (password, username),
        )

    professors = [
        ("Popescu Andrei", "andrei.popescu@universitate.ro"),
        ("Ionescu Maria", "maria.ionescu@universitate.ro"),
        ("Georgescu Vlad", "vlad.georgescu@universitate.ro"),
        ("Dumitrescu Elena", "elena.dumitrescu@universitate.ro"),
    ]
    connection.executemany(
        "INSERT OR IGNORE INTO professors (name, email) VALUES (?, ?)",
        professors,
    )

    students = [
        ("Student Anul 1", 1, "student1@universitate.ro"),
        ("Student Anul 2", 2, "student2@universitate.ro"),
        ("Student Anul 3", 3, "student3@universitate.ro"),
    ]
    for name, an, email in students:
        connection.execute(
            """
            INSERT INTO students (name, an, email)
            SELECT ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM students WHERE name = ? AND an = ?
            )
            """,
            (name, an, email, name, an),
        )

    subjects = [
        ("Programare orientata pe obiecte", 1, 1),
        ("Structuri de date", 1, 1),
        ("Baze de date", 2, 1),
        ("Retele de calculatoare", 2, 2),
        ("Inteligenta artificiala", 3, 1),
        ("Inginerie software", 3, 2),
    ]
    connection.executemany(
        "INSERT OR IGNORE INTO subjects (name, an, semester) VALUES (?, ?, ?)",
        subjects,
    )

    rooms = [
        ("A101", 40),
        ("A202", 35),
        ("B303", 50),
        ("Lab 1", 28),
        ("Lab 2", 28),
    ]
    connection.executemany(
        "INSERT OR IGNORE INTO rooms (name, capacity) VALUES (?, ?)",
        rooms,
    )
