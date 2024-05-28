import unittest
import requests
from app import create_app

class BookingRequestTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_index(self):
        response = requests.get('http://booking.um.localhost/api/v1/booking/')
        self.assertEqual(response.status_code, 200)
    
    def test_create(self):
        response = requests.post('http://booking.um.localhost/api/v1/booking/create?user_id=1&apartment_id=1', json={
            "start_date": "2021-07-01",
            "finish_date": "2021-07-10",
            "duration": 9,
            "amount_people": 2
        })
        self.assertEqual(response.status_code, 200)

    def test_find_all(self):
        response = requests.get('http://booking.um.localhost/api/v1/booking/findall')
        self.assertEqual(response.status_code, 200)

    def test_find_by_id(self):
        response = requests.get('http://booking.um.localhost/api/v1/booking/findbyid/1')
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        response = requests.put('http://booking.um.localhost/api/v1/booking/update/1', json={
            "start_date": "2021-07-01",
            "finish_date": "2021-07-10",
            "duration": 9,
            "amount_people": 3
        })
        self.assertEqual(response.status_code, 200)
    

if __name__ == '__main__':
    unittest.main()