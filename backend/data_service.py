from backend.database.db import get_connection


def _fetch_all(query, params=()):
    connection = get_connection()
    try:
        rows = connection.execute(query, params).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()


def _execute(query, params=()):
    connection = get_connection()
    try:
        connection.execute(query, params)
        connection.commit()
    finally:
        connection.close()


def list_professors():
    return _fetch_all("SELECT id, name, email FROM professors ORDER BY name")


def add_professor(name, email):
    _execute(
        "INSERT INTO professors (name, email) VALUES (?, ?)",
        (name.strip(), email.strip()),
    )


def delete_professor(record_id):
    _execute("DELETE FROM professors WHERE id = ?", (int(record_id),))


def list_students():
    return _fetch_all("SELECT id, name, an, email FROM students ORDER BY an, name")


def add_student(name, an, email):
    _execute(
        "INSERT INTO students (name, an, email) VALUES (?, ?, ?)",
        (name.strip(), int(an), email.strip()),
    )


def delete_student(record_id):
    _execute("DELETE FROM students WHERE id = ?", (int(record_id),))


def list_subjects():
    return _fetch_all("SELECT id, name, an, semester FROM subjects ORDER BY an, name")


def add_subject(name, an, semester):
    _execute(
        "INSERT INTO subjects (name, an, semester) VALUES (?, ?, ?)",
        (name.strip(), int(an), int(semester)),
    )


def delete_subject(record_id):
    _execute("DELETE FROM subjects WHERE id = ?", (int(record_id),))


def list_rooms():
    return _fetch_all("SELECT id, name, capacity FROM rooms ORDER BY name")


def add_room(name, capacity):
    _execute(
        "INSERT INTO rooms (name, capacity) VALUES (?, ?)",
        (name.strip(), int(capacity)),
    )


def delete_room(record_id):
    _execute("DELETE FROM rooms WHERE id = ?", (int(record_id),))
