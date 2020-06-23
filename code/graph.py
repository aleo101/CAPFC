import sys
import copy 
import matplotlib.pyplot as plt
import networkx as nx
import googlemaps
import pickle
import time
import csv
from itertools import islice
#import re

def distance(source, dest):
    #Requires API key 
    gmaps = googlemaps.Client(key = 'API_KEY') 
  
    #Requires destination and source names 
    my_dist = gmaps.distance_matrix(source, dest, units="imperial")
    
    #returning result
    return (my_dist) 

def counties_graph():
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
    G_with_edges = copy.deepcopy(G) # just use g2?
    edgelist = G_with_edges.edges(data='weight')
    num_of_removed_paths = 0
    for x in edgelist: #parse through all edges in the graph
        if x[2] > nx.dijkstra_path_length(G_with_edges, x[0], x[1]): #if the edge is longer than shortest path...
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
    for x in edgelist: #iterate through all edges in the graph
        if x[2] > 154: # If the edge is > 154 miles
            #and there is a closer neighbor for both nodes
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
    
def find_next_shortest_paths(G, source, target, k, weight= 'weight'):
    return list(islice(nx.shortest_simple_paths(G, source, target, weight=weight), k))
    
def find_shortest_path( max_cases, G, county_check1, county_check2):    
    for path in find_next_shortest_paths(G, county_check1, county_check2, 30): #check the next k shortest paths 
        total_cases_on_path = 0
        #print("checking path: " + str(path))
        for node in path:
            total_cases_on_path = total_cases_on_path + G.nodes[node]['attr1']
        if total_cases_on_path < max_cases:
            # print("--->The path takes this route: " + str(path) 
            # print('-->Total cases: ' + str(total_cases_on_path))
            length=0
            for l in range(len(path)-1):
                length = length + G[path[l]][path[l+1]]['weight']
            #print(f"length between {path[l]} and {path[l+1]} = {G[path[l]][path[l+1]]['weight']}")
            #print("Total Distance: {}".format(length))
            return path, length, total_cases_on_path 
   
    return [], 0, total_cases_on_path   
    
def total_cases(graph, county_check1, county_check2):      
    total_cases_on_path = 0
    for j in nx.dijkstra_path(G, county_check1, county_check2):
        total_cases_on_path = total_cases_on_path + G.nodes[j]['attr1']
    #print("total cases on this path: " + str(total_cases_on_path))
    return total_cases_on_path   
    
def get_county_web_data(county):
    county = county.strip()
    switcher = {
        'Alameda'         : "http://www.acphd.org/2019-ncov.aspx",
        'Butte'           : "https://www.buttecounty.net/publichealth/Home/fbclid",
        'Contra Costa'    : "https://www.contracosta.ca.gov/CivicAlerts.aspx?AID=2180",
        'Fresno'          : "https://www.co.fresno.ca.us/departments/public-health/covid-19",
        'Kern'            : "https://kernpublichealth.com/2019-novel-coronavirus/",
        'Los Angeles'     : "http://publichealth.lacounty.gov/media/coronavirus/",
        'Monterey'        : "https://www.co.monterey.ca.us/government/departments-a-h/administrative-office/office-of-emergency-services/response/covid-19",
        'Orange'          : "https://occovid19.ochealthinfo.com/coronavirus-in-oc",
        'Placer'          : "https://www.placer.ca.gov/6367/Novel-Coronavirus-COVID-19",
        'Riverside'       : "https://www.rivcoph.org/coronavirus",
        'Sacramento'      : "https://www.saccounty.net/COVID-19/Pages/default.aspx",
        'San Bernardino'  : "https://sbcovid19.com/",
        'San Diego'       : "https://www.sandiegocounty.gov/coronavirus.html",
        'San Francisco'   : "https://sf.gov/topics/coronavirus-covid-19",
        'San Joaquin'     : "http://www.sjcphs.org/coronavirus.aspx",
        'San Mateo'       : "https://www.smchealth.org/coronavirus",
        'Santa Barbara'   : "https://publichealthsbc.org/",
        'Santa Clara'     : "https://www.sccgov.org/sites/covid19/Pages/dashboard.aspx",
        'Shasta'          : "https://www.co.shasta.ca.us/covid-19/overview",
        'Solano'          : "https://www.solanocounty.com/depts/ph/coronavirus.asp",
        'Sonoma'          : "https://www.sonomacounty.com/coronavirus",
        'Stanislaus'      : "http://schsa.org/publichealth/pages/corona-virus/",
        'Tulare'          : "https://tchhsa.org/eng/index.cfm/public-health/covid-19-updates-novel-coronavirus/",
        'Ventura'         : "https://www.vcemergency.com/"
    }
    return switcher.get(county, "https://www.google.com/intl/en_us/covid19/")


