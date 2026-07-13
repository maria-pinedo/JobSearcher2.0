import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "jobsearcher.db")


def init_db():
    """
    Initializes the SQLite database and creates all necessary tables
    for the Candidate Profile Database phase.
    """
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Enable foreign key support in SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Candidates Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            phone TEXT,
            visa_status TEXT DEFAULT 'F-1 STEM OPT',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 2. Skills Table (One-to-Many)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER,
            skill_name TEXT,
            FOREIGN KEY (candidate_id) REFERENCES candidates (id) ON DELETE CASCADE
        )
    """)

    # 3. Education Table (One-to-Many)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS education (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER,
            school TEXT,
            degree TEXT,
            major TEXT,
            graduation_date TEXT,
            FOREIGN KEY (candidate_id) REFERENCES candidates (id) ON DELETE CASCADE
        )
    """)

    # 4. Experience Table (One-to-Many)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS experience (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER,
            title TEXT,
            company TEXT,
            start_date TEXT,
            end_date TEXT,
            responsibilities TEXT, -- Stored as a JSON string or newline-separated text
            FOREIGN KEY (candidate_id) REFERENCES candidates (id) ON DELETE CASCADE
        )
    """)

    # 5. Projects Table (One-to-Many)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER,
            name TEXT,
            tools TEXT, -- Stored as a comma-separated string
            description TEXT,
            FOREIGN KEY (candidate_id) REFERENCES candidates (id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()
    print(f"Database initialized successfully at: {DB_PATH}")


if __name__ == "__main__":
    init_db()