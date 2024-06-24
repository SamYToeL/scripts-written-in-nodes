#!/usr/bin/env python3

import sys
import time
import re
import argparse



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

def frz_rel(namesp):
    gjf = namesp.gjfb
    fi = open(gjf,'r')
    filen = gjf.split('.')[0]
    lines = fi.readlines()
    ml,sl,ifc = gjfkeylines(lines)
    atomlines = lines[sl[1]+2:sl[2]]
    H_jud = 'H-[A-Z]'
    for i, line in enumerate(atomlines):
        
        if re.findall(H_jud,line) != []:
            #print(re.findall(H_jud,line))
            atomlines[i] = line.replace(' -1 ','  0 ')
        else:
            atomlines[i]  = line.replace(' 0 ',' -1 ')
    fw = open(filen + '_frz.gjf','w')
    fw.writelines(lines[:sl[1]+2])
    fw.writelines(atomlines)
    fw.writelines(lines[sl[2]:])
    print('frz_rel done')

def frz(namesp):
    gjf = namesp.gjfa
    fi = open(gjf,'r')
    filen = gjf.split('.')[0]
    lines = fi.readlines()
    ml,sl,ifc = gjfkeylines(lines)
    atomlines = lines[sl[1]+2:sl[2]]
    ele_jud = '[A-Z]-[A-Z]'
    for i, line in enumerate(atomlines):
        
        if re.findall(ele_jud,line) != []:
            #print(re.findall(H_jud,line))
            atomlines[i]  = line.replace(' 0 ',' -1 ')
        fw = open(filen + '_frz.gjf','w')
    fw.writelines(lines[:sl[1]+2])
    fw.writelines(atomlines)
    fw.writelines(lines[sl[2]:])
    print('frzdone')

parser = argparse.ArgumentParser(
    prog='freeze.py',
    description="This is a python script do help freeze all atoms or freeze only heavy atoms",
    usage='%(prog)s fzall or fzheavy .gjf '
)

subparsers = parser.add_subparsers(help="two functions: 'fzall'  and 'fzheavy'")

parser_fzall = subparsers.add_parser("fzall",help="freeze all atoms")
parser_fzall.add_argument("gjfa",type=str,help="Give the input gjf")
parser_fzall.set_defaults(func=frz)

parser_fzheavy = subparsers.add_parser("fzheavy",help="freeze heavy atoms other than Hydrogen")
parser_fzheavy.add_argument("gjfb",type=str,help="Give the input gjf")
parser_fzheavy.set_defaults(func=frz_rel)


if __name__ == '__main__' :
    s_t = time.time()
    args = parser.parse_args()
    args.func(args)

    
    e_t = time.time()
    elap = e_t - s_t
    print(f'Executed \n TIME: {elap} s')
    