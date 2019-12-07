import STSP, readMM, reader_utils, main
import os, sys
import random
import networkx as nx
import matplotlib.pyplot as plt
from random import sample
"""
def local_cycle(dropoffs, graph):
    dropoff_length = len(dropoffs)
    path = []
    for i in range(dropoff_length):
        path.append(dropoffs[i][0])
    for i in range(dropoff_length - 4):
        neighbours = list(nx.neighbours(graph, i))
        for j in range(1, dropoff_length):
            if dropoffs[j][0] in neighbours and dropoffs[i][0] != 
        
        
        for e in nx.neighbours(graph, i):
        
"""
def solve(infile, output):
    inputs = reader_utils.read_input(infile)
    dropoffs=STSP.ta_dropoff(inputs[0], inputs[2], inputs[1])
    reader_utils.write_output(dropoffs, inputs[3], output)
    nx.draw(inputs[0])
    plt.show()
    return STSP.energy(inputs[0], dropoffs)


def get_complete_graph(G, vertices):
    l=nx.all_pairs_shortest_path_length(G)
    C=nx.Graph()
    for vertex in l:
        if vertex[0] in vertices:
            for v in vertex[1]:
                if v in vertices:
                    C.add_edge(vertex[0], v, weight=vertex[1][v])
    return C    
    
if __name__ == "__main__": 
    
    #main.solve(str(1)+'_50.in', str(1)+'_50.out')
    
    for i in range(1, 2):
        if os.path.exists(str(i)+'_50.in'):    
            main.solve(str(i)+'_50.in', str(i)+'_50.out')
        if os.path.exists(str(i)+'_100.in'):
            main.solve(str(i)+'_100.in', str(i)+'_100.out')
        if os.path.exists(str(i)+'_200.in'):
            main.solve(str(i)+'_200.in', str(i)+'_200.out')
   