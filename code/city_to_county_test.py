from geopy.geocoders import Nominatim 
import re


def find_county(city):
    geolocator = Nominatim(user_agent= 'CAPFC')
    city_find = geolocator.geocode(city)
    return (city_find.address.split(', ')[1])

with open(r'..\resources\data\top_100_cities_cali.txt', 'r') as f:
    with open(r'..\resources\data\100_cities_AND_counties_cali.txt', 'r') as cf:
        for line in f.readlines():
            for county_line in cf.readlines():
                file_lines = [''.join([line.strip(), county_line, '\n'])]
                print(county_line) 

with open(r'..\resources\data\100_cities_AND_counties_cali.txt', 'w') as f:
    f.writelines(file_lines)
    print('wrote')