-- Insert European countries including Romania
INSERT INTO Country_country (name) VALUES ('Germany');
INSERT INTO Country_country (name) VALUES ('France');
INSERT INTO Country_country (name) VALUES ('Italy');
INSERT INTO Country_country (name) VALUES ('Spain');
INSERT INTO Country_country (name) VALUES ('Romania');

-- Insert cities for each country
-- Germany
INSERT INTO City_city (name, country_id) VALUES ('Berlin', 1);
INSERT INTO City_city (name, country_id) VALUES ('Munich', 1);
INSERT INTO City_city (name, country_id) VALUES ('Frankfurt', 1);

-- France
INSERT INTO City_city (name, country_id) VALUES ('Paris', 2);
INSERT INTO City_city (name, country_id) VALUES ('Lyon', 2);
INSERT INTO City_city (name, country_id) VALUES ('Marseille', 2);

-- Italy
INSERT INTO City_city (name, country_id) VALUES ('Rome', 3);
INSERT INTO City_city (name, country_id) VALUES ('Milan', 3);
INSERT INTO City_city (name, country_id) VALUES ('Naples', 3);

-- Spain
INSERT INTO City_city (name, country_id) VALUES ('Madrid', 4);
INSERT INTO City_city (name, country_id) VALUES ('Barcelona', 4);
INSERT INTO City_city (name, country_id) VALUES ('Valencia', 4);

-- Romania
INSERT INTO City_city (name, country_id) VALUES ('Bucharest', 5);
INSERT INTO City_city (name, country_id) VALUES ('Cluj-Napoca', 5);
INSERT INTO City_city (name, country_id) VALUES ('Timisoara', 5);

-- Insert Cost of living data

-- Insert cost of living data items for each city
-- Manually for each city (example for city_id 1, repeat for each city)
INSERT INTO CostOfLivingData_costoflivingdata  (city_id, item, price, date) VALUES (1, 'Rent', 1200.00, '2023-01-01');
INSERT INTO CostOfLivingData_costoflivingdata  (city_id, item, price, date) VALUES (1, 'Utilities', 150.00, '2023-01-01');
INSERT INTO CostOfLivingData_costoflivingdata  (city_id, item, price, date) VALUES (1, 'Groceries', 300.00, '2023-01-01');
INSERT INTO CostOfLivingData_costoflivingdata  (city_id, item, price, date) VALUES (1, 'Public Transport', 70.00, '2023-01-01');
INSERT INTO CostOfLivingData_costoflivingdata  (city_id, item, price, date) VALUES (1, 'Internet', 40.00, '2023-01-01');
INSERT INTO CostOfLivingData_costoflivingdata  (city_id, item, price, date) VALUES (1, 'Gym Membership', 35.00, '2023-01-01');
INSERT INTO CostOfLivingData_costoflivingdata  (city_id, item, price, date) VALUES (1, 'Cinema Ticket', 12.00, '2023-01-01');
INSERT INTO CostOfLivingData_costoflivingdata  (city_id, item, price, date) VALUES (1, 'Coffee', 3.50, '2023-01-01');
INSERT INTO CostOfLivingData_costoflivingdata  (city_id, item, price, date) VALUES (1, 'Meal in Restaurant', 15.00, '2023-01-01');
INSERT INTO CostOfLivingData_costoflivingdata  (city_id, item, price, date) VALUES (1, 'Pair of Jeans', 60.00, '2023-01-01');

-- Repeat similar INSERT statements for each city with appropriate city_id

