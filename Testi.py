import sqlite3

db = sqlite3.connect("testaus.db")
db.isolation_level = None

c = db.cursor()

c.execute("CREATE TABLE Tuotteet(id INTEGER PRIMARY KEY, nimi TEXT, hinta INTEGER)")
c.execute("INSERT INTO Tuotteet(nimi,hinta) values ('retiisi', 7)")
c.execute("INSERT INTO Tuotteet(nimi,hinta) values ('porkkana', 5)")
c.execute("INSERT INTO Tuotteet(nimi,hinta) values ('nauris', 4)")
c.execute("INSERT INTO Tuotteet(nimi,hinta) values ('lanttu', 8)")
c.execute("INSERT INTO Tuotteet(nimi,hinta) values ('selleri', 4)")

c.execute("SELECT * FROM Tuotteet")
print(c.fetchall())
c.execute("DROP TABLE Tuotteet")
