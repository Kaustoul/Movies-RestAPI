import sqlite3

class Database:
  def __init__(self, name):
    self.name = name
    self.con = None
    self.cur = None

  def connect(self):
    self.con = sqlite3.connect(self.name)
    self.cur = self.con.cursor()

  def create_table(self):
    self.cur.execute('''CREATE TABLE IF NOT EXISTS movies(
      id INTEGER PRIMARY KEY NOT NULL,
      description TEXT,
      release_year INTEGER NOT NULL CHECK(length(release_year) = 4)
      )''')
    self.con.commit()
    
  def insert_movie(self, movie_json):
    self.cursor.execute("INSERT INTO movies (name, description, release_year) VALUES (?, ?, ?)",
                        (movie_json['name'], movie_json['description'], movie_json['release_year']))
    self.connection.commit()

  def get_all_movies(self):
    self.cur.execute("SELECT * FROM movies")
    return self.cur.fetchall()

  def get_movie(self, id):
    self.cur.execute('SELECT * FROM movies WHERE id=?', id)
    return self.cur.fetchone()
  
  def update_movie(self, id, movie_json):
    self.cursor.execute('''INSERT INTO movies 
      (name, description, release_year) 
      VALUES (?, ?, ?) 
      WHERE id=?''',
      (movie_json['name'], 
       movie_json['description'], 
       movie_json['release_year'], 
       id))

    self.connection.commit()
  
  def delete_movie(self, id):
    self.cursor.execute('DELETE FROM movies WHERE id = ?', id)
    self.connection.commit()

  def close(self):
    self.cursor.close()
    self.connection.close()