from backend.database.db import get_connection

def get_orar():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orar")
    data = cursor.fetchall()
    cursor.close()
    return data

def add_orar(zi, ora, materie, profesor, sala):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO orar (zi, ora, materie, profesor, sala)
    values (%s, %s, %s, %s, %s)
    """

    cursor.execute(query, (zi, ora, materie, profesor, sala))
    conn.commit()
    conn.close()

def check_conflict(zi, ora, profesor, sala):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT * FROM orar
    WHERE zi=%s AND ora=%s
    AND (profesor=%s OR sala=%s)
    """

    cursor.execute(query, (zi, ora, profesor, sala))
    result = cursor.fetchone()
    conn.close()
    return result
