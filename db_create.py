__author__ = 'Beryl'
import sqlite3

from config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:
    #get a cursor object used to execute SQL commands
    c = connection.cursor()

    #create the table
    c.execute("""CREATE TABLE tasks(task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL, due_date TEXT NOT NULL, priority INTEGER NOT NULL, status INTEGER
    NOT NULL)""")

    #Insert dummy data into the table

    c.execute('INSERT INTO tasks (name, due_date, priority, status)''VALUES("Finish this tutorial", "09/16/2015", 10, 1)')
    c.execute('INSERT INTO tasks (name, due_date, priority, status)''VALUES("Finsh Real Python Course 2", "09/17/2015", 10, 1)')