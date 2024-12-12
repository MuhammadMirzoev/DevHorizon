import sqlite3

def create_database():
    conn = sqlite3.connect("DevHorizon.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role_id INTEGER NOT NULL,
            last_login TEXT,
            email TEXT,
            qualification_level INTEGER,
            FOREIGN KEY (role_id) REFERENCES roles (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            assigned_user_id INTEGER,
            status TEXT CHECK(status IN ('новая', 'в процессе', 'завершена')) DEFAULT 'новая',
            deadline TEXT,
            FOREIGN KEY (assigned_user_id) REFERENCES users (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS qualifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            points INTEGER NOT NULL,
            evaluation_date TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    cursor.executemany('''
        INSERT OR IGNORE INTO roles (name, description) VALUES (?, ?)
    ''', [
        ("Разработчик", "Отвечает за разработку и поддержку системы"),
        ("Дизайнер", "Создает UI/UX дизайн и макеты"),
        ("Менеджер", "Управляет проектами и задачами"),
        ("Администратор", "Админ"),
    ])

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
