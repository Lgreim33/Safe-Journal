import sqlite3


#connect to the database
def create_connection():
    return sqlite3.connect("journal_app.db")

#create the database
def initialize_db():
    conn = create_connection()
    cursor = conn.cursor()

    #create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')

    #create JournalEntries table with a foreign key to Users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS JournalEntries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            entry TEXT,
            date TEXT,
            FOREIGN KEY (user_id) REFERENCES Users (id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()

#initialize the database on import
initialize_db()