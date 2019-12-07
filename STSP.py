
import networkx as nx
import mlrose
import matplotlib.pyplot as plt
from networkx.algorithms import approximation

"""
Figure out best, path along a cycle. 
"""
def cycle_optimize(G, cycle, homes):
    print('this is harder than I thought.')

def metric_tsp(G, start=None):
    mst = nx.minimum_spanning_tree(G, weight='weight')
    return nx.dfs_preorder_nodes(mst, source=start)   

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
    #dists=[]
    paths=dict(nx.all_pairs_shortest_path(G)) #store all shortest paths.
    
    C=get_complete_graph(G, vertices) 
    best_state=list(metric_tsp(C, start=start))
    
    
    #get input to the TSP problem. Input is a list of node pairs and their distances.
    #for i in range(len(vertices)):
    #    for j in range(i+1, len(vertices)): dists.append((i, j, C[vertices[i]][vertices[j]]['weight']))
#
    ##copied from documentation, best_state is the TSP path on C and is the only variable we care about. 
    #fitness_dists = mlrose.TravellingSales(distances=dists)
    #problem_fit = mlrose.TSPOpt(length=len(C), fitness_fn=fitness_dists, maximize=False)
    #
    #print('Computing TSP...')
    ##best_state, _ = mlrose.genetic_alg(problem_fit, random_state = 2)
    #best_state, _  = mlrose.genetic_alg(problem_fit, mutation_prob = 0.5, random_state = 2)
    #print('Finished computing TSP.')

    #We are going to replace all edges traversed in C with their corresponding paths in G. 
    tsp=[]
    #tsp.extend(paths[vertices[best_state[0]]][vertices[best_state[1]]])
    tsp.extend(paths[best_state[0]][best_state[1]])
    for k in range(1,len(best_state)-1):
        tsp.pop() #prevent path overlap
        #tsp.extend(paths[vertices[best_state[k]]][vertices[best_state[k+1]]])
        tsp.extend(paths[best_state[k]][best_state[k+1]])
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
def ta_dropoff(G, start, homes):
    #G=approximation.steiner_tree(G, [start]+homes)
    #G=nx.minimum_spanning_tree(G)
    drive=stsp(G, [start] + homes) #optimal drive which drops of all TAs off at their homes.
    
    marked=set()
    #extending the STSP solution so that it can be interpreted as a solution to the TA dropoff problem. 
    for i in range(len(drive)): 
        #set corresponds with TAs which were dropped off at this point. Remember that 
        #Ta's are identified by the houses in which they live. 
        drive[i]=[drive[i], set()] 
        if drive[i][0] in homes and drive[i][0] not in marked: 
            drive[i][1].add(drive[i][0]) #drop TA off the first time we visit house. avoid repeat dropoffs by marking. 
            marked.add(drive[i][0])
    
    #collapse lone paths. 
    i=1
    while i<len(drive)-1:
        while i>0 and i<len(drive)-1 and drive[i-1][0]==drive[i+1][0] and len(drive[i][1])<2: 
            drive[i-1][1]=drive[i-1][1].union(drive.pop(i)[1])
            drive[i-1][1]=drive[i-1][1].union(drive.pop(i)[1])
            i-=1
        i+=1

    for i in range(len(drive)):
        for j in range(i+1, len(drive)):
            if drive[i][0]==drive[j][0]:
                drive[i][1]=drive[i][1].union(drive[j][1])
                drive[j][1]=set()

    seen = {}
    i=0
    while i < len(drive):
        if drive[i][0] in seen:
            last=seen[drive[i][0]]
            seen[drive[i][0]]=i
            drive = drive[:last] + cycle_check(G, drive[last:i+1]) + \
                drive[i+1:len(drive)]
        else:
            seen[drive[i][0]]=i
        i+=1

    #new_dropoffs = [node[0] for node in drive if len(node[1])>0]
    #if start not in new_dropoffs: new_dropoffs = [start] + new_dropoffs
    #new_drive = stsp(G, new_dropoffs)
