import STSP, readMM
import sys
import random
import networkx as nx
import matplotlib.pyplot as plt
from random import sample

#get input file from .mtx file
def generate_input(infile, outfile, size=50):
    print(infile)
    g=readMM.read_graph(infile)
    print(g.nodes())
    houses=random.sample(g.nodes(), size)
    with open(outfile, 'w') as file:
        file.write(str(len(g)) + '\n')
        file.write(str(size) + '\n')
        file.write(' '.join([str(i) for i in range(len(g))]) + '\n')
        file.write(' '.join([str(e) for e in houses]) + '\n')
        file.write(str(houses[0]) + '\n')
        m=nx.to_numpy_array(g)
        for row in m:
            file.write(' '.join([str(int(e)) if int(e)==1 else 'x' for e in row]) + '\n')

def solve(infile, output):
    with open(infile, 'r') as file:
        reader=file.readlines()
        g=nx.Graph()
        homes=list(map(int, reader[3].split(' ')))
        matrix=reader[5:]
        for i in range(len(matrix)):
            row = matrix[i].strip().split(' ')
            for j in range(len(row)):
                if row[j] != 'x':
                    g.add_edge(i+1, j+1, weight=float(row[j]))
        
        drive = STSP.ta_dropoff(g, homes)
        with open(output, 'w') as file:
            for stop in drive: file.write(str(stop[0]))



#Enter filename which corresponds with input 
if __name__ == "__main__":
    generate_input(sys.argv[1], sys.argv[2])
    solve(sys.argv[2], 1)
