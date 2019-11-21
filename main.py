import STSP, readMM, reader_utils
import sys
import random
import networkx as nx
import matplotlib.pyplot as plt
from random import sample

#get input file as specified by spec from .mtx file. size corresponds to number of homes we want in our test case.
#homes are selected randomly.
def generate_input(infile, outfile, size=50):
    g=readMM.read_graph(infile)
    nodes=set(g.nodes)
    houses=random.sample(nodes, size)
    start=random.choice(list(nodes - set(houses))) #make sure start isn't in homes. 
    with open(outfile, 'w') as file:
        file.write(str(len(g)) + '\n')
        file.write(str(size) + '\n')
        file.write(' '.join([str(i) for i in range(len(g))]) + '\n')
        file.write(' '.join([str(e) for e in houses]) + '\n')
        file.write(str(start) + '\n')
        m=nx.to_numpy_array(g)
        for row in m:
            file.write(' '.join([str(int(e)) if int(e)==1 else 'x' for e in row]) + '\n')

#master function. Return output file given input file. Incomplete. 
def solve(infile, output):
    inputs = reader_utils.read_input(infile)
    reader_utils.write_output(STSP.ta_dropoff(inputs[0], inputs[2], inputs[1]), inputs[3], output)
    
#arguments: .mtx file, .in file, .out file, num homes
if __name__ == "__main__":
    generate_input(sys.argv[1], sys.argv[2], size=int(sys.argv[4]))
    solve(sys.argv[2], sys.argv[3])
