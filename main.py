import STSP, readMM, reader_utils
import os, sys
import random
import networkx as nx
import matplotlib.pyplot as plt
from random import sample

#get input file as specified by spec from .mtx file. size corresponds to number of homes we want in our test case.
#homes are selected randomly.
def generate_input(infile, outfile, size):
    g=readMM.read_graph(infile)
    nodes=set(g.nodes)
    print(nodes)
    houses=random.sample(nodes, size)
    print(houses)
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
    
#arguments: matrix name, num homes
if __name__ == "__main__":
    if not(os.path.exists(sys.argv[1]+'.in')):
        generate_input(sys.argv[1]+".mtx", sys.argv[1]+'.in', size=int(sys.argv[2]))
    solve(sys.argv[1]+'.in', sys.argv[1]+'.out')
