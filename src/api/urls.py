from django.urls import path
from .views import (
    CityList, CitiesOfCountry, CityDetail, 
    CountryList, CountryDetail, 
    CostOfLivingOfCityList, CostOfLivingOfCityDetail,
    CostOfLivingList
)

urlpatterns = [
    path('cities/', CityList.as_view(), name='city-list'),
    path('cities/<int:pk>/', CityDetail.as_view(), name='city-detail'),
    path('cities/country/<str:country>/', CitiesOfCountry.as_view(), name='cities-of-country'),
    path('countries/', CountryList.as_view(), name='country-list'),
    path('countries/<int:pk>/', CountryDetail.as_view(), name='country-detail'),
    path('cost-of-living/', CostOfLivingList.as_view(), name='cost-of-living-list'),
    path('cost-of-living/city/<str:city>/', CostOfLivingOfCityList.as_view(), name='cost-of-living-city-list'),
    path('cost-of-living/<int:pk>/', CostOfLivingOfCityDetail.as_view(), name='cost-of-living-detail'),
]
