import sqlite3

from _config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:

    c = connection.cursor()
    
    c.execute("""CREATE TABLE uporabniki(id INTEGER PRIMARY KEY AUTOINCREMENT,
        uporabniskoime TEXT NOT NULL UNIQUE, email TEXT NOT NULL UNIQUE, geslo TEXT NOT NULL)""")

    c.execute("""CREATE TABLE vnosi(vnos_id INTEGER PRIMARY KEY AUTOINCREMENT,
        naslov TEXT NOT NULL, opis TEXT NOT NULL, spremembe TEXT NOT NULL, kategorija TEXT NOT NULL,
        stroski TEXT NOT NULL, odobritev TEXT NOT NULL, vpliv TEXT NOT NULL, uporabnik_id INTEGER NOT NULL REFERENCES uporabniki(id))""")