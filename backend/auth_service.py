import hashlib

from backend.database.db import get_connection


def authenticate(username, password):
    username = username.strip()
    password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

    connection = get_connection()
    try:
        user = connection.execute(
            """
            SELECT id, username, role, full_name, an
            FROM users
            WHERE username = ? AND password_hash = ?
            """,
            (username, password_hash),
        ).fetchone()
        return dict(user) if user else None
    finally:
        connection.close()
