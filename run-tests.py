import os, unittest, json, sqlite3
from flask import Flask, jsonify, current_app
import hmc, api_module
from services import MovieManager
from db import execute_sql, upgrade_db, get_db_version, create_db

flask_app = Flask(__name__)
flask_app.config.from_object('config.Testing')

class HmcTestCase(unittest.TestCase):
    MOVIES_FILE_COUNT = 4
    
    def setUp(self):
        hmc.app.config.from_object('config.Testing')
        self.app = hmc.app.test_client()
        current_app = self.app

    def tearDown(self):
        pass;

    def test_create_db(self):
        with flask_app.test_request_context():
            create_db()
            print('OK - test_create_db')

    def test_rescan_movies(self):
        with flask_app.test_request_context():
            movies_path = current_app.config['MOVIES_PATH']
            movie_file_exts = current_app.config['DEFAULT_MOVIE_FILE_EXTENSIONS']
            movie_share_path = current_app.config['MOVIE_SHARE_PATH']
            result = MovieManager().rescan(movies_path, movie_share_path, movie_file_exts, True, True)
            assert result == self.MOVIES_FILE_COUNT

    def test_api_movies(self):
        response = self.app.get('/api/movies')
        assert response.status_code, 200
        actual_result = json.loads(response.data)
        assert len(actual_result['result']) == self.MOVIES_FILE_COUNT
        print('OK - test_api_movies')

    def test_remove_all_missing_files_in_db(self):
        with flask_app.test_request_context():
            movieManager = MovieManager()
            expected_count = 22
            for i in range(expected_count):
                execute_sql('insert into movies(file_name, name) values(?, ?)', ['.filenotfound' + str(i), 'test' + str(i)])
            actual_count = movieManager.remove_all_missing_files_in_db()
            assert actual_count == expected_count, 'actual: {0}, expected: {1}'.format(actual_count, expected_count)
            print('OK - test_remove_all_missing_files_in_db')

    def test_get_db_version(self):
        with flask_app.test_request_context():
            actual_result = get_db_version()
            assert actual_result >= 0
            print('OK - test_get_db_version')

    def test_upgrade_db(self):
        with flask_app.test_request_context():
            current_version = get_db_version()
            actual_version = upgrade_db()
            assert actual_version >= current_version

if __name__ == '__main__':
    unittest.main()
