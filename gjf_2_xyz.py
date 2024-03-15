#!/usr/bin/env python3

import sys
import os

def get_coors(lines):
    space_l = []
    for i , line in enumerate(lines):
        if line.isspace():
            space_l.append(i)
    
    return lines[space_l[1]+2:space_l[2]]
            

gjf_file = sys.argv[1]

with open(gjf_file) as f:
    lines = f.readlines()
    coors = get_coors(lines)

file_name = os.path.splitext(gjf_file)[0] + '.xyz'
with open(file_name,'w') as new:
    new.write('%d\n' % len(coors))
    new.write(os.path.basename(gjf_file)+'\n')
    new.writelines(coors)

print(f'xyz_files is printed in {file_name}')      #available only after python 3.6
