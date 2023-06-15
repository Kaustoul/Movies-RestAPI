from flask import Flask
from flask.testing import FlaskClient
import unittest

from main import app, setup_db, clear_db

test_data1 = {
  "title": "Test1",
  "description": "Testing example",
  "release_year": 2020
}

test_data2 = {
  "title": "Test2",
  "release_year": 2021
}

result_data2 = test_data2
result_data2['description'] = None

test_data3 = {
  "title": "Test3",
  "description": "Update test",
  "release_year": 2022
}

test_data4 = {
  "title": "Test4",
  "release_year": 2023
}

result_data4 = test_data4
result_data4['description'] = None


class FlaskApiTestCase(unittest.TestCase):
  def setUp(self):
    # Create a test client
    setup_db("test.db")
    clear_db()
    self.app = app.test_client()
  
  def test_get_empty(self):
    response = self.app.get('/movies')
    
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json, [])
  
  def test_post(self):
    # Basic POST test
    response = self.app.post('/movies', json=test_data1)
    
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json['title'], "Test1")
    self.assertEqual(response.json['description'], "Testing example")
    self.assertEqual(response.json['release_year'], 2020)
    self.assertEqual(response.json['id'], 1)

    # No description test
    response = self.app.post('/movies', json=test_data2)
    
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json['title'], "Test2")
    self.assertIsNone(response.json['description'])
    self.assertEqual(response.json['release_year'], 2021)
    self.assertEqual(response.json['id'], 2)

    # No title test
    data = {"release_year": 2021}
    response = self.app.post('/movies', json=data)
    
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.json['message'], "Invalid request params")

    # No release_year test
    data = {"title": "Test3"}
    response = self.app.post('/movies', json=data)
    
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.json['message'], "Invalid request params")

    # Invalid release_year format
    data = {
      "title": "Test3", 
      "release_year": 20211
    }
    response = self.app.post('/movies', json=data)
    
    self.assertEqual(response.status_code, 400)
    self.assertEqual(response.json['message'], "'release_year' must be a 4 digit number")

  def test_get_all(self):
    self.app.post('/movies', json=test_data1)
    self.app.post('/movies', json=test_data2)

    test_data1['id'] = 1
    result_data2['id'] = 2

    response = self.app.get('/movies')

    self.assertEqual(response.status_code, 200)
    # self.assertEqual(response.json[0], test_data1)
    # self.assertEqual(response.json[1], result_data2)
    # self.assertEqual(len(response.json), 2)
    self.assertListEqual(response.json, [test_data1, result_data2])
  
  def test_get_id(self):
    self.app.post('/movies', json=test_data1)
    self.app.post('/movies', json=test_data2)

    response = self.app.get('/movies/1')
    
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json, test_data1)

    response = self.app.get('/movies/2')
    
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json, result_data2)


    response = self.app.get('/movies/3')
    
    self.assertEqual(response.status_code, 404)

  def test_put(self):    
    self.app.post('/movies', json=test_data1)
    self.app.post('/movies', json=test_data2)

    response = self.app.put('/movies/2', json=test_data3)

    test_data3['id'] = 2
    
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json, test_data3)
  
    response = self.app.put('/movies/2', json=test_data4)

    test_data4['id'] = 2
    
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json, result_data4)

    response = self.app.put('/movies/3', json=test_data3)
    self.assertEqual(response.status_code, 404)

    data = {
      "title": "Test5"
    }
    response = self.app.put('/movies/3', json=data)
    self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
