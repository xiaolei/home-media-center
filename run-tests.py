import os, unittest, json
from flask import Flask, jsonify
import hmc, api_module
from services import MovieManager
from db import execute_sql, upgrade_db, get_db_version

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

    def test_get_db_version(self):
        with flask_app.test_request_context():
            actual_result = get_db_version()
            assert actual_result >= 0, True
            print('OK - test_get_db_version')

    def test_upgrade_db(self):
        with flask_app.test_request_context():
            current_version = get_db_version()
            actual_version = upgrade_db()
            assert actual_version >= current_version, True

if __name__ == '__main__':
    unittest.main()
