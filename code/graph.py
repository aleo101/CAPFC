import re
import sys
import copy 
import matplotlib.pyplot as plt
import networkx as nx
import googlemaps
import pickle
import time
import csv

def distance(source, dest):
    #Requires API key 
    gmaps = googlemaps.Client(key = 'API_STRING') 
  
    #Requires destination and source names 
    my_dist = gmaps.distance_matrix(source, dest, units="imperial")
    
    #returning result
    return (my_dist) 

def cities_graph():
    #file = open(r'..\resources\data\top_100_cities_cali.txt')
    G = nx.Graph()
    cities = []
    with open(r'..\resources\data\populous-ca-counties-6-6-2020.csv', newline='') as csvfile:
        linereader = csv.reader(csvfile, delimiter=',')
        for row in linereader:
            if row[0].startswith("#"):
                continue 
            line = row[1].strip() #County name (ex: "Sonoma")
            #2 commente lines below are currently unused but may be useful in the future.
            #county = line.strip()
            #counties.append(county)
            G.add_node(line)
    G2 = copy.deepcopy(G)
    G3 = copy.deepcopy(G)
    for node in G2.nodes():
        dist = distance(node, list(G3.nodes()))  # distance between a single node and all others.
        for i in range(len(dist["rows"][0]["elements"])):   #for each destination.
            G3list = list(G3.nodes())  #same destination above but with correct nodal names.
            single_distance = int(dist["rows"][0]["elements"][i]["distance"]["value"] * 0.000621371192) #distance between node and a single iteration i. 
            if(single_distance !=0):
                print("distance between {node} and {node2} is : {dist}".format(node = node, node2=  G3list[i], dist = single_distance))
                #commented line below is no longer used.
                # <dist['destination_addresses'][i].split(',', 2)[:2]> returns a couple ['City", 'ST'] below line uses .join to make it a string 'City, St'.
                G.add_edge(node, G3list[i], weight=single_distance) #add edge between node and "node at index i" with weight as direct driving distance between.  
        G3.remove_node(node) #remove node whos edges have been calculated from list of nodes.
    G_with_edges = copy.deepcopy(G)
    edgelist = G_with_edges.edges(data='weight')
    num_of_removed_paths = 0
    for x in edgelist: #parse through all edges in the graph
        if x[2] > nx.dijkstra_path_length(G_with_edges, x[0], x[1]): #if the edge is longer than shortest path...
            #print("{} and {}".format(x[0], x[1]))
            G.remove_edge(x[0], x[1])  #...remove the edge 
            #print("removing path between" + str(x[0]) + "and" + str(x[1]))
            num_of_removed_paths += 1
    line_sep()
    print("The number of removed inefficient edges is : {}".format(num_of_removed_paths))
    return G
def line_sep():
    print("""
            ********************************************************************
            
           """)
    
def cases_edge_weight(G):
    G2 = copy.deepcopy(G)
    for node1 in G2.nodes():
        for node2 in G2.nodes():
            if G2.has_edge(node1, node2) == True:
                G2[node1][node2]['weight'] = 10
    return G2
G = cities_graph()
filehandler = open('counties_ca.obj', 'wb')
pickle.dump(G, filehandler)

# filehandler = open('counties_ca.obj', 'rb')
# G = pickle.load(filehandler)
filehandler.close()
#G2 = copy.deepcopy(G) # equal to cases_edge_weight(G) when cases data is finished. 
print("digraph has %d nodes with %d edges"
         % (nx.number_of_nodes(G), nx.number_of_edges(G)))
         
nx.draw_networkx(G)
print("number of nodes: " + str(G.number_of_nodes()))
print("number of edges : " + str(G.number_of_edges()))
line_sep()
line_sep()
#print("edges: {}",format(G.edges())) #very long edge list
plt.show()

while True:
    while True:
        city_check1 = input("Enter First City: ")
        if G.has_node(city_check1) == False:
            print("Node, " + city_check1 + " doesn't exist. Try again")
            continue
        else:
            break
    while True:
        city_check2 = input("Enter Second City: ")
        if G.has_node(city_check2) == False:
            print("Node, " + city_check2 + " doesn't exist. Try again")
            continue 
        else:
            break 
            
    print("The direct distance between " +city_check1+ " and " + city_check2 + " is " + str( G.get_edge_data(city_check1, city_check2, default=0)))
    print("(Dij) The path distance between " +city_check1+ " and " + city_check2 + " is " + str( nx.dijkstra_path_length(G, city_check1, city_check2)))
    print("--->The path: " + str(nx.dijkstra_path(G, city_check1, city_check2)))
    line_sep()
    #print("There are {} COVID-19 cases on this path".format(#call method that counts covid cases))
    