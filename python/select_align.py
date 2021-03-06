#!/usr/bin/python
import pymol
import string

datafile1="/Users/caixiuhong/Dropbox/cai/btype_cco/hbonds_data/all_data/cytoscape/classification/PLS.dat"
datafile2="/Users/caixiuhong/Dropbox/cai/btype_cco/hbonds_data/all_data/cytoscape/classification/K-path.dat"
datafile3="/Users/caixiuhong/Dropbox/cai/btype_cco/hbonds_data/all_data/cytoscape/classification/P-exit.dat"
datafile4="/Users/caixiuhong/Dropbox/cai/btype_cco/hbonds_data/all_data/cytoscape/classification/unknown.dat"
#datafile5="/Users/caixiuhong/Dropbox/cai/btype_cco/hbonds_data/all_data/cytoscape/classification/cluster1.dat"
#datafile6="/Users/caixiuhong/Dropbox/cai/btype_cco/hbonds_data/all_data/cytoscape/classification/cluster2.dat"
f1=open(datafile1,"r")
f2=open(datafile2,"r")
f3=open(datafile3,"r")
f4=open(datafile4,"r")
#f5=open(datafile5,"r")
#f6=open(datafile6,"r")

def file_to_array(fname):
    array=[]
    f=open(fname,"r")
    for line in f:
        larray=line.split()
        array.append(larray[0])
    f.close()
    return array

ar1=file_to_array(datafile1)
ar2=file_to_array(datafile2)
ar3=file_to_array(datafile3)
ar4=file_to_array(datafile4)
#ar5=file_to_array(datafile5)
#ar6=file_to_array(datafile6)
s1=set([ar1[i] for i in xrange(len(ar1))])
s2=set([ar2[i] for i in xrange(len(ar2))])
s3=set([ar3[i] for i in xrange(len(ar3))])
s4=set([ar4[i] for i in xrange(len(ar4))])
#s6=s1.intersection(s2)
#s7=s1.intersection(s3)
#s8=s1.intersection(s4)
#s9=set([ar5[i] for i in xrange(len(ar5))])
#s10=set([ar6[i] for i in xrange(len(ar6))])
def creator(objname,setname,color):
    selection=""
    for res in setname:
        if (res=="PAAK9301" or res=="PDDK9302" or res=="PAAK9101" or res=="PDDK9102" or res=="HEM3K9300"):
            selection=selection+"resname HE3 and chain K  resname HEA and chain K "
        elif (res=="CUBK9500"):
            selection=selection+"name CU and resname CUB and chain K "
            if (objname=="BNCCnn" or  objname=="BNCnc"):
                cmd.show("spheres","name CU and resname CUB and chain K")
                if (objname=="BNCCnn"):
                    cmd.color("purple","name CU and resname CUB and chain K")
                if (objname=="BNCnc"):
                    cmd.color("pink","resi 1005 and chain A")
            
        else:
          resname=res[0:3]
          reschain=res[3]
          residn=res[4:]
          resid=int(residn)%10000
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
    cmd.color(color,objselection)

creator("PLS_ba3",s1,"yellow")
creator("K-path_ba3",s2,"blue")
creator("P-exit_ba3",s3,"grey")
creator("unknown_ba3",s4,"green")
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



