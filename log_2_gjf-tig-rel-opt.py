#!/usr/bin/env python3
#This script is to take out all the strcutures in the log file generalized during the process of relaxed scan and transcribe it into separate gjf file
#The principle of finding the structure is that The opt structure of each step must be followed with a not opt structure
###optimziede for relax-scan and opt but not for "opt=newdefinition"

#Sam Liao
#2023.12.6

import sys
import Strain_energy as st
import os

log_file = sys.argv[1]
gjf_file = sys.argv[2]
if len(sys.argv) == 4:
    if sys.argv[3] == 's' :
    #scan mode start
        f = open(log_file, "r")
        lines = f.readlines()
        f.close()
        n = open('scan_E_'+log_file,"w")
        for line in lines:
            if line.startswith(' SCF Done'):
                E = line.split()[3]
                n.write(E,'\n')
        print("Scan task Energy is printed out to 'scan_E' log, please check")
else:
    #other task    
    f = open(log_file, "r")
    lines = f.readlines()
    f.close()

    g = open(gjf_file,'r')
    gjf_lines = g.readlines()
    g.close()
    ml, sl, ifconn = st.gjfkeylines(gjf_lines)
    spin_line = gjf_lines[sl[1]+1]
    method = gjf_lines[ml:sl[0]]
    method = ''.join(method)
    method = method.replace('opt=modredundant', '')
    if ifconn:
        conn_line = gjf_lines[sl[2]+1:]

    '''
    def key_judger(row):
        for lintp in lines[row-10:row]:
            if lintp.startswith(" Lowest energy"):
                return True
        return False
        '''
    def multi_opt(lines,point,sym):
        key_lines = []
        if len(point) == 1:
            ltmp = lines[:point[-1]]
            ltmp.reverse()
            for j, line in enumerate(ltmp):
                if sym :
                    if "Standard orientation" in line:
                        key_lines.append(point[-1]-j-1)              #在底下加的情况下，从point【-2】开始算，0的情况已经被包含在内了，就不用多一个1
                        break
                else:
                    if  "Input orientation" in line:
                        key_lines.append(point[-1]-j-1)
                        break
        else:        
            for j, line in enumerate(lines[point[-2]:point[-1]]):
                    if sym :
                        if "Standard orientation" in line:
                            key_lines.append(j+point[-2])
                    else:
                        if  "Input orientation" in line:
                            key_lines.append(j+point[-2])
        return key_lines

    def sing_opt(lines,opt_point,sym):
        key_lines=[]
        for i in range(len(opt_point)-1):
                if i == 0:
                    for j, line in enumerate(lines[:opt_point[i]]):
                        if sym :
                            if "Standard orientation" in line:
                                key_lines.append(j)
                        else:
                            if  "Input orientation" in line:
                                key_lines.append(j)
                for j, line in enumerate(lines[opt_point[i]:opt_point[i+1]]):
                        if sym :
                            if "Standard orientation" in line:
                                key_lines.append(j+opt_point[i])
                        else:
                            if  "Input orientation" in line:
                                key_lines.append(j+opt_point[i])
        
        return key_lines


    def get_steplines(lines,method):
        scan_index = [[]]
        opt_point = []
        scan_point = 1
        key_lines = []
        for i,line in enumerate(lines):
            if line.startswith(" Step number "):
                if "scan point" in line:
                    Task = 'relax scan'
                    if int(line.split()[-4]) == scan_point:
                        scan_index[-1].append(i)
                    else:
                        scan_index.append([])
                        scan_point += 1
                        scan_index[-1].append(i)
                else:
                    Task = 'opt'
                    opt_point.append(i)       
        if 'nosymm' in method:
            sym = False
        else:
            sym = True
        
        if Task == 'scan':
            for point in scan_index:
                key_lines += multi_opt(lines,point,sym)
        else:
            print(opt_point)
            key_lines += sing_opt(lines,opt_point,sym)
            
                    
        
        return key_lines

                
    elelist = []
    for tmp in gjf_lines[sl[1]+2:sl[2]]:
        elelist.append(tmp.split()[0])

    '''
    for row , line in enumerate(lines):
        if "Center     Atomic      Atomic             Coordinates (Angstroms)" in line:
            key_candidate.append(row)
    '''

    atom_num = sl[2]-sl[1]-2
    key_lines = get_steplines(lines,method)
    #keylines searching is over
    #Next step is the gjfs' generation
    gjfname = log_file.split(".")[0]
    filelist = []
    for i in range(len(key_lines)):
        fw = open(gjfname+ "_" +str(i+1)+'.gjf', 'w')
        fw.write("%chk=" + gjfname + "_" +str(i+1) + ".chk\n")
        fw.write("%nprocshared=4\n")
        fw.write("%mem=4GB\n")
        fw.write(method)
        fw.write('\n')
        fw.write(gjfname + "_" +str(i+1)+'\n')
        fw.write('\n')
        fw.write(spin_line)
        j=0
        for coor in lines[key_lines[i]+5:key_lines[i]+5+atom_num]:
            linetmp = [float(var) for var in coor.split()[3:]]
            fw.write('%-16s%14.8f%14.8f%14.8f \n' % (elelist[j],linetmp[0],linetmp[1],linetmp[2]))
            j+=1
        fw.write('\n')
        if ifconn:
            fw.writelines(conn_line)
        fw.close()
        filelist.append(gjfname+ "_" +str(i+1)+'.gjf\n')

    c = open('filelist.dat','w')
    c.writelines(filelist)
    c.close()




    

        
            
            
