import sqlite3

conn=sqlite3.connect('database.db')

conn.execute('''CREATE TABLE users
			(email TEXT PRIMARY KEY,
			password TEXT,
			firstName TEXT,
			lastName TEXT
			)''')

conn.execute('''CREATE TABLE blogs
			(email TEXT,
			title TEXT,
			blog TEXT,
			blogid INTEGER PRIMARY KEY,
			createddate TIME,
			FOREIGN KEY(email) REFERENCES users(email)
			)''')

conn.close()