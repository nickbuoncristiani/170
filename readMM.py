
import networkx as nx
import random
import matplotlib.pyplot as plt
import STSP

"""
Given a .mtx file, read matrix into networkx graph. Note the matrix/graph should be connected. 
get matrices from here https://sparse.tamu.edu/
Make sure to specify that you want exactly one strongle connected component otherwise the graph 
won't be connected. Download mtx file and then input this file to the function below.
"""
def read_graph(filename, n=1):
    g=nx.Graph()
    with open(filename, 'r') as file:
        reader=file.readlines()
        start=0 
        while reader[start][0]=='%': start+=1 #skip the comments at the start of the file. 
        for i in range(start+1, len(reader)):
            coords=reader[i].split(' ')
            weight=(1+random.random())*n #get weight in range n and 2n to satisfy triangle ineq
            #sparse format lists all nonzero values and their coordinates to save space. 
            #Having a nonzero value at i, j corresponds with having an edge between i, j
            if int(coords[0]) != int(coords[1]): g.add_edge(int(coords[0]), int(coords[1]), weight=weight)
            
    return g

if __name__ == "__main__":
    g=read_graph('bcspwr03.mtx')
    print(STSP.ta_dropoff(g, [i+1 for i in range(5)]))
    nx.draw_networkx(g, show_labels=True)
    plt.show()
    