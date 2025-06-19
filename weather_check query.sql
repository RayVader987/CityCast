CREATE DATABASE weather_app;
USE weather_app;

CREATE TABLE city_weather_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(100),
    country VARCHAR(50),
    temperature FLOAT,
    humidity INT,
    weather_desc VARCHAR(100),
    search_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLES city_weather_log;

DROP DATABASE weather_app;