from flask import Flask, request, jsonify
from db import Database
from movie import Movie

# Setup flask
app = Flask(__name__)
db = None


def setup_db(name):
  global db
  db = Database(name)
  db.connect()
  db.create_table()

def clear_db():
  db.cur.execute("DELETE FROM movies")
  db.con.commit()

@app.route('/')
def hello():
  return 'Hello world!'

@app.route('/movies', methods=['GET'])
def fetch_all_movies():
  result = db.get_all_movies()
  movies = [Movie(id=movie[0], title=movie[1], description=movie[2], release_year=movie[3]).jsonify() for movie in result]
  return movies, 200

@app.route('/movies/<int:id>', methods=['GET'])
def fetch_movie(id):
  result = db.get_movie(id)
  if result is None:
    return {"message": "Invalid movie ID"}, 404
  
  movie = Movie(id = result[0], title=result[1], description=result[2], release_year=result[3])
  return movie.jsonify(), 200

@app.route('/movies', methods=['POST'])
def create_movie():
  movie = Movie.from_json(request.get_json())
  if not movie:
    return {"message": "Invalid request params"}, 400
  
  result = db.insert_movie(movie)
  if result == -2:
    return {"message": "'release_year' must be a 4 digit number"}, 400
  elif result == -1:
    return {"message": "Failed to create a new entry in database."}, 500
  else:
    movie.id = result
    return movie.jsonify(), 201
  
@app.route('/movies/<int:id>', methods = ['PUT'])
def update_movie(id):
  movie = Movie.from_json(request.get_json())
  if not movie:
    return {"message": "Invalid request params"}, 400
  
  movie.id = id
  result = db.update_movie(movie)

  if result == -2:
    return {"message": "'release_year' must be a 4 digit number"}, 400
  
  elif result == -1:
    {"message": "Failed to create a new entry in database."}, 500

  elif (result < 1):
    return {"message": "Invalid movie ID"}, 404
  
  return movie.jsonify(), 200

setup_db("movies.db")

if __name__ == '__main__':
  try:
    app.run()
  finally:
    db.close()