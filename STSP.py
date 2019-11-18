
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import approximation
    

"""
Gets graph which can be interpreted by TSP to give STSP through vertices
"""    
def get_complete_graph(G, vertices):
    l=nx.all_pairs_shortest_path_length(G)
    C=nx.Graph(vertices)
    for vertex in l:
        if vertex[0] in vertices:
            for v in vertex[1]:
                if v in vertices:
                    C.add_edge(vertex[0], v, weight=vertex[1][v])
    return C

def 
    
if __name__ == "__main__":
    G=nx.Graph([(1, 2), (2, 3), (3, 4), (4, 1)])
    l=nx.all_pairs_shortest_path_length(G)
    
    #S=approximation.steiner_tree(G, [1, 2])
    #nx.draw_networkx(S, with_labels=True)
    #plt.show()

