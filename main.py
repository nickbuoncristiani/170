import STSP, readMM, reader_utils
import os, sys
import random
import networkx as nx
import matplotlib.pyplot as plt
from random import sample

#get input file as specified by spec from .mtx file. size corresponds to number of homes we want in our test case.
#homes are selected randomly.
def generate_input(infile, outfile):
    g=readMM.read_graph(infile)
    nodes=set(g.nodes)

    if len(g) > 150: size = 100
    elif len(g) > 100: size = 50
    else: size = 25
    
    houses=random.sample(nodes, size)
    
    start=random.choice(list(nodes - set(houses))) #make sure start isn't in homes. 
    with open(outfile, 'w') as file:
        file.write(str(len(g)) + '\n')
        file.write(str(size) + '\n')
        file.write(' '.join([str(node) for node in nodes]) + '\n')
        file.write(' '.join([str(house) for house in houses]) + '\n')
        file.write(str(start) + '\n')
        m=nx.to_numpy_array(g)
        for row in m:
            file.write(' '.join([str(round(float(e), 5)) if float(e)>0 else 'x' for e in row]) + '\n')

#master function. Return output file given input file. Incomplete. 
def solve(infile, output):
    inputs = reader_utils.read_input(infile)
    dropoffs=STSP.ta_dropoff(inputs[0], inputs[2], inputs[1])
    reader_utils.write_output(dropoffs, inputs[3], output)
    return STSP.energy(inputs[0], dropoffs)

def total_cost(refresh=False):
    total_energy=0
    for filename in os.listdir('Tests'):
        if filename.endswith('.mtx'):
            matrixname = filename[0:len(filename)-4]
            if not(os.path.exists('Tests/' + matrixname+ '.in')) or refresh:
                generate_input('Tests/' + filename, 'Tests/' + matrixname+'.in')
            total_energy += solve('Tests/' + matrixname+'.in', 'Tests/' + matrixname+'.out')
    return total_energy
    
#arguments: matrix name, num homes
if __name__ == "__main__":
    if sys.argv[1]=='all': 
        print('Running all tests...')
        print('Total cost is: ' + str(total_cost()))
    else:
        if not(os.path.exists(sys.argv[1]+'.in')):
            generate_input(sys.argv[1]+".mtx", sys.argv[1]+'.in')
        solve(sys.argv[1]+'.in', sys.argv[1]+'.out')
