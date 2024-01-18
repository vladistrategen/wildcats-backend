import requests
import environ
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
from .serializers import CitySerializer, CountrySerializer, CostOfLivingDataSerializer, SearchTravelDataQuerySerializer, FlightDataSerializer, HotelDataSerializer, UserSerializer
from django.contrib.auth.decorators import login_required

ENV_PATH = Path(__file__).resolve().parent.parent / '.env'
env = environ.Env()
env.read_env(ENV_PATH)
TRAVELPAYOUTS_API_KEY = env('TRAVELPAYOUTS_API_KEY')
RAPID_API_KEY = env('RAPID_API_KEY')
RAPID_API_HOST = env('RAPID_API_HOST')
TRAVELPAYOUTS_API_URL = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"


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
    def post(self, request):
        # Get data from the request body
        data = request.data

        # Initialize the serializer with the request data
        serializer = SearchTravelDataQuerySerializer(data=data)
        print(serializer.is_valid())
        # Validate the data
        if serializer.is_valid():
            HEADERS = {
                'X-Access-Token': TRAVELPAYOUTS_API_KEY,
                'Content-Type': 'application/json'
            }
            query ={
                "currency": "eur",
                "destination": serializer.data['to_iata'],
                "origin": serializer.data['from_iata'],
            }
            response = requests.request("GET", TRAVELPAYOUTS_API_URL, headers=HEADERS, params=query)
            return Response(response.json())
        else:
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