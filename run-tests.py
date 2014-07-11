import os, unittest, json
import hmc, api_module
from flask import jsonify

class HmcTestCase(unittest.TestCase):
    def setUp(self):
        hmc.app.config.from_object('config.Testing')
        self.app = hmc.app.test_client()
        self.app.get('/api/create_db')
        self.app.get('/api/rescan')

    def tearDown(self):
        pass;

    def test_api_movies(self):
        response = self.app.get('/api/movies')
        assert response.status_code, 200
        expected_result = json.loads(response.data)
        print(response.data)
        assert len(expected_result), 3

if __name__ == '__main__':
    unittest.main()
