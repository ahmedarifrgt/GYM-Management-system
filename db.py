import sqlite3

def connect_db():
    conn = sqlite3.connect("gym.db")
    cur = conn.cursor()

    # Members Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            phone TEXT,
            address TEXT,
            membership_type TEXT,
            start_date TEXT,
            end_date TEXT
        )
    """)

    # Attendance Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER,
            checkin_time TEXT,
            checkout_time TEXT
        )
    """)

    # Transactions Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER,
            amount_paid REAL,
            date TEXT
        )
    """)

    conn.commit()
    conn.close()
