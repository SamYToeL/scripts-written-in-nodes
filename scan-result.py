#!/bin/env python3

from sys import argv
import os 
import numpy as np
def scantake(file):
    sysname = os.path.splitext(file)[0]
    print(sysname)
    f = open(log,'r')
    lines = f.readlines()
    f.close()
    Y_value = []
    for i, line in enumerate(lines):
        if 'Scan the potential surface.' in line:
            ind = i + 3
        if "SCF Done" in line:
            Y_value.append(float(line.split()[4]))
            

    #Variable   Value     No. Steps Step-Size
    scan_info = lines[ind]
    st_point = float(scan_info.split()[1])
    steps = int(scan_info.split()[2])
    step_size = float(scan_info.split()[3])
    X = np.linspace(st_point,st_point + steps*step_size, num=steps+1,endpoint=True,dtype=float)
    if len(Y_value) != steps+1:
        print('Number of results in log doesnt match the stepsl ')
        exit()
    
    with open(f'{sysname}.txt','w') as wf:
        wf.write("# Scan of Total Energy \n# X-Axis:  Scan Coordinate\n# Y-Axis:  Total Energy (Hartree)\n#                  X                   Y\n")
        for i in range(len(Y_value)):

            wf.write(f'        {X[i]:.10f}     {Y_value[i]:.10f}\n')
    

if __name__ == '__main__':
    log = argv[1]
    scantake(log)
    print('Please check the file.')
    
