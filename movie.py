class Movie:
  def __init__(self, title, release_year, description = None, id = -1):
    self.id = id
    self.title = title
    self.description = description
    self.release_year = release_year

  def jsonify(self):
    """Json representation of the movie"""
    return {'id': self.id, 'title': self.title, 'description': self.description, 'release_year': self.release_year}

  def __repr__(self):
    return f'{self.id}:{self.title} ({self.release_year}) - {self.description}'
  
  @staticmethod
  def from_json(json):
    """Loads a movie from json representation"""
    if json.get('title') is None or json.get('release_year') is None:
      return None
    
    desc = None
    if json.get('description') is not None:
      desc = json['description']
    
    return Movie(title=json['title'], description=desc, release_year=json['release_year'])