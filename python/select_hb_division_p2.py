#!/usr/bin/python
import pymol
import string

#parameter setting
file_names=['k-path', 'midd', 'N-surf', 'p-exit1', 'p-exit2','p-exit-prime', 'pls', 'pls2']
file_main_path=r'C:\Users\PC\Dropbox\cai\btype_cco\hbonds_data\more_md_str_hb\cytoscape\classification\classification'


def file_to_array(fname):
    array=[]
    f=open(fname,"r")
    for line in f:
        larray=line.split()
        array.append(larray[0])
    f.close()
    return array

def creator(objname,setname,color):
    selection=""


    for res in setname:
        res=res.split(':')
        reschain=res[0]
        resid=res[1]
        resname=res[3]

        if (resname=="PRA" or resname=="PRD" or resname=="FA3" or resname=="HAS" or resname=="CU"):
            continue

        #elif (res=="CUBK9500"):
        #    selection=selection+"name CU and resname CUB and chain K "
        #    if (objname=="BNCCnn" or  objname=="BNCnc"):
        #        cmd.show("spheres","name CU and resname CUB and chain K")
        #        if (objname=="BNCCnn"):
        #            cmd.color("purple","name CU and resname CUB and chain K")
        #        if (objname=="BNCnc"):
        #            cmd.color("pink","resi 1005 and chain A")
            
        else:
          selection=selection+"resid "+str(resid)+" and"+" chain "+reschain+" and"+" resn "+resname+ " "
    
    ##select protein (object) wanted to select
    selection=selection+" and 3s8f"

    cmd.select("residues",selection)
    cmd.create(objname,"residues")
    objselection=objname
    # if (objname=="BNC"):
    #     cmd.show("sticks",objselection)
    # else:
    #     cmd.show("surface",objselection)
    cmd.show("sticks",objselection)
    cmd.show("mesh",objselection)
    cmd.color(color,objselection)




datafile=[]
ars=[]
colors=['yellow', 'blue', 'cyan', 'green', 'orange','magenta', 'red', 'wheat', 'grey']

for i in range(len(file_names)):
    file_path=file_main_path + '/'+file_names[i]+'.txt'
    ars.append(file_to_array(file_path))

ss=[]
for ar in ars:
    ss.append(set(ar))

for i in range(len(file_names)):
    creator(file_names[i], ss[i], colors[i])




#creator("cluster1",s9,"gray")
#creator("cluster2",s10,"gray")
#cmd.set("cartoon_cylindrical_helices",1)
# cmd.cartoon("tube","1:49")
# cmd.cartoon("arrow","50:99")
# cmd.cartoon("loop","100:149")
# cmd.cartoon("oval","150:199")
# cmd.cartoon("rect","200:250")
# cmd.set("cartoon_flat_sheets",0)
# cmd.set("cartoon_smooth_loops",1)
# cmd.set("cartoon_transparency",0.75)
#cmd.set("stick_radius",0.5,"cons_res")
# cmd.show("cartoon","protein")
#cmd.select("Waters","resname HOH within 5 of BNCCnn resname HOH within 5 of PLSCnn resname HOH within 5 of DchannelCnn resname HOH within 5 of outsideCnn")
#cmd.create("Waters","Waters")
#cmd.show("spheres","Waters")
#cmd.color("skyblue","Waters")
#cmd.set("sphere_transparency",0.2,"Waters")



