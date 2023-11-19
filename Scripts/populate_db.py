import logging
import os
import mysql.connector
import random
import environ

env = environ.Env()
env_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
env.read_env(env_file_path)

# Database configuration

config = {
    'user': env('MYSQL_USER'),
    'password': env('MYSQL_PASSWORD'),
    'host': 'db',
    'port': env('MYSQL_PORT'),
    'database': env('MYSQL_DATABASE')
}

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
        countries = [('Germany', 'DEU'), ('France', 'FRA'), ('Italy', 'ITA'), ('Spain', 'ESP'), ('Romania', 'ROU')]
        for country_name, country_code in countries:
            cursor.execute("INSERT INTO Country_country (name, code) VALUES (%s, %s)", (country_name, country_code))

        cnx.commit()

        # Insert cities and cost of living data
        cities = [
            ('Berlin', 1), ('Munich', 1), ('Frankfurt', 1),
            ('Paris', 2), ('Lyon', 2), ('Marseille', 2),
            ('Rome', 3), ('Milan', 3), ('Naples', 3),
            ('Madrid', 4), ('Barcelona', 4), ('Valencia', 4),
            ('Bucharest', 5), ('Cluj-Napoca', 5), ('Timișoara', 5)
        ]

        for city, country_id in cities:
            cursor.execute("INSERT INTO City_city (name, country_id, latitude, longitude) VALUES (%s, %s, %s, %s)", (city, country_id, 0, 0))

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
