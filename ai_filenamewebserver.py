import http.server
import sqlite3
from random import randint

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        
        # Connect to the SQLite database file
        conn = sqlite3.connect('mysqlitedb')
        c = conn.cursor()
        
        # Get the number of rows in the "filenames" table
        c.execute("SELECT COUNT(*) FROM filenames")
        result = c.fetchone()
        num_rows = result[0]
        
        # Get a random row from the "filenames" table using the number of rows as the upper bound
        for i in range(10):
            c.execute("SELECT filename FROM filenames WHERE id=?", (randint(1, num_rows),))
            row = c.fetchone()
            
            # Write the string from the database to the output
            self.wfile.write(row[0].encode('utf-8'))
            self.wfile.write(b'\n')
            
        conn.close()

if __name__ == '__main__':
    server = http.server.HTTPServer(('localhost', 8000), MyRequestHandler)
    server.serve_forever()
