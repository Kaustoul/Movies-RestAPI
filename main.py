from flask import Flask, request
from db import Database

class Movie:
  def __init__(self, name, description, release_year):
    self.name = name
    self.description = description
    self.release_year = release_year

  def __repr__(self):
    return f'{self.name} ({self.releae_year} - {self.description})'
  
db = Database('movies.db')
db.connect()
db.create_table()

app = Flask(__name__)

@app.route('/')
def hello():
  return 'Hello world!'


@app.route('/movies', methods=['POST'])
def hello():
  return {}

if __name__ == '__main__':
  app.run()