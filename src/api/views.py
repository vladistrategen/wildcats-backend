from django.http import Http404
from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from City.models import City
from Country.models import Country
from CostOfLivingData.models import CostOfLivingData

from .serializers import CitySerializer, CountrySerializer, CostOfLivingDataSerializer

class CityList(APIView):
    def get(self, request, format=None):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)

class CitiesOfCountry(APIView):
    def get(self, request, country, format=None):
        cities = City.objects.filter(country=country)
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
    def get(self, request, city, format=None):
        costOfLivingData = CostOfLivingData.objects.filter(city__name=city)
        serializer = CostOfLivingDataSerializer(costOfLivingData, many=True)
        return Response(serializer.data)

class CostOfLivingList(APIView):
    def get(self, request, format=None):
        costOfLivingData = CostOfLivingData.objects.all()
        serializer = CostOfLivingDataSerializer(costOfLivingData, many=True)
        return Response(serializer.data)

class CostOfLivingOfCityDetail(APIView):
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
    

