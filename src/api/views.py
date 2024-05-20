import requests
import hashlib
import time
import socket
import environ
import json
from pathlib import Path
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from apps.City.models import City
from apps.Country.models import Country
from apps.CostOfLivingData.models import CostOfLivingData
from apps.FlightData.models import FlightData
from apps.HotelData.models import HotelData
from django.contrib.auth.decorators import login_required
from .serializers import CitySerializer, CountrySerializer, CostOfLivingDataSerializer, SearchFlightDetailSerializer, SearchTravelDataQuerySerializer, FlightDataSerializer, HotelDataSerializer, UserSerializer, SearchHotelDetailSerializer, SearchHotelDataQuerySerializer
from forex_python.converter import CurrencyRates

ENV_PATH = Path(__file__).resolve().parent.parent / '.env'
env = environ.Env()
env.read_env(ENV_PATH)
TRAVELPAYOUTS_API_KEY = env('TRAVELPAYOUTS_API_KEY')
TRAVELPAYOUTS_API_MARKER = env("TRAVELPAYOUTS_API_MARKER")
RAPID_API_KEY = env('RAPID_API_KEY')
RAPID_API_BOOKING_KEY= env('RAPID_API_BOOKING_KEY')
RAPID_API_HOST = env('RAPID_API_HOST')
SEARCH_FLIGHTS_API_URL = "http://api.travelpayouts.com/v1/flight_search"
SEARCH_FLIGHTS_DETAILS_API_URL = "http://api.travelpayouts.com/v1/flight_search_results"
SEARCH_HOTELS_API_URL = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchHotels"
SEARCH_HOTELDETAIL_API_URL = "https://booking-com15.p.rapidapi.com/api/v1/hotels/getHotelDetails"
SEARCH_HOTELS_DESTINATION_API_URL = 'https://booking-com15.p.rapidapi.com/api/v1/hotels/searchDestination'


class CityList(APIView):
    def get(self, request, format=None):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)

class CitiesOfCountry(APIView):
    def get(self, request, pk, format=None):
        cities = City.objects.filter(country_id=pk)
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)

class CityDetail(APIView):
    def get_object(self, pk):
        try:
            return City.objects.get(pk=pk)
        except City.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        city = self.get_object(pk)
        serializer = CitySerializer(city)
        return Response(serializer.data)

class CountryList(APIView):
    def get(self, request, format=None):
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data)

class CountryDetail(APIView):
    def get_object(self, pk):
        try:
            return Country.objects.get(pk=pk)
        except Country.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        country = self.get_object(pk)
        serializer = CountrySerializer(country)
        return Response(serializer.data)

class CostOfLivingOfCityList(APIView):
    def get(self, request, pk, format=None):
        costOfLivingData = CostOfLivingData.objects.filter(city = pk)
        #costOfLivingData = CostOfLivingData.objects.filter(city__name=city)
        serializer = CostOfLivingDataSerializer(costOfLivingData, many=True)
        return Response(serializer.data)

class CostOfLivingList(APIView):
    def get(self, request, format=None):
        costOfLivingData = CostOfLivingData.objects.all()
        serializer = CostOfLivingDataSerializer(costOfLivingData, many=True)
        return Response(serializer.data)

class CostOfLivingDetail(APIView):
    def get_object(self, pk):
        try:
            return CostOfLivingData.objects.get(pk=pk)
        except CostOfLivingData.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        costOfLivingData = self.get_object(pk)
        serializer = CostOfLivingDataSerializer(costOfLivingData)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        costOfLivingData = self.get_object(pk)
        serializer = CostOfLivingDataSerializer(costOfLivingData, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, pk, format=None):
        costOfLivingData = self.get_object(pk)
        costOfLivingData.delete()
        return Response(status=204)

    def post(self, request, format=None):
        serializer = CostOfLivingDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    

class SearchAccomodations(APIView):
    def get(self, request, city, format=None):
        pass