def line_sep(number):
    for i in range(number):
        print("""
                ********************************************************************
            """)
#############################################################################################################

#save G as graph object 
# G = counties_graph()
# filehandler = open('counties_ca_far_removed_6_16.obj', 'wb')
# pickle.dump(G, filehandler)

#Load Graph object
filehandler = open('counties_ca_far_removed_6_16.obj', 'rb')
G = pickle.load(filehandler)
filehandler.close()

''' **This block of code removes far edges to make the graph better reflect a real world map**
    **It also adds the case totals for each county as a nodal attribute**
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
nx.set_node_attributes(G, attrs)

filehandler = open('counties_ca_far_removed_6_16.obj', 'wb') #save graph obj in its final form.
pickle.dump(G, filehandler)
filehandler.close()
'''
line_sep(1)
print("digraph has %d nodes with %d edges" % (nx.number_of_nodes(G), nx.number_of_edges(G)))
print("number of nodes: " + str(G.number_of_nodes()))
print("number of edges : " + str(G.number_of_edges()))
line_sep(2)


nx.draw_networkx(G)
plt.show(block=False)



for i in range(23):
    node_to_list = list(G.nodes)[i]
    print(node_to_list, end = ": ")
    print(f"{G.nodes[node_to_list]['attr1']} cases") 
#print("edges: {}".format(G.edges())) #very long edge list
line_sep(2)

while True:
    while True:                                                                             
        county_check1 = input("Enter First County (case sensitive): ") + ', CA'
        if G.has_node(county_check1) == False:
            print("Node, " + county_check1 + " doesn't exist. Try again")
            line_sep(1)
            continue
        else:
            break
    while True:
        county_check2 = input("Enter Second County (case sensitive): ") + ', CA'
        if G.has_node(county_check2) == False:
            print("Node, " + county_check2 + " doesn't exist. Try again")
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
            
    print("") 
    
    total_cases_on_path = total_cases(G, county_check1, county_check2)
    if total_cases_on_path > max_cases:
        k_short_path, length, total_cases_on_path = find_shortest_path( max_cases, G, county_check1, county_check2 ) 
        if not k_short_path:
            most_infectious_county = sorted(G.nodes().items(), key = lambda x: x[1]['attr1'], reverse=True)[0][0] #need to only use nodes on the path 
            print(most_infectious_county)
            print("Sorry, there are no paths which encounter less than the max set COVID-19 cases.")
            
        else:
            print(f'--->The path takes this route: {k_short_path}.') 
            print(f'--->Total cases: {total_cases_on_path}.')
            print(f'--->Total path distance: {length} miles.')
            print(get_county_web_data(county_check2))
    else:       
        print("--->The path takes this route: " + str(nx.dijkstra_path(G, county_check1, county_check2)))
        print(f"(Dij)--->Total path distance: {nx.dijkstra_path_length(G, county_check1, county_check2)} miles.")
        print(f"The path has {total_cases_on_path} cases which is under the maximum of {max_cases}.")
        print(f"finding the website for {county_check2}")
        print(get_county_web_data(county_check2.split(",")[0])) 
    line_sep(2)     
