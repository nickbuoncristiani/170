"""
Space for figuring out how to run STSP on networkx 
"""
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import approximation
import mip 


if __name__ == "__main__":
    G=nx.Graph([(1, 2), (2, 3), (3, 4), (4, 1)])
    S=approximation.steiner_tree(G, [1, 2, 3])
    nx.draw_networkx(S, with_labels=True)
    plt.show()