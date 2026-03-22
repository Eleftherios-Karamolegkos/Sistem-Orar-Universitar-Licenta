from backend.database.db import get_connection
import random

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


def generate_orar():
    zile = ["Luni", "Marti", "Miercuri", "Joi", "Vineri"]
    ore = ["09:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00", "17:00-19:00"]

    materii = ["POO", "BD", "AI", "Retele", "PPCD", "DAM"]
    profesori = ["Popescu", "Ionescu", "Georgescu", "Vasilescu", "Dumitrescu", "Stan"]
    sali = ["AP11", "D255", "D217", "DP18", "D316", "BI22"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM orar")

    for zi in zile:
        for ora in ore:
            materie = random.choice(materii)
            profesor = random.choice(profesori)
            sala = random.choice(sali)

            #verificare confict
            cursor.execute("""
            SELECT * FROM orar
            WHERE zi=%s AND ora=%s
            AND (profesor=%s OR sala=%s)
            """, (zi, ora, profesor, sala))
            
            conflict = cursor.fetchone()

            if not conflict:
                cursor.execute("""
                INSERT INTO orar (zi, ora, materie, profesor, sala)
                VALUES (%s, %s, %s, %s, %s)
                """, (zi, ora, materie, profesor, sala))
    conn.commit()
    conn.close()

def get_orar_student(grupa):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orar WHERE grupa=%s", (grupa,))
    data = cursor.fetchall()
    conn.close()
    return data
    
def get_orar_profesor(nume):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orar WHERE profesor=%s", (nume,))
    data = cursor.fetchall()
    conn.close()
    return data
    
