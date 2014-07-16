import os, unittest, json
from flask import Flask, jsonify
import hmc, api_module
from services import MovieManager
from db import execute_sql

flask_app = Flask(__name__)
flask_app.config.from_object('config.Testing')

class HmcTestCase(unittest.TestCase):
    def setUp(self):
        hmc.app.config.from_object('config.Testing')
        self.app = hmc.app.test_client()
        self.app.get('/api/create_db')
        self.app.get('/api/rescan')
        current_app = self.app
        print('OK - setUp')

    def tearDown(self):
        pass;

    def test_api_movies(self):
        response = self.app.get('/api/movies')
        assert response.status_code, 200
        expected_result = json.loads(response.data)
        assert len(expected_result), 3
        print('OK - test_api_movies')

    def test_remove_all_missing_files_in_db(self):
        with flask_app.test_request_context():
            movieManager = MovieManager()
            expected_count = 22
            for i in range(expected_count):
                execute_sql('insert into movies(file_name, name) values(?, ?)', ['.filenotfound' + str(i), 'test' + str(i)])
            actual_count = movieManager.remove_all_missing_files_in_db()
            assert actual_count, expected_count
            print('OK - remove_all_missing_files_in_db')

if __name__ == '__main__':
    unittest.main()