class SearchFlights(APIView):
    
    def create_signature(self, currency_code, host, locale, adults, date, destination, origin, trip_class, ip):
        return hashlib.md5(f'{TRAVELPAYOUTS_API_KEY}:{host}:{locale}:{TRAVELPAYOUTS_API_MARKER}:{adults}:0:0:{date}:{destination}:{origin}:{trip_class}:{ip}'.encode('utf-8')).hexdigest()

    def get_search_id(self, data):
        ip = socket.gethostbyname(socket.gethostname())
        currency_code = "EUR"
        host = 'wildcats'
        locale = 'en'
        adults = data["adults"]
        date = data["startDate"]
        destination = data["to_iata"]
        origin = data["from_iata"]
        trip_class = 'Y'
        signature = self.create_signature(currency_code, host, locale, adults, date, destination, origin, trip_class, ip)
        HEADERS = {
            'Content-Type': 'application/json',
        }


        BODY = {
            'signature': signature,
            'marker': TRAVELPAYOUTS_API_MARKER,
            'host': host,
            'user_ip': ip,
            'locale': locale,
            'trip_class': trip_class,
            'passengers': {
                'adults': adults,
                'infants': 0,
                'children': 0
            },
            'segments': [{
                'origin': origin,
                'destination': destination,
                'date': date
            }],

        }

        try:
            response = requests.post(SEARCH_FLIGHTS_API_URL, headers=HEADERS, data=json.dumps(BODY))
            response.raise_for_status()  # Raise an exception for non-200 status codes

            # Try to parse JSON
            data = response.json()
            return data.get('search_id')
            
        
        except requests.exceptions.RequestException as e:
            print("Request error:", e)

        except json.decoder.JSONDecodeError as e:
            print("JSON decode error:", e)

    def formatResponse(self, data):
        currencies = [] 
        with open('/app/Scripts/currencies.json', 'r', encoding='utf-8') as file:
            currencies = json.load(file)
        response = {
            'search_id': data[0]['search_id'],
            'proposals': [] 
        }
        for item in data:
            for proposal in item['proposals']:
                airline = proposal['carriers'][0]
                stops = len(proposal['stops_airports']) - 1
                airport_stops = proposal['stops_airports']
                terms = proposal['terms']
                local_start_time = proposal['segment'][0]['flight'][0]['departure_time']
                local_end_time = proposal['segment'][len(proposal['segment']) - 1]['flight'][len(proposal['segment'][len(proposal['segment']) - 1]['flight']) - 1]['arrival_time']
                departure_date = proposal['segment'][0]['flight'][0]['departure_date']
                arrival_date = proposal['segment'][len(proposal['segment']) - 1]['flight'][len(proposal['segment'][len(proposal['segment']) - 1]['flight']) - 1]['arrival_date']
                origin_airport = proposal['segments_airports'][0][0]
                destination_airport = proposal['segments_airports'][len(proposal['segments_airports']) - 1][1]
                
                if terms:
                    first_key = next(iter(terms))  # Get the first key in the terms dictionary
                    url = terms[first_key].get('url', None)  # Safely get the URL, defaults to None if not found
                    currency = terms[first_key].get('currency', None)
                    price = terms[first_key].get('price', None)
                    if currency and currency != 'eur':
                        try:
                            exchange_rate = currencies[currency]['inverseRate']
                            price = price * exchange_rate
                            price = round(price, 2)
                        except Exception as e:
                            print(f"Error converting currency: {e}")
                            # Handle conversion error (e.g., set price to None or keep as is)


                    proposal_data = {
                        'airline': airline,
                        'no_stops': stops,
                        'url': url,
                        'currency': currency,
                        'price': price,
                        'local_start_time': local_start_time,
                        'local_end_time': local_end_time,
                        'stops_airports': airport_stops,
                        'origin_airport': origin_airport,
                        'destination_airport': destination_airport,
                        'departure_date': departure_date,
                        'arrival_date': arrival_date
                    }

                    response['proposals'].append(proposal_data)
        
        return response

    def post(self, request):
        serializer = SearchTravelDataQuerySerializer(data=request.data)
        
        if serializer.is_valid():
            
            search_id = self.get_search_id(serializer.data)

            HEADERS = {
                'Accept-Encoding': 'gzip,deflate,sdch'
            }

            params = {
                'uuid': search_id
            }

            MAX_RETRIES = 5  
            retries = 0

            while retries < MAX_RETRIES:
                try:
                    response = requests.get(SEARCH_FLIGHTS_DETAILS_API_URL, headers=HEADERS, params=params)
                    response.raise_for_status()

                    data = response.json()

                    # Check if any item has an empty 'proposals' array
                    if all(len(item.get('proposals', [])) > 0 for item in data):
                        return Response(self.formatResponse(data))
                    else:
                        retries += 1

                except requests.exceptions.RequestException as e:
                    print("Request error:", e)
                    return Response({'error': str(e)}, status=500)

                if retries >= MAX_RETRIES:
                    return Response({'error': 'Max retries reached, no suitable data found'}, status=500)
                
        
        else:
            return Response(serializer.errors, status=400)

class SearchFlightDetail(APIView):
    def get_search_url(self, search_id, url):
        base_url = "http://api.travelpayouts.com/v1/flight_searches/{}/clicks/{}.json?marker={}"
        return base_url.format(search_id, url, TRAVELPAYOUTS_API_MARKER)
    
    def post(self, request):
        
        data = request.data
        
        serializer = SearchFlightDetailSerializer(data=data)

        if serializer.is_valid():
            url = self.get_search_url(serializer.data['search_id'], serializer.data['url'])
            print(url)
            response = requests.get(url)

            result = response.json().get('url', None)

            if result is None:
                return Response({'error': 'No URL found'}, status=500)
            else:
                return Response({'url': result})

            MAX_RETRIES = 5
        return Response(serializer.errors, status=400)

