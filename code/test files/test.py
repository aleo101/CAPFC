import re
import sys
import copy 
import matplotlib.pyplot as plt
import networkx as nx
import googlemaps
import pickle
def distance(source, dest):
    #Requires API key 
    gmaps = googlemaps.Client(key = 'API_KEY') 
  
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
        if not "CA" in line:
            line = line.strip() + ", CA"
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
                print("distance between {node} and {node2} is : {dist}".format(node = node, node2=  dist['destination_addresses'][i].split(',')[0] + ", CA", dist = single_distance))
                G.add_edge(node, ",".join(dist['destination_addresses'][i].split(',', 2)[:2]), weight=single_distance)
        G3.remove_node(node)
    file.close()
    return G

    
    
G = cities_graph()
filehandler = open('graph_pi_shortest.obj', 'rb')
G = pickle.load(filehandler)
print("\n\n\n")
print("digraph has %d nodes with %d edges"
          % (nx.number_of_nodes(G), nx.number_of_edges(G)))
A = copy.deepcopy(G)
edgelist = A.edges(data='weight')

iter = 0
checked_edges = []
for x in edgelist:
    if x[0] not in checked_edges:
        if G.has_edge(x[0], "Clovis, CA"):
            print("Edge length from {} to Clovis: {}".format(x[0], G.edges[x[0], "Clovis, CA"]['weight']))
        print("Shortest path from {} to Clovis: {}\n\n".format(x[0], nx.dijkstra_path_length(G, x[0], "Clovis, CA")))
        iter+=1
        checked_edges.append(x[0])
        if iter == 20:
            break
print("\n\n\n\n\n\n")
print("Now the digraph has %d nodes with %d edges" % (nx.number_of_nodes(G), nx.number_of_edges(G)))
print("Shortest path from Oakland to clovis: {}\n\n".format(nx.dijkstra_path_length(G, "Oakland, CA", "Clovis, CA")))
print("Edge? : " + str(G.has_edge("Oakland, CA", "Clovis, CA")))

# print("number of nodes: " + str(G.number_of_nodes()))
# print("number of edges : " + str(G.number_of_edges()))
# print("\n\n\n")
# print("edges: {}",format(G.edges()))
# print(G['Los Angeles, CA'])
nx.draw_networkx(G)
plt.show()