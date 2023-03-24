from sqlite3 import *


with connect('database.db') as db:
    cursor = db.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS table1 (id INTEGER PRIMARY KEY, group_name TEXT )""") #groups
    cursor.execute(""" CREATE TABLE IF NOT EXISTS table2 (id INTEGER PRIMARY KEY, FIO TEXT, group_name TEXT )""") #students
    


