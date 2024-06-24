#!/usr/bin/env python3

import os
import sys
import numpy as np
from pathlib import Path
import copy


def readxyz(fxyz):
    name, tfile=os.path.splitext(fxyz)
    fr = open(fxyz,"r")
    lines = fr.readlines()
    fr.close()
    natoms=int(lines[0])
    coords=getcoords(lines[2:natoms+2])
    
    return coords

def getcoords(lines):
    natoms=len(lines)
    coords=np.zeros((natoms,3),dtype=float)
    var=lines[0].split()
    if '.' in var[1]:
        # ele x y z
        for i, linestr in enumerate(lines):
            vartmp=linestr.split()

            coords[i][0]=round(float(vartmp[1]),6)
            coords[i][1]=round(float(vartmp[2]),6)
            coords[i][2]=round(float(vartmp[3]),6)
    else:
        # ele frez x y z
        for i, linestr in enumerate(lines):
            vartmp=linestr.split()

            coords[i][0]=float(vartmp[2])
            coords[i][1]=float(vartmp[3])
            coords[i][2]=float(vartmp[4])
    return coords

def linkmatrix(lines):
    linkm=np.zeros((len(lines),len(lines)), dtype=float)
    for i, linestr in enumerate(lines):
        var=linestr.split()
        if len(var) == 1:
            continue
        else:
            j=1
            while j < len(var):        
                linkm[i][int(var[j])-1]=float(var[j+1])
                linkm[int(var[j])-1][i]=float(var[j+1])
                j=j+2
    return linkm

def gjfkeylines(lines):
    spacelist=[]
    for i in range(len(lines)):
        #method lines
        if lines[i].startswith('#'):
            mline=i
        #empty lines
        if lines[i].isspace() :
            #repeat empty lines at the end of files
            if len(spacelist)> 1 and i==spacelist[-1]+1:
                break
            spacelist.append(i) 
    #if contains connectivity key word
    ifconn=False
    for linestr in lines[mline:spacelist[0]]:
        if 'geom=connectivity' in linestr:
            ifconn=True
    return mline, spacelist, ifconn

def get_coors(gjf):
    name, tfile=os.path.splitext(gjf)
    fr = open(gjf,"r")
    lines = fr.readlines()
    fr.close()

    ml, sl, b=gjfkeylines(lines)

    #method lines
    mlines=lines[ml:sl[0]]

    #atoms lines
    atomlines=lines[sl[1]+2:sl[2]]
    natoms=len(atomlines)
    coords=getcoords(atomlines)
    return atomlines, coords

def get_head_tail(gjf):
    name, tfile=os.path.splitext(gjf)
    fr = open(gjf,"r")
    lines = fr.readlines()
    fr.close()

    ml, sl, b=gjfkeylines(lines)

    #head
    head=lines[:sl[1]+2]
    tail=lines[sl[2]:]
    return head,tail

def pdb_coor(file):
    with open(file,'r') as pdb:
        lines = pdb.readlines()
        coor_lines = []
        for line in lines:
            if line.startswith(('ATOM','HETATM')) and len(line.split()) > 9:
                tmp =line.split()[6:9]
                tmp.insert(0,line.split()[0])
                coor_lines.append(' '.join(tmp))
        coors = getcoords(coor_lines)
    return coors

if __name__ == '__main__' :
    f1 = sys.argv[1]
    f2 = sys.argv[2]
    fnm = Path(f1)
    prefi = fnm.stem
    head, tail = get_head_tail(f1)
    atline, ori_coor = get_coors(f1)
    if f2.endswith('.gjf'):
        atline2, can_coor = get_coors(f2)    
    elif f2.endswith('.pdb'):
        can_coor = pdb_coor(f2)
    fw = open(prefi+'-CH.gjf','w')
    fw.writelines(head)    
    for i in range(len(ori_coor)):    
        tmp = atline[i].split()
        '''
        tmp[2] = str(round(can_coor[i][0],6))
        tmp[3] = str(round(can_coor[i][1],6))
        tmp[4] = str(round(can_coor[i][2],6))
        '''
        tmp[2] = round(can_coor[i][0],6)
        tmp[3] = round(can_coor[i][1],6)
        tmp[4] = round(can_coor[i][2],6)
        #atline[i] =f'{tmp[0]}   {tmp[1]}  {tmp[2]:6f}  {tmp[3]:6f}  {tmp[4]:6f} {tmp[5]}' 
        #if len(tmp) == 6:
        #    atline[i] = ' %-14s %-3s %-10.6f %-10.6f %-10.6f %s %s ' % (tmp[0],tmp[1],tmp[2],tmp[3],tmp[4],tmp[5],tmp[6])
        #else:
        atline[i] = ' %-14s %-3s %-10.6f %-10.6f %-10.6f %s' % (tmp[0],tmp[1],tmp[2],tmp[3],tmp[4],' '.join(tmp[5:]))
        
        fw.write(atline[i]+'\n')
    
    fw.writelines(tail)
                                                
   
        












