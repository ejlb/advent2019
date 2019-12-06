import networkx as nx

orbits = open('006.txt', 'r').readlines()
edges = [o.strip().split(')') for o in orbits]

G = nx.DiGraph()
G.add_edges_from(edges)

ancestors = sum([len(nx.ancestors(G, n)) for n in G.nodes()])
print('direct + indirect', ancestors)

G = G.to_undirected()

shortest_path = nx.astar_path_length(G, source='YOU', target='SAN')-2
print('path', shortest_path)