#
    #marked=set()
    ##extending the STSP solution so that it can be interpreted as a solution to the TA dropoff problem. 
    #for i in range(len(new_drive)): 
    #    #set corresponds with TAs which were dropped off at this point. Remember that 
    #    #Ta's are identified by the houses in which they live.
    #    dropoffs=set() 
    #    if new_drive[i] not in marked:
    #        for k in range(len(drive)): 
    #            if drive[k][0] == new_drive[i]: 
    #                dropoffs=drive[k][1]
    #                break
    #        marked.add(new_drive[i])
    #    new_drive[i]=[new_drive[i], dropoffs] 

    print(drive)
    print('Total energy used: '+ str(energy(G, drive)))
    return drive

"""
Input: list returned from calling ta_dropoff and Graph G
Returns the total energy that the driver and TA's will take in total.
"""
def energy(G, locations):
    paths = dict(nx.shortest_path_length(G, weight='weight'))
    driving_dis = 0
    walking_dis = 0
    #looping over each of the locations to find the distance needed to travel between a vertex and the next
    for i in range(len(locations) - 1):
        vertex = locations[i][0]
        nextVertex = locations[i + 1][0]
        driving_dis = driving_dis + paths[vertex][nextVertex]

    #looping over the locations to compare the walking the TAs have to do from where they get dropped off to home
    for location in locations:
        starting = location[0]
        for home in location[1]:
            walking_dis = walking_dis + paths[starting][home]

    return walking_dis + (2/3)*(driving_dis)

def largest_subcycle(cycle, node):
    side = {}
    node_index = cycle.index(node)
    for i in range(node_index+1, len(cycle)-1):
        #side.add(cycle[i])
        side[cycle[i][0]]=i
    i=node_index
    best=i
    while i>0:
        if cycle[i][0] in side:
            best=i
        i-=1
    print(cycle[best+1:side[cycle[best][0]]+1])
    if best != node_index:
        return best, cycle[best+1:side[cycle[best][0]]+1]
    else:
        return best, []

def cycle_check(G, cycle):
    homes=[cycle[0]] + [node for node in cycle[1:] if len(node[1])>=1]
    through_cycle = energy(G, cycle) 
    cycle_copy = [[node[0], set(node[1])] for node in cycle]
    
    if len(homes)<2:
        return cycle
    second_last = homes[-2]
    second_last_index = cycle.index(second_last)

    no_cycle_path = cycle_copy[:second_last_index+1]
    no_cycle_path[second_last_index][1] = no_cycle_path[second_last_index][1].union(homes[-1][1])
    no_cycle = no_cycle_path[:]
    for i in reversed(range(len(no_cycle_path) - 1)):
        no_cycle.append([no_cycle_path[i][0], set()])

    #driving = 2*(2/3*(nx.shortest_path_length(G, source = second_last[0], target = homes[0][0])))
    #walking = nx.shortest_path_length(G, source = second_last[0], target = homes[-1][0])
    #no_cycle = driving + walking
    
    if through_cycle < energy(G, no_cycle):
        return cycle
    else:
        return no_cycle
    #homes=[cycle[0]] + [node for node in cycle[1:] if len(node[1])>=1]
    #through_cycle = energy(G, cycle) 
    #cycle_copy = [[node[0], set(node[1])] for node in cycle]
    #
    #if len(homes)<2:
    #    return cycle 
    #second_last = homes[-2]
    #second_last_index, path = largest_subcycle(cycle, second_last)
    ##second_last_index = cycle.index(second_last)
#
    #no_cycle_path = cycle_copy[:second_last_index+1]+path 
#
    #no_cycle_path[second_last_index][1] = no_cycle_path[second_last_index][1].union(homes[-1][1])
    #no_cycle = no_cycle_path[:]
    #for i in reversed(range(second_last_index)):
    #    no_cycle.append([no_cycle_path[i][0], set()])
#
    ##driving = 2*(2/3*(nx.shortest_path_length(G, source = second_last[0], target = homes[0][0])))
    ##walking = nx.shortest_path_length(G, source = second_last[0], target = homes[-1][0])
    ##no_cycle = driving + walking
    #if through_cycle < energy(G, no_cycle):
    #    return cycle
    #else:
    #    return no_cycle
        
if __name__ == "__main__":
    G=nx.Graph([(0, 1), (1, 2), (2, 3), (3, 0), (1, 4), (2, 5), (0, 6), (6, 7), (7, 8), (8, 0), (1, 8), (2, 4), (4, 5)])
    ta_dropoff(G, 0, [1, 8, 7, 5, 3])
    
    nx.draw_networkx(G, with_labels=True)
    
    plt.show()
    
