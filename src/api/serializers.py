from rest_framework import serializers
from apps.City.models import City
from apps.Country.models import Country
from apps.CostOfLivingData.models import CostOfLivingData
from apps.FlightData.models import FlightData
from apps.HotelData.models import HotelData
from django.contrib.auth.models import User, Group
from accounts.models import UserProfile

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class CostOfLivingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostOfLivingData
        fields = '__all__'
    
class FlightDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightData
        fields = '__all__'
        
class HotelDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelData
        fields = '__all__'

class SearchTravelDataQuerySerializer(serializers.Serializer):
    to_id = serializers.IntegerField(required=True)
    from_id = serializers.IntegerField(required=True)
    startDate = serializers.DateField(required=True)
    endDate = serializers.DateField(required=False)
    maxPrice = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    directOnly = serializers.BooleanField(required=True)
    maxStops = serializers.IntegerField(required=False)
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['is_premium']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    groups = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'profile', 'groups' ]