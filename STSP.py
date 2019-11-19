
import networkx as nx
import mlrose
import matplotlib.pyplot as plt
from networkx.algorithms import approximation

"""
Gets graph which can be interpreted by TSP to give STSP through vertices
"""    
def get_complete_graph(G, vertices):
    l=nx.all_pairs_shortest_path_length(G)
    C=nx.Graph()
    for vertex in l:
        if vertex[0] in vertices:
            for v in vertex[1]:
                if v in vertices:
                    C.add_edge(vertex[0], v, weight=vertex[1][v])
    return C

"""
Return stsp on a given subset of vertices which starts and ends at start argument. 
Output is a list of vertex labels.  
"""
def stsp(G, vertices, start=None):
    if not start: start=vertices[0]
    dists=[]
    paths=dict(nx.all_pairs_shortest_path(G))
    C=get_complete_graph(G, vertices)
    
    for i in range(len(vertices)):
        for j in range(i+1, len(vertices)): dists.append((i, j, C[vertices[i]][vertices[j]]['weight']))

    fitness_dists = mlrose.TravellingSales(distances=dists)
    problem_fit = mlrose.TSPOpt(length=len(C), fitness_fn=fitness_dists, maximize=False)
    best_state, _ = mlrose.genetic_alg(problem_fit, random_state = 2)  

    tsp=[]
    
    tsp.extend(paths[vertices[best_state[0]]][vertices[best_state[1]]])
    for k in range(1,len(best_state)-1):
        tsp.pop()
        tsp.extend(paths[vertices[best_state[k]]][vertices[best_state[k+1]]])
    tsp.extend(paths[tsp.pop()][tsp[0]][0:-1])
    
    start_index=tsp.index(start)
    tsp=tsp[start_index:]+tsp[0:start_index]
    tsp.append(tsp[0]) #add start vertex to end to complete the tour
    return tsp

def ta_dropoff(G, homes):
    drive=stsp(G, homes)
    marked=set()
    for i in range(len(drive)): 
        drive[i]=[drive[i], set()]
        if drive[i][0] in homes and drive[i][0] not in marked: 
            drive[i][1].add(drive[i][0])
            marked.add(drive[i][0])
    i=1
    while i<len(drive)-1:
        while drive[i-1][0]==drive[i+1][0] and len(drive[i][1])<2: 
            drive[i-1][1]=drive[i-1][1].union(drive.pop(i)[1])
            drive[i-1][1]=drive[i-1][1].union(drive.pop(i)[1])
            i-=1
        i+=1

    return drive
        
if __name__ == "__main__":
    G=nx.Graph([(0, 1), (1, 2), (2, 3), (3, 0), (1, 4), (2, 5), (0, 6), (6, 7), (7, 8), (8, 0), (1, 8), (2, 4), (4, 5)])
    print(ta_dropoff(G, [0, 1, 8, 7, 5, 3]))
    
    nx.draw_networkx(G, with_labels=True)
    
    plt.show()

