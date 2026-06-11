import re
import secrets
import string
import unicodedata

from backend.database.db import get_connection, hash_password


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


def list_login_accounts():
    return _fetch_all(
        """
        SELECT id, username, role, full_name, an, initial_password
        FROM users
        WHERE role IN ('profesor', 'student')
        ORDER BY id DESC
        """
    )


def list_professors():
    return _fetch_all("SELECT id, name, email FROM professors ORDER BY name")


def add_professor(name, email):
    name = name.strip()
    email = email.strip()

    connection = get_connection()
    try:
        connection.execute(
            "INSERT INTO professors (name, email) VALUES (?, ?)",
            (name, email),
        )
        credentials = _create_login_account(connection, name, "profesor")
        connection.commit()
        return credentials
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def delete_professor(record_id):
    connection = get_connection()
    try:
        professor = connection.execute(
            "SELECT name FROM professors WHERE id = ?",
            (int(record_id),),
        ).fetchone()
        connection.execute("DELETE FROM professors WHERE id = ?", (int(record_id),))
        if professor:
            connection.execute(
                "DELETE FROM users WHERE role = 'profesor' AND full_name = ?",
                (professor["name"],),
            )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def list_students():
    return _fetch_all("SELECT id, name, an, email FROM students ORDER BY an, name")


def add_student(name, an, email):
    name = name.strip()
    email = email.strip()
    an = int(an)

    connection = get_connection()
    try:
        connection.execute(
            "INSERT INTO students (name, an, email) VALUES (?, ?, ?)",
            (name, an, email),
        )
        credentials = _create_login_account(connection, name, "student", an)
        connection.commit()
        return credentials
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def delete_student(record_id):
    connection = get_connection()
    try:
        student = connection.execute(
            "SELECT name, an FROM students WHERE id = ?",
            (int(record_id),),
        ).fetchone()
        connection.execute("DELETE FROM students WHERE id = ?", (int(record_id),))
        if student:
            connection.execute(
                """
                DELETE FROM users
                WHERE role = 'student'
                  AND full_name = ?
                  AND an = ?
                """,
                (student["name"], student["an"]),
            )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


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


def _create_login_account(connection, full_name, role, an=None):
    username = _unique_username(connection, _base_username(full_name, role))
    password = _generate_password(role)

    connection.execute(
        """
        INSERT INTO users (username, password_hash, initial_password, role, full_name, an)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (username, hash_password(password), password, role, full_name, an),
    )
    return {"username": username, "password": password}


def _base_username(full_name, role):
    prefix = "prof" if role == "profesor" else "stud"
    normalized = unicodedata.normalize("NFKD", full_name)
    ascii_name = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", ".", ascii_name.lower()).strip(".")
    return f"{prefix}.{slug or 'utilizator'}"


def _unique_username(connection, base):
    base = base[:48].rstrip(".")
    username = base
    counter = 2

    while connection.execute(
        "SELECT 1 FROM users WHERE username = ?",
        (username,),
    ).fetchone():
        suffix = f".{counter}"
        username = f"{base[:48 - len(suffix)]}{suffix}"
        counter += 1

    return username


def _generate_password(role):
    prefix = "Prof" if role == "profesor" else "Stud"
    alphabet = string.ascii_lowercase + string.digits
    token = "".join(secrets.choice(alphabet) for _ in range(6))
    return f"{prefix}-{token}"
