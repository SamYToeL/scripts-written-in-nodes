#!/usr/bin/env python3

import sys
from pathlib import Path

f1 = sys.argv[1]
f2 = sys.argv[2]

k=open(f1,'r')
j=open(f2,'r')
    
layer = k.readlines()
total = j.readlines()

tmp_array = []
lay_tmp = []
tot_tmp = []

for i in layer:
    tmp1 = i.split()
    if len(tmp1) > 1:
        lay_tmp.append(i.split())
        
    
for j in total:
    tmp2 = j.split()
    if len(tmp2) > 5:
        tot_tmp.append(j.split())

#print(tot_tmp[:7])
for i in lay_tmp:
    for label, j in enumerate(tot_tmp):
        if round(float(i[1]),6) == round(float(j[6]),6) and round(float(i[2]),6) == round(float(j[7]),6):
            tmp_array.append(str(j[1]))
print(','.join(tmp_array))

k.close()
j.close()
