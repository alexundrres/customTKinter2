from sqlite3 import *


with connect('database.db') as db:
    cursor = db.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS table1 (id INTEGER PRIMARY KEY, name TEXT,  expenses TEXT )""")
    cursor.execute(""" CREATE TABLE IF NOT EXISTS table2 (id INTEGER PRIMARY KEY, names TEXT, paid TEXT, 
    FOREIGN KEY (names) REFERENCES table1 (name) ON DELETE CASCADE) """)


