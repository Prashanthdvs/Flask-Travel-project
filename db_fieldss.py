import sqlite3

conn = sqlite3.connect('databas_new1.db')
print("Opened database successfully")

#conn.execute('CREATE TABLE todoss (email TEXT, title TEXT, summary TEXT, type_of_place TEXT, Expenditure INTEGER, todo_owner TEXT)')

conn.execute('CREATE TABLE userssd (first_name TEXT, last_name TEXT, email TEXT, password TEXT)')

print("Table created successfully")
conn.close()