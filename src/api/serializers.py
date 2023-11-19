from rest_framework.serializers import ModelSerializer
from City.models import City
from Country.models import Country
from CostOfLivingData.models import CostOfLivingData

class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class CostOfLivingDataSerializer(ModelSerializer):
    class Meta:
        model = CostOfLivingData
        fields = '__all__'