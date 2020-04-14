import networkx as nx 
import copy
import matplotlib.pyplot as plt
G = nx.Graph()

G.add_nodes_from(["Sacramento", "Stockton", "Fresno", "Bakersfield", "LosAngeles", "SanDiego"])
G.add_edges_from([("Sacramento", "Stockton"), ("Stockton", "Fresno"), ("Fresno", "Bakersfield"),
("Bakersfield", "LosAngeles"), ("LosAngeles", "SanDiego")])
A = copy.deepcopy(G)
for node in A.nodes():
	G.add_edge(node, "NewYork")
	
print("number of nodes: " + str(G.number_of_nodes()))
print("number of edges : " + str(G.number_of_edges()))
print("New York neighbors: " + str([n for n in G.neighbors("NewYork")]))

nx.draw_networkx(G)

plt.savefig('plot.png')