class FlightList(APIView):
    def get(self, request, format=None):
        flights = FlightData.objects.all()
        serializer = FlightDataSerializer(flights, many=True)
        return Response(serializer.data)
    
class FlightDetail(APIView):
    def get_object(self, pk):
        try:
            return FlightData.objects.get(pk=pk)
        except FlightData.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        flights = FlightData.objects.filter(pk=pk)
        serializer = FlightDataSerializer(flights, many=True)
        return Response(serializer.data)
    
class FlightByOrigin(APIView):
    def get(self, request, origin, format=None):
        flights = FlightData.objects.filter(origin=origin)
        serializer = FlightDataSerializer(flights, many=True)
        return Response(serializer.data)

class FlightByDestination(APIView):
    def get(self, request, destination, format=None):
        flights = FlightData.objects.filter(destination=destination)
        serializer = FlightDataSerializer(flights, many=True)
        return Response(serializer.data)

class HotelList(APIView):
    def get(self, request, format=None):
        hotels = HotelData.objects.all()
        serializer = HotelDataSerializer(hotels, many=True)
        return Response(serializer.data)

class HotelDetail(APIView):
    def get_object(self, pk):
        try:
            return HotelData.objects.get(pk=pk)
        except HotelData.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        hotels = HotelData.objects.filter(pk=pk)
        serializer = HotelDataSerializer(hotels, many=True)
        return Response(serializer.data)
    
def user_data(request):
    """
    View to return user data if authenticated, else return an
    'unauthenticated' response.
    """
    if request.user.is_authenticated:
        user = request.user
        serializer = UserSerializer(user)
        return JsonResponse({'isAuthenticated': True, 'user': serializer.data})
    else:
        return JsonResponse({'isAuthenticated': False, 'user': None}, status=401)
    
class SearchHotels(APIView):
    def getSearchID(self, data):
        HEADERS = {
            'X-RapidAPI-Key': RAPID_API_BOOKING_KEY,
            'X-RapidAPI-Host': 'booking-com15.p.rapidapi.com'
        }

        querystring = {"query":data['city_iata']}

        try:
            response = requests.request("GET", SEARCH_HOTELS_DESTINATION_API_URL, headers=HEADERS, params=querystring)
            response.raise_for_status()  # Raise an exception for non-200 status codes

            # Try to parse JSON
            # get the data array from the json response
            # print (response.json())
            data = response.json().get('data')

            for item in data:
                if item.get('search_type') == 'city':
                    return {
                        'dest_id': item.get('dest_id'),
                        'dest_type': item.get('dest_type'),
                    }
                
            return None
        except requests.exceptions.RequestException as e:
            print("Request error:", e)

    def post(self, request):
        data = request.data
        
        serializer = SearchHotelDataQuerySerializer(data=data)


        if serializer.is_valid():
            searchParams = self.getSearchID(serializer.data)
            if searchParams is None:
                return Response({'error': 'No search params found'}, status=500)
            
            HEADERS = {
                'X-RapidAPI-Key': RAPID_API_BOOKING_KEY,
                'X-RapidAPI-Host': 'booking-com15.p.rapidapi.com'
            }

            query = {
                "arrival_date": serializer.data['arrival_date'],
                "departure_date": serializer.data['departure_date'],
                'search_type': 'city',
                "adults": serializer.data['adults'],
                "dest_id": searchParams['dest_id'],
                "currency_code": "EUR"
            }

            response = requests.request("GET", SEARCH_HOTELS_API_URL, headers=HEADERS, params=query)
            
            return Response(response.json())
        else:
            return Response(serializer.errors, status=400)
        
class SearchHotelDetail(APIView):
    def post(self, request):
        data = request.data
        
        serializer = SearchHotelDetailSerializer(data=data)

        if serializer.is_valid():

            HEADERS = {
                'X-RapidAPI-Key': RAPID_API_BOOKING_KEY,
                'X-RapidAPI-Host': 'booking-com15.p.rapidapi.com'
            }
            
            query = {
                "hotel_id":serializer.data['hotel_id'],
                "arrival_date":serializer.data['arrival_date'],
                "departure_date":serializer.data['departure_date'],
                "adults":serializer.data['adults'],
                "currency_code":"EUR"
            }

            response = requests.request("GET", SEARCH_HOTELDETAIL_API_URL, headers=HEADERS, params=query)
            
            return Response(response.json())
        else:
            return Response(serializer.errors, status=400)
