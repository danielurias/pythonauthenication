import sqlite3


def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

class FightersDB:

	def __init__(self):
		self.connection = sqlite3.connect("fighters_db.db")
		self.connection.row_factory = dict_factory
		self.cursor = self.connection.cursor()

	def insertFighter(self, name, color, style, stock, hp):
		data = [name, color, style, stock, hp]
		self.cursor.execute("INSERT INTO fighters (name, color, style, stock, hp) VALUES (?, ?, ?, ?, ?)",data)
		self.connection.commit()


	def getAllFighters(self):
		self.cursor.execute("SELECT * FROM fighters")
		restaurants = self.cursor.fetchall()
		return restaurants

	def getOneFighter(self, fighter_id):
		data = [fighter_id]
		self.cursor.execute("SELECT * FROM fighters WHERE id = ?", data)
		return self.cursor.fetchone()

	def updateFighter(self, name, color, style, stock, hp, fighter_id):
		data = [name, color, style, stock, hp, fighter_id]
		self.cursor.execute("UPDATE fighters SET name = ?, color = ?, style = ?, stock = ?, hp = ? WHERE id = ?", data)
		self.connection.commit()

	def deleteFighter(self, fighter_id):
		data = [fighter_id]
		self.cursor.execute("DELETE FROM fighters WHERE id = ?", data)
		self.connection.commit()

	def getUserEmail(self, email):
		data = [email]
		self.cursor.execute("SELECT * FROM users WHERE email = ?", data)
		results = self.cursor.fetchone()
		return results

	def registerUser(self, first_name, last_name, email, password):
		data = [first_name, last_name, email, password]
		self.cursor.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (?, ?, ?, ?)", data)
		self.connection.commit()

