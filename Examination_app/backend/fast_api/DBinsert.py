import sqlite3

DB_NAME = "edtech.db"
username = "Sudha"
password = "Sudha"  
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

try:
    cursor.execute("INSERT INTO admin (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    print("Admin inserted successfully.")
except sqlite3.IntegrityError:
    print("Admin already exists.")
finally:
    conn.close()
