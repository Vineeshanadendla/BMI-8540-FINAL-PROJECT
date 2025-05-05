import sqlite3

with open('schema.sql', 'r') as f:
    schema = f.read()

conn = sqlite3.connect('bacteria.db')
cursor = conn.cursor()
cursor.executescript(schema)
conn.commit()
conn.close()

print("Database initialized successfully using Python.")
