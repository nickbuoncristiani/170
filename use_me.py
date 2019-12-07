import main
import os, sys
"""
Simply running this will attempt to solve for the entire class inputs.
"""
if __name__ == "__main__": 
    for i in range(1, 367):
        if os.path.exists(str(i)+'_50.in'):    
            main.solve(str(i)+'_50.in', str(i)+'_50.out')
        if os.path.exists(str(i)+'_100.in'):
            main.solve(str(i)+'_100.in', str(i)+'_100.out')
        if os.path.exists(str(i)+'_200.in'):
            main.solve(str(i)+'_200.in', str(i)+'_200.out')
   
    for filename in os.listdir():
        if filename.endswith('.in'):
            matrixname = filename[0:len(filename)-3]
            validate_output(filename, matrixname+'.out')