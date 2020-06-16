import re
import sys
import copy 
import matplotlib.pyplot as plt
import networkx as nx
import googlemaps
import pickle
import time
import csv
from itertools import islice

def distance(source, dest):
    #Requires API key 
    gmaps = googlemaps.Client(key = 'API_KEY') 
  
    #Requires destination and source names 
    my_dist = gmaps.distance_matrix(source, dest, units="imperial")
    
    #returning result
    return (my_dist) 

def cities_graph():
    #file = open(r'..\resources\data\top_100_cities_cali.txt')
    G = nx.Graph()
    with open(r'..\resources\data\populous-ca-counties-6-6-2020.csv', newline='') as csvfile:
        linereader = csv.reader(csvfile, delimiter=',')
        for row in linereader:
            if row[0].startswith("#"): #skip commented lines
                continue 
            line = row[1].strip() + ", CA"  #County name (ex: "Sonoma")
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
    line_sep(1)
    print("The number of removed inefficient edges is : {}".format(num_of_removed_paths))
    return G
    
def remove_far_edges(G):
    G2 = copy.deepcopy(G) # equal to cases_edge_weight(G) when cases data is finished. 
    edgelist = G2.edges(data='weight')
    num_of_removed_paths = 0
    for x in edgelist: #parse through all edges in the graph
        if x[2] > 154:
            for neighbor in G.neighbors(x[0]):
                if G[x[0]][neighbor]['weight'] < G[x[0]][x[1]]['weight']:
                    for neighbor in G.neighbors(x[1]):
                        if G[x[1]][neighbor]['weight'] < G[x[0]][x[1]]['weight']:
                            G.remove_edge(x[0], x[1])  #...remove the edge 
                            print("removing path between " + str(x[0]) + " and " + str(x[1]))
                            num_of_removed_paths += 1
                            break 
                    break
    print("Removed {} paths".format(num_of_removed_paths))    
    line_sep(1) 
    return G
    
def k_shortest_paths(G, source, target, k, weight= 'weight'):
    return list(islice(nx.shortest_simple_paths(G, source, target, weight=weight), k))

def line_sep(number):
    for i in range(number):
        print("""
                ********************************************************************
            """)
#############################################################################################################
# G = cities_graph()
# filehandler = open('counties_ca_6_16.obj', 'wb')
# pickle.dump(G, filehandler)

filehandler = open('counties_ca_6_16.obj', 'rb')
G = pickle.load(filehandler)
G= remove_far_edges(G)


attrs = {'Alameda': {'attr1': 0}}
with open(r'..\resources\data\populous-ca-counties-6-6-2020.csv', newline='') as csvfile:
    linereader = csv.reader(csvfile, delimiter=',')
    row_num = 0
    
    for row in linereader:
        if row[0].startswith("#"): #skip commented lines
            continue 
        case_number = int(row[4]) #index 4 is county case number
        attrs[list(G.nodes)[row_num]] = {'attr1': case_number}
        row_num = row_num + 1
        #if row_num ==2 : break
nx.set_node_attributes(G, attrs)
line_sep(1)
print("digraph has %d nodes with %d edges" % (nx.number_of_nodes(G), nx.number_of_edges(G)))
print("number of nodes: " + str(G.number_of_nodes()))
print("number of edges : " + str(G.number_of_edges()))
line_sep(2)
for i in range(23):
    node_to_list = list(G.nodes)[i]
    print(node_to_list, end = ": ")
    print(G.nodes[node_to_list]['attr1']) 
#print("edges: {}",format(G.edges())) #very long edge list
filehandler.close()
nx.draw_networkx(G)
plt.show()
line_sep(2)
while True:
    while True:
        city_check1 = input("Enter First County (case sensitive): ") + ', CA'
        if G.has_node(city_check1) == False:
            print("Node, " + city_check1 + " doesn't exist. Try again")
            line_sep(1)
            continue
        else:
            break
    while True:
        city_check2 = input("Enter Second County (case sensitive): ") + ', CA'
        if G.has_node(city_check2) == False:
            print("Node, " + city_check2 + " doesn't exist. Try again")
            continue 
        else:
            break 
    while True:
        max_cases = input("Maximum you are willing to encounter: ")
        try: 
            max_cases = int(max_cases)
            break
        except ValueError:
            print("Error: Input must be a positive integer...")
            
    print("Max Case allowed: {}".format(max_cases))  
    line_sep(1)
    print("(Dij) The path distance between " +city_check1+ " and " + city_check2 + " is " + str( nx.dijkstra_path_length(G, city_check1, city_check2)))
    print("--->The path: " + str(nx.dijkstra_path(G, city_check1, city_check2)))
    
    total_cases_on_path = 0
    for j in nx.dijkstra_path(G, city_check1, city_check2):
        total_cases_on_path = total_cases_on_path + G.nodes[j]['attr1']
    print("total cases on this path: " + str(total_cases_on_path))
    if total_cases_on_path > max_cases:
        for path in k_shortest_paths(G, city_check1, city_check2, 30):
            total_cases_on_path = 0
            print("checking path: " + str(path))
            for k in path:
                total_cases_on_path = total_cases_on_path + G.nodes[k]['attr1']
            if total_cases_on_path < max_cases:
                print(str(path) + '--> cases: ' + str(total_cases_on_path))
                break
                
    else: 
        print("The path has " + str(total_cases_on_path) + " which is under the max: " +
            str(max_cases))
    line_sep(2)    

    
