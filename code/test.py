import re
import sys
import copy 
import matplotlib.pyplot as plt
import networkx as nx
import googlemaps
import pickle
from concurrent.futures import ThreadPoolExecutor
def distance(source, dest):
    #Requires API key 
    gmaps = googlemaps.Client(key = 'API_STRING') 
  
    #Requires cities name 
    my_dist = gmaps.distance_matrix(source, dest, units="imperial")
    
    #Printing the result 
    return (my_dist) 

def cities_graph():
    file = open(r'..\resources\data\top_100_cities_cali.txt')
    G = nx.Graph()
    cities = []
    
    for line in file.readlines():
        if line.startswith("#"):  # skip comments
            continue

        numfind = re.compile("^\d+")

        if numfind.match(line):  # this line is distances
            dist = line.split()
            for d in dist:
                G.add_edge(city, cities[i], weight=int(dist))
                i = i + 1
        else:  # this line is a city, position, population
            i = 1
            city = line.strip()
            cities.append(city)
            G.add_node(city)
    G2 = copy.deepcopy(G)
    G3 = copy.deepcopy(G)
    for node in G2.nodes():
        dist = distance(node, list(G3.nodes()))  # distance converted to miles
        for i in range(len(dist["rows"][0]["elements"])):
            single_distance = int(dist["rows"][0]["elements"][i]["distance"]["value"] * 0.000621371192)
            if(single_distance < 250 and single_distance !=0):
                if dist['destination_addresses'][i].split(',')[0] == 'Ontario' or dist['destination_addresses'][i].split(',')[0] == "Corona":
                    print("distance between {node} and {node2} is : {dist}".format(node = node, node2=  dist['destination_addresses'][i].split(',')[0] + ", CA", dist = single_distance))
                    G.add_edge(node, ",".join(dist['destination_addresses'][i].split(',', 2)[:2]), weight=single_distance)
                else:    
                    print("distance between {node} and {node2} is : {dist}".format(node = node, node2= dist['destination_addresses'][i].split(',')[0], dist = single_distance))
                    G.add_edge(node, dist['destination_addresses'][i].split(',')[0], weight=single_distance)
                 
        G3.remove_node(node)
    file.close()
    return G

    
    
G = cities_graph()
filehandler = open('graph_pi.obj', 'rb')
G = pickle.load(filehandler)
print("digraph has %d nodes with %d edges"
          % (nx.number_of_nodes(G), nx.number_of_edges(G)))

nx.draw_networkx(G)
print("number of nodes: " + str(G.number_of_nodes()))
print("number of edges : " + str(G.number_of_edges()))
print(G.nodes())
print("edges: {}",format(G.edges()))
plt.show()