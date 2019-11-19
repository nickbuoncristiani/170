
import networkx as nx
import matplotlib.pyplot as plt
import STSP

"""
Given a .mtx file, read matrix into networkx graph. Note the matrix/graph should be connected. 
get matrices from here https://sparse.tamu.edu/
Make sure to specify that you want exactly one strongle connected component otherwise the graph 
won't be connected. Download mtx file and then input this file to the function below.
"""
def read_graph(filename):
    g=nx.Graph()
    with open(filename, 'r') as file:
        reader=file.readlines()
        start=0
        while reader[start][0]=='%': start+=1 
        for i in range(start+1, len(reader)):
            coords=reader[i].split(' ')
            if int(coords[0]) != int(coords[1]): g.add_edge(int(coords[0]), int(coords[1]), weight=1)
            
    return g

if __name__ == "__main__":
    g=read_graph('ash85.mtx')
    print(STSP.ta_dropoff(g, [52, 46, 17, 8]))
    nx.draw_networkx(g, show_labels=True)
    plt.show()
    