import sqlite3

con = sqlite3.connect(':memory:')
cur = con.cursor()

cur.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, first_name VARCHAR(100), last_name VARCHAR(30))')
con.commit()

cur.execute('INSERT INTO users (first_name, last_name) VALUES ("Aliaksandr", "Klimovich")')
con.commit()
print(cur.lastrowid)

cur.execute('SELECT * FROM users')
print(cur.fetchall())

cur.close()
con.close()
