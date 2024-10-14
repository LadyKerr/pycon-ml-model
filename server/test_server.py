import unittest
from server import app

class TestServer(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Let's build a flight delay prediction api!")

    def test_predict(self):
        response = self.app.get('/predict?airport_id=123&day_of_week=1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('model_prediction', data)
        self.assertIn('confidence_percent', data)
        self.assertIn('delayed_percent', data)
        self.assertIn('interpretation', data)

    def test_airports(self):
        response = self.app.get('/airports')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('airports', data)
        airports = data['airports']
        self.assertIsInstance(airports, list)
        self.assertTrue(all(isinstance(airport, dict) for airport in airports))
        self.assertTrue(all('id' in airport and 'name' in airport for airport in airports))

if __name__ == '__main__':
    unittest.main()