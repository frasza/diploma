import sqlite3

from _config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:

    c = connection.cursor()
    
    c.execute("""CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE, email TEXT NOT NULL UNIQUE, password TEXT NOT NULL)""")

    c.execute("""CREATE TABLE entries(entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL, description TEXT NOT NULL, changes TEXT NOT NULL, category TEXT NOT NULL,
        costs TEXT NOT NULL, approval TEXT NOT NULL, work TEXT NOT NULL, user_id INTEGER NOT NULL REFERENCES users(id))""")