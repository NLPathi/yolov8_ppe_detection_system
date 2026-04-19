import sqlite3

conn = sqlite3.connect("projectDatabase.db")
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS userDetails")   # deletes the table itself
conn.commit()
conn.close()



# import sqlite3

# conn = sqlite3.connect("projectDatabase.db")
# c = conn.cursor()

# c.execute("SELECT * FROM userDetails")
# rows = c.fetchall()

# for row in rows:
#     print(row)

# conn.close()
