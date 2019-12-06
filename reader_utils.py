import networkx as nx
import matplotlib.pyplot as plt
import STSP

"""
Given a naive .in file with properties as defined in the spec, read input into 0-indexed networkx graph. 
Calculates approximate 'cycle', then outputs to file.
Assumes the matrix given is symmetric and obeys the triangle inequality for now.
Assumes the file is well-defined for now.
"""

def read_input(filename):
    """
    Given .in file, models the nodes of the graph with a dictionary and creates networkx graph.
    """
    g = nx.Graph()
    with open(filename, 'r') as file:
        n=int(file.readline().strip())
        num_homes = int(file.readline().replace('\n', ''))
        g_nodes = file.readline()
        g_homes = file.readline()
        g_start = file.readline()
        
        def to_dict(nodes):
            """0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84
            Transforms raw readline, nodes, into corresponding dictionary of their numerical representations.
            0-indexed.
            """
            nodes = nodes.replace('\n', '').split()
            dict = {}
            count = 0
            for i in nodes:
                dict[i] = count
                count += 1
            return dict
        
        def get_homes(homes, keys):
            """
            Transforms raw readline, homes, into corresponding list in numerical representation.
            """
            homes = homes.replace('\n', '').split()
            for i in range(num_homes):
                homes[i] = keys[homes[i]]
            return homes
        
        def get_start(start, keys):
            """
            Transforms raw readline, start, into corresponding numerical representation.
            """
            return keys[start.replace('\n', '')]
        
        count = 0
        for line in file:
            temp = line.replace('\n', '').split()
            for i in range(len(temp)):
                if temp[i] != 'x':
                    g.add_edge(count, i, weight = float(temp[i]))  
            count += 1
    graph_numrep = to_dict(g_nodes)           
    return(g, get_homes(g_homes, graph_numrep), get_start(g_start, graph_numrep), graph_numrep)     

def write_output(dropoffs, keys, output):
    """
    Given a list of TA dropoffs of the form of a list of tuples and numerical representation,
    write to output with alphanumerical notation.    
    """
    with open(output, 'w+') as file:
        keys = {v: k for k, v in keys.items()}
        dropoff_nodes = []
        closed_path = []
        len_dropoffs = len(dropoffs)
        for i in range(len_dropoffs - 1):
            stop_i = keys[dropoffs[i][0]]
            file.write(stop_i + ' ')
            closed_path.append(stop_i)
            if len(dropoffs[i][1]) != 0:
                dropoff_nodes.append(stop_i)
        file.write(keys[dropoffs[len_dropoffs - 1][0]] + '\n')
        file.write(str(len(set(dropoff_nodes))) + '\n')
    
        for i in range(len_dropoffs):
            len_drop_i = len(dropoffs[i][1])
            if len_drop_i != 0:
                file.write(closed_path[i] + ' ')
                len_drop_list_i = list(dropoffs[i][1])
                for j in range(len_drop_i - 1):
                    file.write(keys[len_drop_list_i[j]] + ' ')
                file.write(keys[len_drop_list_i[len_drop_i - 1]] + '\n')
    
        
if __name__ == "__main__":
    inputs = read_input('ash85.in')
    g = inputs[0]
    
    write_output(STSP.ta_dropoff(g, inputs[2], inputs[1]), inputs[3], 'ash85.out')

    nx.draw_networkx(g, show_labels=True)
    plt.show()