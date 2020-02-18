
# coding: utf-8

# In[1]:

import os, re
import sys
#import pandas as pd

#Classify residues in protein.pdb to polar, non_polar, charged, special, water categories.
#inputpathway of protein.pdb, outputpathway of output lists

inputpathway='/home/cai/ba3/xray/3S8F.pdb'
outputpathway='/home/cai/ba3/sequence/list/'


##categories defination
polar_list=['GLN', 'ASN','HIS','SER', 'THR','TYR','CYS','TRP']
charged_list=['ARG', 'LYS', 'ASP','GLU']
hydrophobic_list=['PHE', 'LEU', 'ILE', 'VAL','ALA', 'PRO', 'GLY','PRO', 'MET']
water_list=['HOH']

##read protein.pdb
##classfy each residue in protein.pdb to 'polar', 'charged' 'non-polar' 'special' categories.
with open(inputpathway,mode='r',encoding='utf-8') as f1:
    print("processing %s." % (str(f1)))
    lines=[l.split() for l in f1.readlines()]
    res_list=[]
    polar_res=[]
    charged_res=[]
    hydrophobic_res=[]
    water_res=[]
    special_res=[]
    res_set=set()
    for l in lines:
        title=l[0]
        ##test
        #print(l)

        if (len(l) == 12 and len(l[3]) <= 3 and (title == "ATOM" or title=="HETATM")):
            res_full=l[3].rjust(3,'_')+l[4]+l[5].zfill(4)
            if (res_full in res_set):
                continue 
            else:
                res_dict={}
                res_dict['resname']=l[3]
                res_dict['reschain']=l[4]
                res_dict['resid']=l[5]
                res_dict['full_name']=res_full
                if ((l[3]) in polar_list or l[3] in charged_list or l[3] in hydrophobic_list or l[3] in water_list):
                    if (l[3] in polar_list):
                        res_dict['role']='polar'
                        polar_res.append(res_dict)
                    elif (l[3] in charged_list):
                        res_dict['role']='charged'
                        charged_res.append(res_dict)
                    elif (l[3] in hydrophobic_list):
                        res_dict['role']='hydrophobic'
                        hydrophobic_res.append(res_dict)
                    elif (l[3] in water_list):
                        res_dict['role']='water'
                        water_res.append(res_dict)
                else:
                    res_dict['role']='special'
                    special_res.append(res_dict)
                res_list.append(res_dict)
                res_set.add(res_full)

##test
#print(res_list)
#print(polar_res)


##wrtie out the file of each category

with open(outputpathway+'polar.dat',mode='w',encoding='utf-8') as f2:
    for residue in polar_res:
        f2.write(residue['full_name'])
        f2.write('\n')

with open(outputpathway+'charged.dat',mode='w',encoding='utf-8') as f3:
    for residue in charged_res:
        f3.write(residue['full_name'])
        f3.write('\n')

with open(outputpathway+'hydrophobic.dat',mode='w',encoding='utf-8') as f4:
    for residue in hydrophobic_res:
        f4.write(residue['full_name'])
        f4.write('\n')

with open(outputpathway+'special.dat',mode='w',encoding='utf-8') as f5:
    for residue in special_res:
        f5.write(residue['full_name'])
        f5.write('\n')

with open(outputpathway+'water.dat',mode='w',encoding='utf-8') as f6:
    for residue in water_res:
        f6.write(residue['full_name'])
        f6.write('\n')


    




