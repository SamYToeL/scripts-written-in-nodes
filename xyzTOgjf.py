#!/usr/bin/env python3
import os
import Strain_energy as st
import sys



def check_spin(gjf):
    fr = open(gjf,'r')
    lines = fr.readlines()
    fr.close()
    if len(lines[0].split()) != 4:
        lines = lines[2:]
    eles, coords = st.getcoords(lines)
    total_e = sum(st.eleslist.index(ele) for ele in eles)
    if total_e % 2 != 0:
        return 2
    else:
        return 1  
    



def xyz2gjf(xyzname,spin,ncpu,mem,ml):
    chkname = os.path.splitext(xyzname)[0]
    fw = open(xyzname,'r')
    coordlines = fw.readlines()
    fw.close()
    if len(coordlines[0].split()) != 4:
        coordlines = coordlines[2:]
    with open(chkname+'.gjf','w') as fl:
        fl.write('%chk='+chkname+'.chk\n%nprocshared='+ncpu+'\n%mem='+mem+'GB\n')
        fl.write('#'+ml+'\n\ntitle card\n\n')
        fl.write('0 %d\n' % spin)            #临时改成1 1 
        fl.writelines(coordlines)
        fl.writelines('\n')
    
        
xyzfile = sys.argv[1]
ncpu=sys.argv[2]
mem=sys.argv[3]
ml = sys.argv[4]
spin=check_spin(xyzfile)
xyz2gjf(xyzfile,spin,ncpu,mem,ml)


