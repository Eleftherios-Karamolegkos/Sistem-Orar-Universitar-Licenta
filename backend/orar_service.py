import random

from backend.database.db import get_connection
from backend.notification_service import notify_schedule_changed


DAYS = ["Luni", "Marti", "Miercuri", "Joi", "Vineri"]
HOURS = ["08:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00"]
YEARS = [1, 2, 3]
ORDER_BY_SCHEDULE = """
ORDER BY
    CASE zi
        WHEN 'Luni' THEN 1
        WHEN 'Marti' THEN 2
        WHEN 'Miercuri' THEN 3
        WHEN 'Joi' THEN 4
        WHEN 'Vineri' THEN 5
        ELSE 6
    END,
    ora,
    an
"""


def _fetch_all(query, params=()):
    connection = get_connection()
    try:
        rows = connection.execute(query, params).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()


def _fetch_one(query, params=()):
    connection = get_connection()
    try:
        row = connection.execute(query, params).fetchone()
        return dict(row) if row else None
    finally:
        connection.close()


def get_orar():
    return _fetch_all(f"SELECT * FROM orar {ORDER_BY_SCHEDULE}")


def get_orar_student(an):
    return _fetch_all(
        f"SELECT * FROM orar WHERE an = ? {ORDER_BY_SCHEDULE}",
        (int(an),),
    )


def get_orar_profesor(nume):
    return _fetch_all(
        f"SELECT * FROM orar WHERE profesor = ? {ORDER_BY_SCHEDULE}",
        (nume,),
    )


def add_orar(zi, ora, materie, profesor, sala, an):
    zi = zi.strip()
    ora = ora.strip()
    materie = materie.strip()
    profesor = profesor.strip()
    sala = sala.strip()
    an = int(an)

    if not all([zi, ora, materie, profesor, sala]):
        raise ValueError("Completeaza toate campurile inainte de salvare.")

    conflict = check_conflict(zi, ora, profesor, sala, an)
    if conflict:
        raise ValueError(_conflict_message(conflict, profesor, sala, an))

    connection = get_connection()
    try:
        connection.execute(
            """
            INSERT INTO orar (zi, ora, materie, profesor, sala, an)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (zi, ora, materie, profesor, sala, an),
        )
        connection.commit()
    finally:
        connection.close()
    notify_schedule_changed(
        "Intrare adaugata",
        f"{zi}, {ora}, anul {an}, {materie}, {profesor}, sala {sala}",
    )


def delete_orar(entry_id=None):
    connection = get_connection()
    try:
        if entry_id is None:
            details = "Toate intrarile din orar au fost sterse."
            connection.execute("DELETE FROM orar")
            action = "Orar golit"
        else:
            existing = connection.execute(
                "SELECT * FROM orar WHERE id = ?",
                (int(entry_id),),
            ).fetchone()
            details = _entry_details(dict(existing)) if existing else f"ID {entry_id}"
            connection.execute("DELETE FROM orar WHERE id = ?", (int(entry_id),))
            action = "Intrare stearsa"
        connection.commit()
    finally:
        connection.close()
    notify_schedule_changed(action, details)


def check_conflict(zi, ora, profesor, sala, an, exclude_id=None):
    params = [zi, ora, profesor, sala, int(an)]
    extra_filter = ""
    if exclude_id is not None:
        extra_filter = " AND id != ?"
        params.append(int(exclude_id))

    return _fetch_one(
        f"""
        SELECT * FROM orar
        WHERE zi = ?
          AND ora = ?
          AND (profesor = ? OR sala = ? OR an = ?)
          {extra_filter}
        LIMIT 1
        """,
        tuple(params),
    )


def generate_orar():
    connection = get_connection()
    try:
        professors = [
            row["name"]
            for row in connection.execute("SELECT name FROM professors ORDER BY name").fetchall()
        ]
        rooms = [
            row["name"]
            for row in connection.execute("SELECT name FROM rooms ORDER BY name").fetchall()
        ]
        subjects = [
            dict(row)
            for row in connection.execute("SELECT name, an FROM subjects ORDER BY an, name").fetchall()
        ]

        if not professors or not rooms or not subjects:
            raise ValueError("Adauga profesori, sali si materii inainte de generare.")

        connection.execute("DELETE FROM orar")

        for an in YEARS:
            year_subjects = [subject for subject in subjects if subject["an"] == an]
            for subject in year_subjects:
                _place_subject(connection, subject["name"], an, professors, rooms)

        generated_count = connection.execute("SELECT COUNT(*) FROM orar").fetchone()[0]
        connection.commit()
    finally:
        connection.close()

    notify_schedule_changed(
        "Orar generat automat",
        f"Au fost generate {generated_count} intrari.",
    )
    return get_orar()


def get_dashboard_stats():
    connection = get_connection()
    try:
        stats = {
            "orar": connection.execute("SELECT COUNT(*) FROM orar").fetchone()[0],
            "profesori": connection.execute("SELECT COUNT(*) FROM professors").fetchone()[0],
            "studenti": connection.execute("SELECT COUNT(*) FROM students").fetchone()[0],
            "materii": connection.execute("SELECT COUNT(*) FROM subjects").fetchone()[0],
            "sali": connection.execute("SELECT COUNT(*) FROM rooms").fetchone()[0],
        }
        return stats
    finally:
        connection.close()


def _place_subject(connection, materie, an, professors, rooms):
    slots = [(day, hour) for day in DAYS for hour in HOURS]
    random.shuffle(slots)

    for zi, ora in slots:
        shuffled_professors = professors[:]
        shuffled_rooms = rooms[:]
        random.shuffle(shuffled_professors)
        random.shuffle(shuffled_rooms)

        for profesor in shuffled_professors:
            for sala in shuffled_rooms:
                conflict = connection.execute(
                    """
                    SELECT 1 FROM orar
                    WHERE zi = ?
                      AND ora = ?
                      AND (profesor = ? OR sala = ? OR an = ?)
                    LIMIT 1
                    """,
                    (zi, ora, profesor, sala, an),
                ).fetchone()

                if not conflict:
                    connection.execute(
                        """
                        INSERT INTO orar (zi, ora, materie, profesor, sala, an)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (zi, ora, materie, profesor, sala, an),
                    )
                    return


def _conflict_message(conflict, profesor, sala, an):
    if conflict["profesor"] == profesor:
        return f"Conflict: profesorul {profesor} are deja curs in acel interval."
    if conflict["sala"] == sala:
        return f"Conflict: sala {sala} este deja ocupata in acel interval."
    if conflict["an"] == int(an):
        return f"Conflict: anul {an} are deja curs in acel interval."
    return "Conflict de orar."


def _entry_details(entry):
    return (
        f"{entry['zi']}, {entry['ora']}, anul {entry['an']}, "
        f"{entry['materie']}, {entry['profesor']}, sala {entry['sala']}"
    )
