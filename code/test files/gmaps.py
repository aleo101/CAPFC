import googlemaps 
  
# Requires API key 
gmaps = googlemaps.Client(key = 'API_STRING') 
  
# Requires cities name 
my_dist = gmaps.distance_matrix('Los Angeles', 'Cook County', units = "imperial")
  
# Printing the result 

print(my_dist['destination_addresses'][0])

# if within 300 miles and a city within 300 miles that is closer that we are already connected to
