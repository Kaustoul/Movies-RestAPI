import sqlite3
from movie import Movie

class Database:
  def __init__(self, name):
    self.name = name
    self.con = None
    self.cur = None

  def connect(self):
    self.con = sqlite3.connect(self.name, check_same_thread=False)
    self.cur = self.con.cursor()

  def create_table(self):
    self.cur.execute('''CREATE TABLE IF NOT EXISTS movies(
      id INTEGER PRIMARY KEY NOT NULL,
      title VARCHAR(255),
      description TEXT,
      release_year INTEGER NOT NULL CHECK(length(release_year) = 4)
      )''')
    self.con.commit()
    
  def insert_movie(self, movie):
    try:
      self.cur.execute("INSERT INTO movies (title, description, release_year) VALUES (?, ?, ?)",
                          (movie.title, movie.description, movie.release_year))
      self.con.commit()
      return self.cur.lastrowid
    except Exception as e:
      print(e)
      # Check constraint on release_year failed
      if isinstance(e, sqlite3.IntegrityError) and "CHECK constraint" in str(e):
        return -2
      
      return -1

  def get_all_movies(self):
    self.cur.execute("SELECT * FROM movies")
    return self.cur.fetchall()

  def get_movie(self, id):
    self.cur.execute('SELECT * FROM movies WHERE id=?', id)
    return self.cur.fetchone()
  
  def update_movie(self, id, movie_json):
    self.cursor.execute('''INSERT INTO movies 
      (title, description, release_year) 
      VALUES (?, ?, ?) 
      WHERE id=?''',
      (movie_json['title'], 
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