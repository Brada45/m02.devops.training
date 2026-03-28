import sqlite3
import os

DB_NAME = "test_users.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER
        )
    """)

    conn.commit()
    conn.close()


def create_user(name, email, age=None):
    if not name or not email:
        raise ValueError("Name and email required")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            (name, email, age)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        raise Exception("Email already exists")
    finally:
        conn.close()


def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, email, age FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {"id": row[0], "name": row[1], "email": row[2], "age": row[3]}
    return None


def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, email, age FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {"id": row[0], "name": row[1], "email": row[2], "age": row[3]}
    return None


def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, email, age FROM users")
    rows = cursor.fetchall()
    conn.close()

    return [
        {"id": r[0], "name": r[1], "email": r[2], "age": r[3]}
        for r in rows
    ]


def update_user(user_id, name=None, email=None, age=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    if not cursor.fetchone():
        conn.close()
        return False

    fields = []
    values = []

    if name is not None:
        fields.append("name = ?")
        values.append(name)
    if email is not None:
        fields.append("email = ?")
        values.append(email)
    if age is not None:
        fields.append("age = ?")
        values.append(age)

    if not fields:
        conn.close()
        return False

    values.append(user_id)

    try:
        cursor.execute(
            f"UPDATE users SET {', '.join(fields)} WHERE id = ?",
            values
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()

    deleted = cursor.rowcount > 0
    conn.close()
    return deleted


def delete_all_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users")
    conn.commit()
    conn.close()