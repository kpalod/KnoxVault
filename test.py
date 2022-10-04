import pandas as pd
import sqlite3
import sqlalchemy 

try:
    conn = sqlite3.connect("data.db")    
except Exception as e:
    print(e)

#Now in order to read in pandas dataframe we need to know table name
cursor = conn.cursor()
#cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
cursor.execute("PRAGMA table_info(users);")

print(f"Table Name : {cursor.fetchall()}")

df = pd.read_sql_query('SELECT * FROM users', conn)
conn.close()