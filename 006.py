import itertools
import networkx as nx

orbits = open('006.txt', 'r').readlines()
edges = [o.strip().split(')') for o in orbits]
nodes = set(itertools.chain(*edges))

G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

ancestors = sum([len(nx.ancestors(G, n)) for n in nodes])
print('direct + indirect', ancestors)

G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

shortest_path = nx.astar_path_length(G, source='YOU', target='SAN')-2
print('path', shortest_path)
