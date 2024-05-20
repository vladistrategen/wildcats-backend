from django.test import TestCase
from apps import City
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch, Mock
import requests
from apps.City.models import City
from api.serializers import SearchHotelDataQuerySerializer

class SearchHotelsTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('search-hotels')
        self.valid_payload = {
            "adults": 2,
            "arrival_date": "2024-06-01",
            "departure_date": "2024-06-07",
            "city_iata": "NYC"
        }
        self.invalid_payload = {
            "adults": 2,
            "arrival_date": "",
            "departure_date": "",
            "city_iata": ""
        }

    @patch('api.views.requests.get')
    def test_search_hotels_success(self, mock_get):
        # Mocking the destination API response
        mock_dest_response = Mock()
        mock_dest_response.status_code = 200
        mock_dest_response.json.return_value = {
            'data': [
                {
                    'search_type': 'city',
                    'dest_id': 'test-dest-id',
                    'dest_type': 'test-dest-type'
                }
            ]
        }
        mock_get.side_effect = [mock_dest_response, Mock(status_code=200, json=lambda: {'hotels': ['hotel1', 'hotel2']})]

        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('hotels', response.data['data'])
        self.assertGreater(len(response.data['data']['hotels']), 0)

    def test_search_hotels_invalid_payload(self):
        response = self.client.post(self.url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('arrival_date', response.data)
        self.assertIn('departure_date', response.data)
        self.assertIn('city_iata', response.data)
        self.assertEqual(response.data['arrival_date'][0].code, 'invalid')
        self.assertEqual(response.data['departure_date'][0].code, 'invalid')
        self.assertEqual(response.data['city_iata'][0].code, 'blank')

    @patch('api.views.requests.get')
    def test_search_hotels_no_search_params(self, mock_get):
        mock_dest_response = Mock()
        mock_dest_response.status_code = 200
        mock_dest_response.json.return_value = {
            'data': []
        }
        mock_get.return_value = mock_dest_response

        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.data)


class SearchFlightsTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('search')
        self.valid_payload = {
            "adults": 1,
            "startDate": "2024-06-01",
            "to_iata": "JFK",
            "from_iata": "LAX"
        }
        self.invalid_payload = {
            "adults": 1,
            "startDate": "",
            "to_iata": "",
            "from_iata": ""
        }

    @patch('api.views.requests.post')
    @patch('api.views.requests.get')
    def test_search_flights_success(self, mock_get, mock_post):
        mock_post_response = Mock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {'search_id': 'test-search-id'}
        mock_post.return_value = mock_post_response

        mock_get_response = Mock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = [{
            'search_id': 'test-search-id',
            'proposals': [
                {
                    'carriers': ['AA'],
                    'stops_airports': ['LAX', 'JFK'],
                    'terms': {
                        'test_term': {
                            'url': 'http://example.com',
                            'currency': 'usd',
                            'price': 100
                        }
                    },
                    'segment': [
                        {
                            'flight': [
                                {
                                    'departure_time': '10:00',
                                    'departure_date': '2024-06-01'
                                },
                                {
                                    'arrival_time': '18:00',
                                    'arrival_date': '2024-06-01'
                                }
                            ]
                        }
                    ],
                    'segments_airports': [
                        ['LAX', 'JFK']
                    ]
                }
            ]
        }]
        mock_get.return_value = mock_get_response

        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('proposals', response.data)
        self.assertGreater(len(response.data['proposals']), 0)
        print(response.data)

    def test_search_flights_invalid_payload(self):
        response = self.client.post(self.url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('to_iata', response.data)
        self.assertIn('from_iata', response.data)
        self.assertIn('startDate', response.data)
        self.assertEqual(response.data['to_iata'][0].code, 'blank')
        self.assertEqual(response.data['from_iata'][0].code, 'blank')
        self.assertEqual(response.data['startDate'][0].code, 'invalid')


    @patch('api.views.requests.post')
    @patch('api.views.requests.get')
    def test_search_flights_no_proposals(self, mock_get, mock_post):
        mock_post_response = Mock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {'search_id': 'test-search-id'}
        mock_post.return_value = mock_post_response

        mock_get_response = Mock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = [{
            'search_id': 'test-search-id',
            'proposals': []
        }]
        mock_get.return_value = mock_get_response

        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.data)

