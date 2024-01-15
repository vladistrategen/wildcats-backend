import json
import logging
import os

import requests
import mysql.connector
import random
import environ

env = environ.Env()
env_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
env.read_env(env_file_path)

COUNTRIES_BASE_URL = 'https://restcountries.com/v3.1/all'
CITIES_BASE_URL = 'https://api.travelpayouts.com/data/ru/cities.json'
# Database configuration

config = {
    'user': env('MYSQL_USER'),
    'password': env('MYSQL_PASSWORD'),
    'host': 'db',
    'port': env('MYSQL_PORT'),
    'database': env('MYSQL_DATABASE')
}

def getCountries():
    countries = requests.get(COUNTRIES_BASE_URL).json()
    formatted_countries = []

    # First, load all cities from cities.json
    with open('/app/Scripts/cities.json', 'r', encoding='utf-8') as file:
        cities = json.load(file)

    if countries:
        for country in countries:
            if country['region'] == 'Europe':
                # Filter cities for the current country
                country_cities = [
                    {
                        'name': city['name'],
                        'code': city['code'],
                        'latitude': city['latitude'],
                        'longitude': city['longitude']
                    }
                    for city in cities
                    if city['country_code'] == country['cca2']
                ]
                formatted_country = {
                    'name': country['name']['common'],
                    'code': country['cca3'],
                    'cities': country_cities
                }
                formatted_countries.append(formatted_country)

    return formatted_countries


def main():
    # Connect to the database
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # Function to check if a table is empty
    def is_table_empty(table_name):
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        return count == 0

    # Insert countries, cities, and cost of living data if tables are empty
    if is_table_empty('Country_country') and is_table_empty('City_city') and is_table_empty('CostOfLivingData_costoflivingdata'):
        # Insert countries
        countries = getCountries()
        current_country_id = 0
        no_cities = 0
        for country in countries:
            country_name = country["name"]
            country_code = country["code"]
            cursor.execute("INSERT INTO Country_country (name, code) VALUES (%s, %s)", (country_name, country_code))
            current_country_id += 1
            for city in country["cities"]:
                city_name = city["name"]
                city_code = city["code"]
                city_latitude = city["latitude"]
                city_longitude = city["longitude"]
                try:
                    cursor.execute("INSERT INTO City_city (name, country_id, latitude, longitude, main_iata_code) VALUES (%s, %s, %s, %s, %s)", (city_name, current_country_id, city_latitude, city_longitude, city_code))
                except mysql.connector.errors.IntegrityError as e:
                    logging.error(f"Error inserting data: {e}")
                no_cities += 1

        cnx.commit()

        # Fetch city IDs
        cursor.execute("SELECT id FROM City_city")
        city_ids = [city_id[0] for city_id in cursor.fetchall()]

        items = ['Rent', 'Restaurant', 'Groceries', 'Taxi', 'Internet', 'Phone', 'Gas', 'Car', 'Public Transport', 'Cinema', 'Theatre', 'Fitness Club', 'Salon', 'Clothes', 'Shoes', 'Childcare']
        # Insert random cost of living items for each city
        for city_id in city_ids:
            for _ in range(5):
                item = random.choice(items)
                price = round(random.uniform(10, 1000), 2)
                try:
                    cursor.execute("INSERT INTO CostOfLivingData_costoflivingdata (city_id, item, price, date) VALUES (%s, %s, %s, %s)", (city_id, item, price, '2023-01-01'))
                except mysql.connector.errors.IntegrityError as e:
                    logging.error(f"Error inserting data: {e}")

        cnx.commit()

    # Close the connection
    cursor.close()
    cnx.close()

if __name__ == "__main__":
    main()
