import os
import sqlite3

# Connect to the SQLite database file
conn = sqlite3.connect('mysqlitedb')
c = conn.cursor()

# Get a list of all files in the current directory
directory_path = r'directory'

# Get a list of all files in the directory
files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

# Check if each filename exists in the "filenames" table before inserting it
for file in files:
    c.execute("SELECT COUNT(*) FROM filenames WHERE filename=?", (file,))
    result = c.fetchone()
    num_rows = result[0]
    
    # If the filename doesn't exist, insert it into the "filenames" table
    if num_rows == 0:
        c.execute("INSERT INTO filenames (filename) VALUES (?)", (file,))
               
conn.commit()
conn.close()
