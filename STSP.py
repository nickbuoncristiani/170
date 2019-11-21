
import networkx as nx
import mlrose
import matplotlib.pyplot as plt
from networkx.algorithms import approximation

"""
Gets graph which can be interpreted by TSP to give STSP through vertices.
Graph connects all homes by their shortest paths in a complete graph. 
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
    paths=dict(nx.all_pairs_shortest_path(G)) #store all shortest paths.
    C=get_complete_graph(G, vertices) 
    
    #get input to the TSP problem. Input is a list of node pairs and their distances.
    for i in range(len(vertices)):
        for j in range(i+1, len(vertices)): dists.append((i, j, C[vertices[i]][vertices[j]]['weight']))

    #copied from documentation, best_state is the TSP path on C and is the only variable we care about. 
    fitness_dists = mlrose.TravellingSales(distances=dists)
    problem_fit = mlrose.TSPOpt(length=len(C), fitness_fn=fitness_dists, maximize=False)
    best_state, _ = mlrose.genetic_alg(problem_fit, random_state = 2)  

    #We are going to replace all edges traversed in C with their corresponding paths in G. 
    tsp=[]
    
    tsp.extend(paths[vertices[best_state[0]]][vertices[best_state[1]]])
    for k in range(1,len(best_state)-1):
        tsp.pop() #prevent path overlap
        tsp.extend(paths[vertices[best_state[k]]][vertices[best_state[k+1]]])
    tsp.extend(paths[tsp.pop()][tsp[0]][0:-1]) #connect end point back to start 
    
    start_index=tsp.index(start) 
    #Since TSP has arbitary starting point, we want to 
    #rotate the result so that it starts where we want.
    tsp=tsp[start_index:]+tsp[0:start_index]  
    tsp.append(tsp[0]) #add start vertex to end to complete the tour
    return tsp

"""
Solve TA dropoff problem on G given set of homes. Starting point is first element in homes

Input: Graph, List of vertices which correspond to homes (and soda)

Output: list of tuples where first element in tuple is location along the drive and second is set of TAs 
which get dropped off at that location. I.E output to the example in the spec would look like
[(soda, {cory}), (dwinelle, {wheeler, rsf}), (campanile, campanile), (barrows, {}), (soda, {})]. In our case we will
probably use ints instead of strings. 
"""
def ta_dropoff(G, homes):
    drive=stsp(G, homes) #optimal drive which drops of all TAs off at their homes.
    marked=set()
    #extending the STSP solution so that it can be interpreted as a solution to the TA dropoff problem. 
    for i in range(len(drive)): 
        #set corresponds with TAs which were dropped off at this point. Remember that 
        #Ta's are identified by the houses in which they live. 
        drive[i]=[drive[i], set()] 
        if drive[i][0] in homes and drive[i][0] != homes[0] and drive[i][0] not in marked: 
            drive[i][1].add(drive[i][0]) #drop TA off the first time we visit house. avoid repeat dropoffs by marking. 
            marked.add(drive[i][0])
    
    #collapse lone paths. 
    i=1
    while i<len(drive)-1:
        while drive[i-1][0]==drive[i+1][0] and len(drive[i][1])<2: 
            drive[i-1][1]=drive[i-1][1].union(drive.pop(i)[1])
            drive[i-1][1]=drive[i-1][1].union(drive.pop(i)[1])
            i-=1
        i+=1

    return drive

"""
Input: list returned from calling ta_dropoff and Graph G
Returns the total energy that the driver and TA's will take in total.
"""
def energy(G, locations):
    paths = dict(nx.all_pairs_shortest_path_length(G))
    driving_dis = 0
    walking_dis = 0

    #looping over each of the locations to find the distance needed to travel between a vertex and the next
    for i in range(len(locations) - 1):
        vertex = locations[i][0]
        nextVertex = locations [i + 1][0]
        driving_dis = driving_dis + paths[vertex][nextVertex]

    #looping over the locations to compare the walking the TAs have to do from where they get dropped off to home
    for location in locations:
        starting = location[0]
        for home in location[1]:
            walking_dis = walking_dis + paths[starting][home]

    return walking_dis + (2/3*(driving_dis))

        
if __name__ == "__main__":
    G=nx.Graph([(0, 1), (1, 2), (2, 3), (3, 0), (1, 4), (2, 5), (0, 6), (6, 7), (7, 8), (8, 0), (1, 8), (2, 4), (4, 5)])
    print(ta_dropoff(G, [0, 1, 8, 7, 5, 3]))
    
    nx.draw_networkx(G, with_labels=True)
    
    plt.show()

