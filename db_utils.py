import sqlite3
import os
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, 'factory.db')  # ← همه جا فقط همین فایل

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# init_db و بقیه تابع‌ها مثل قبل

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # جدول کاربران
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_code TEXT UNIQUE,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        full_name TEXT,
        email TEXT,
        role TEXT NOT NULL,
        is_active INTEGER DEFAULT 1,
        created_at TEXT DEFAULT (datetime('now','localtime'))
        )
    ''')


    # جدول تجهیزات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS equipments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            name TEXT NOT NULL,
            type TEXT,
            location TEXT,
            parent_equipment TEXT,
            department TEXT,
            install_date TEXT,
            is_active INTEGER DEFAULT 1
        )
    ''')

    # افزودن کاربر مدیر اگر وجود ندارد
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        admin_password = 'admin'
        hashed_password = generate_password_hash(admin_password)
        cursor.execute('''
            INSERT INTO users (username, password, full_name, email, role, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('admin', hashed_password, 'Administrator', 'admin@example.com', 'admin', 1))

    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user
