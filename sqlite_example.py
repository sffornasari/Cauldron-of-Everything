import sqlite3

# Create a connection to a database, implicitly creating it if it does not exist
con = sqlite3.connect("test.db")
# Create a database cursor to execute commands
cur = con.cursor()
# Check all tables in the database
res = cur.execute("SELECT name FROM sqlite_master").fetchall()
# Check if a given table is in the database
cur.execute("SELECT name FROM sqlite_master WHERE name='table'").fetchone() is True
# Create a table (throws an error if the table already exists)
cur.execute("CREATE TABLE tablename(attribute1, attribute2, attribute3)")
# Insert data in table
data = ("value0", 0, 0.0)
cur.execute(f"INSERT INTO tablename VALUES ('{data[0]}', {data[1]}, {data[2]})")
con.commit()  # Remember to commit the transaction after executing INSERT.
# Or do it with this notation
cur.execute(f"INSERT INTO tablename VALUES (?, ?, ?)", data)
con.commit()  # Remember to commit the transaction after executing INSERT.
data = [("value1", 1, 1.0), ("value2", 2, 2.0)]
cur.executemany("INSERT INTO tablename VALUES(?, ?, ?)", data)
con.commit()  # Remember to commit the transaction after executing INSERT.
# Replace existing values (or insert them if they don't exist)
value = "value0"
cur.execute(
    f"""UPDATE tablename
            SET attribute2 = {13}, attribute3 = {13.0}
            WHERE attribute1 = '{value}'
            """
)
con.commit()  # Remember to commit the transaction after executing INSERT.
# Print all row in table
for row in con.execute("SELECT attribute1, attribute2, attribute3 FROM tablename"):
    print(row)
# Close connection to database
con.close()
