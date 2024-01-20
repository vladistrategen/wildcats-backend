from django.urls import path
from .views import (
    CityList, CitiesOfCountry, CityDetail, 
    CountryList, CountryDetail, 
    CostOfLivingOfCityList, CostOfLivingDetail,
    CostOfLivingList, SearchFlights,
    FlightList, HotelList, FlightDetail,
    HotelDetail, FlightByOrigin, FlightByDestination,
    user_data, SearchHotels, SearchHotelDetail, SearchFlightDetail
)

urlpatterns = [
    path('cities/', CityList.as_view(), name='city-list'),
    path('cities/<int:pk>/', CityDetail.as_view(), name='city-detail'),
    path('cities/country/<int:pk>/', CitiesOfCountry.as_view(), name='cities-of-country'),
    path('countries/', CountryList.as_view(), name='country-list'),
    path('countries/<int:pk>/', CountryDetail.as_view(), name='country-detail'),
    path('cost-of-living/', CostOfLivingList.as_view(), name='cost-of-living-list'),
    path('cost-of-living/city/<int:pk>/', CostOfLivingOfCityList.as_view(), name='cost-of-living-city-list'),
    path('cost-of-living/<int:pk>/', CostOfLivingDetail.as_view(), name='cost-of-living-detail'),
    path('search/flights/', SearchFlights.as_view(), name='search'),
    path('search/flights/details/', SearchFlightDetail.as_view(), name='search-flight-detail'),
    path('flights/', FlightList.as_view(), name='flight-list'),
    path('hotels/', HotelList.as_view(), name='hotel-list'),
    path('flight/<int:pk>/', FlightDetail.as_view(), name='flight-detail'),
    path('hotel/<int:pk>/', HotelDetail.as_view(), name='hotel-detail'),
    path('flights/origin/<int:pk>/', FlightByOrigin.as_view(), name='flight-by-origin'),
    path('flights/destination/<int:pk>/', FlightByDestination.as_view(), name='flight-by-destination'),
    path('user_data/', user_data, name='user_data'),
    path('search/hotels/', SearchHotels.as_view(), name='search-hotels'),
    path('search/hotels/details/', SearchHotelDetail.as_view(), name='search-hotel-detail'),

]
