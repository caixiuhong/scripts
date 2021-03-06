
# coding: utf-8

# In[1]:

import os, re, io
import numpy as np
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#import pandas as pd



#transfer amino acid from 3-letter to 1-letter code 
AA_codes = { 'TYF':'Y','CYS': 'C', 'ASP' : 'D','SER':'S','GLN':'Q','LYS':'K','ILE':'I','PRO':'P','THR':'T','PHE':'F',\
'ASN':'N','GLY':'G','HIS':'H','LEU':'L','ARG':'R','TRP':'W','ALA':'A','VAL':'V','GLU':'E','TYR':'Y','MET':'M'}


def populate_clusters(clusters,path):
    #attach residues to each cluster category.

    for k in clusters.keys():
        with open(path+k+'.dat', "r") as f:
            residues_in_k=[res.strip() for res in f.readlines()]
            for residue in residues_in_k:
                if residue[0:3] in AA_codes.keys():
                    clusters[k].append(AA_codes[residue[0:3]]+residue[3:])
                else:
                    clusters[k].append(residue)
    return clusters


def crg_dict(input_file, sub_dir):
#find out charge of residues at each clusters, input_file: sum_crg.out
        with open(input_file,mode='r') as in_file:
            lines=[l.split() for l in in_file.readlines()]
            crg_data_dict={}
            for l in lines[1:-4]:
                #print(l)
                if len(l)==2:
                    #print(l)
                    resn=l[0][0:3]
                    reschain=l[0][4]
                    resid=l[0][5:9]
                    #correct residue id in f2
                    if (sub_dir[0:2] == "f2" and  reschain == "A"):
                        resid=str(int(resid)+11)
                        resid=resid.rjust(4,'0')
                        #print resid


                    if resn in AA_codes.keys():
                        res=AA_codes[resn]+reschain+str(resid)
                    else:
                        res=resn+reschain+str(resid)

                    res_crg=float(l[1])
                    crg_data_dict[res]=res_crg
            return crg_data_dict


# inputpathway to search sum_crg.out, generate outfile at outputpathway
#inputpathway= ['/archive/cai/raw_data/md/rerun-step4', '/archive/cai/raw_data/md/rerun-f2', '/archive/cai/raw_data/md/f4-dep-cub',\
#'/archive/cai/more_trj/step4/F51', '/archive/cai/more_trj/oth_st/step4/F52','/archive/cai/more_trj/step4/F62',\
 #'/archive/cai/more_trj/step4/r41','/archive/cai/more_trj/oth_st/step4/r42',\
#'/archive/cai/more_trj/oth_st/step4/r51','/archive/cai/more_trj/oth_st/step4/r52','/archive/cai/more_trj/oth_st/step4/r62']

#inputpathway=['/archive/cai/ba3/more_md_str/step4/md_re/p2000', '/archive/cai/ba3/more_md_str/step4/md_re/p2012/', \
#'/archive/cai/ba3/more_md_str/step4/md_re/p1000', '/archive/cai/ba3/more_md_str/step4/md_re/p3012', '/archive/cai/ba3/xray/step4/3s8f_per_stdMC_2.5.1', '/archive/cai/ba3/xray/step4/3s8f_per_3.5']

#inputpathway=['/archive/cai/ba3/xray/step4/3eh3', '/archive/cai/ba3/xray/step4/3eh4', '/archive/cai/ba3/xray/step4/3eh5',\
#'/archive/cai/ba3/xray/step4/3s3a','/archive/cai/ba3/xray/step4/3s3b','/archive/cai/ba3/xray/step4/3s3c',\
#'/archive/cai/ba3/xray/step4/3s3d']

#create inputpathway lists and strucs list
#inputpathway=['/archive/cai/ba3/xray/step4/4gp4','/archive/cai/ba3/xray/step4/4gp5']
'''
str_ctrl="/archive/cai/ba3/more_md_str/quick_run/more_md_pdbs/quotefile/str.ctrl"
print str_ctrl
main_path="/archive/cai/ba3/more_md_str/quick_run/more_md_pdbs/step4"
inputpathway=[]
strucs=[]
with open(str_ctrl) as fp:
    lines=fp.readlines()
    #print lines
    for line in lines:
        #print line
        folder_name=line[0:-5]
        #print folder_name
        folder_path=main_path+'/'+folder_name
        inputpathway.append(folder_path)
        strucs.append(folder_name)
#print inputpathway 
#print strucs
'''

'''
inputpathway=['/archive/cai/ba3/xray/full_run/step4/no_wat/4gp4', '/archive/cai/ba3/xray/full_run/step4/no_wat/3eh5',\
'/archive/cai/ba3/xray/full_run/step4/3s3d', '/archive/cai/ba3/xray/full_run/step4/3eh5', \
'/archive/cai/ba3/xray/full_run/step4/no_wat/4gp5', '/archive/cai/ba3/xray/full_run/step4/no_wat/4gp5_2',\
'/archive/cai/ba3/xray/full_run/step4/no_wat/3eh4','/archive/cai/ba3/xray/full_run/step4/no_wat/3s8f',\
'/archive/cai/ba3/xray/full_run/step4/no_wat/3s8f_2',
'/archive/cai/ba3/xray/full_run/step4/3eh3', '/archive/cai/ba3/xray/full_run/step4/3eh4', \
'/archive/cai/ba3/xray/full_run/step4/3s3a', '/archive/cai/ba3/xray/full_run/step4/3s3b', \
'/archive/cai/ba3/xray/full_run/step4/3s3c', '/archive/cai/ba3/xray/full_run/step4/3s8f', \
'/archive/cai/ba3/xray/full_run/step4/4gp4', '/archive/cai/ba3/xray/full_run/step4/4gp5',\
'/archive/cai/ba3/more_md_str/full_run/step4/no_wat/p1000', '/archive/cai/ba3/more_md_str/full_run/step4/no_wat/p1025',\
'/archive/cai/ba3/more_md_str/full_run/step4/no_wat/p1050',
'/archive/cai/ba3/more_md_str/full_run/step4/no_wat/p2000','/archive/cai/ba3/more_md_str/full_run/step4/no_wat/p2012',\
'/archive/cai/ba3/more_md_str/full_run/step4/no_wat/p2025','/archive/cai/ba3/more_md_str/full_run/step4/no_wat/p2050',\
'/archive/cai/ba3/more_md_str/full_run/step4/no_wat/p3000','/archive/cai/ba3/more_md_str/full_run/step4/no_wat/p3012',\
'/archive/cai/ba3/more_md_str/full_run/step4/no_wat/p3025', '/archive/cai/ba3/more_md_str/full_run/step4/no_wat/p3037',\
'/archive/cai/ba3/more_md_str/full_run/step4/no_wat/p3050',\
'/archive/cai/ba3/more_md_str/full_run/step4/no_wat/p4000', '/archive/cai/ba3/more_md_str/full_run/step4/no_wat/p4025']
'''
inputpathway=["/archive/cai/ba3/more_md_str/quick_run/more_md_pdbs/step4/test/ppdro3_t_HHL_35ns", \
"/archive/cai/ba3/more_md_str/quick_run/more_md_pdbs/step4/test/ppdro3_t_HHL_44ns", \
"/archive/cai/ba3/more_md_str/quick_run/more_md_pdbs/step4/test/debug_test/ppdro3_t_HHL_35ns", \
"/archive/cai/ba3/more_md_str/quick_run/more_md_pdbs/step4/test/debug_test/ppdro3_t_HHL_44ns"]
outputpathway='/home/cai/Dropbox/cai/btype_cco/crg_data/quick_run/test'

#structure name
#strucs=['3eh3', '3eh4', '3eh5', '3s3a', '3s3b', '3s3c','3s3d']
#strucs=['4gp4','4gp5']
'''
strucs=['4gp4_nowat', '3eh5_nowat', '3s3d','3eh5', '4gp5_nowat','4gp5_nowat_2', '3eh4_nowat', '3s8f_nowat', '3s8f_nowat_2',\
'3eh3','3eh4','3s3a','3s3b','3s3c','3s8f','4gp4','4gp5', \
'p1000','p1025','p1050','p2000', 'p2012','p2025', 'p2050','p3000','p3012', 'p3025','p3037','p3050','p4000', 'p4025']
'''
strucs=["ppdro3_t_HHL_35ns_rerun", "ppdro3_t_HHL_44ns_rerun", "ppdro3_t_HHL_35ns_debug", "ppdro3_t_HHL_44ns_debug"]

##attach each cluster residues
path = "/home/cai/Dropbox/cai/btype_cco/hbonds_data/all_data/cytoscape/classification/cluster_lists/"
input_dir =path
if not os.path.isdir(input_dir):
        sys.exit("Input directory not found.")
else:
        cluster_files = [f[:-4]for f in os.listdir(input_dir)]
        cluster_dict={clust:[] for clust in cluster_files}
        cluster_dict = populate_clusters(cluster_dict, input_dir)


#states=["f1", "f2", "f4", 'f51','f52','f62','r41','r42','r51','r52','r62']
states=[ 'r3','r5','f1','f3','f5','o1','o3','o5','e1','e3','e5','r1']

state_snap_list=[]

state_data_dict={}
state_data_dict_detail=[]



for index, state in enumerate(strucs):
    print "Generating report for: ", state
    state_path=inputpathway[index]

    snap_list=[]

    for root,dirs,files in os.walk(state_path):
            for name in files:
                if name=="sum_crg.out":
                    cluster_crg_dict={}
                    headers=['state_snap']
                    crg_dicts={}
                    inputfilepath=os.path.join(root,name)
                    #print("processing %s." % (str(inputfilepath)))
                    subdirpath=os.path.dirname(inputfilepath)
                    filename, subdir_name=os.path.split(subdirpath)
                    subdir_name_new=state+'+'+subdir_name
                    crg_dicts=crg_dict(inputfilepath,subdir_name)
                    #print crg_dicts
                    cluster_res={}
                    cluster_res['state_snap']=subdir_name_new
                    for cluster in cluster_dict:
                        cluster_residues=cluster_dict[cluster]
                        cluster_res_list=[]
                        
                        for res in cluster_residues:
                            #print res
                            if res in crg_dicts.keys():
                                cluster_res_list.append(crg_dicts[res])
                                #if (state=='f2'):
                                #print subdir_name, cluster, res, crg_dicts[res]
                                cluster_res[res]=crg_dicts[res]
                                headers.append(res)
                        cluster_crg_dict[cluster]= np.sum(cluster_res_list)
                        
                    state_data_dict[subdir_name_new]=cluster_crg_dict
                    state_data_dict_detail.append(cluster_res)
                    snap_list.append(subdir_name_new)                
                    
    state_snap_list.append(snap_list)
#print state_data_dict_detail
#print headers

##write the csv file
f1=open(outputpathway+'/'+'crg_detail_ba3_fullrun.csv', 'w')
f1_writer=csv.DictWriter(f1, fieldnames=headers)
f1_writer.writeheader()

for d in state_data_dict_detail:
    f1_writer.writerow(d)
f1.close()

clusts=sorted ([cluster for cluster in cluster_dict])
print clusts
all_state_data_dict={}
snaps={}
sorted_snaps={}
for index, state in enumerate(strucs):
    new_snaps=[]
    for i in states:   
        new_snap=state+'+'+i  
        #print new_snap
        new_snaps.append(new_snap)
    sorted_snaps[state]=new_snaps   
    state_datas=[]
    snaps[state]=[snap for snap in state_snap_list[index]]
    #print sorted(snaps[state])
    for cluster in clusts:
        #print cluster
        state_data=[]
        for snap in sorted_snaps[state]:
            #print snap
            state_data.append(state_data_dict[snap][cluster])
            #print snap
        state_datas.append(state_data)
    all_state_data_dict[state]=state_datas

#print all_state_data_dict['f2']
'''
x=[]
ys=[]
for index,state in enumerate(states):
    x.append(index)
    y=np.mean(all_state_data_dict[state], axis=1)
    ys.append(y)
'''

'''
#print ys
for i in range(len(clusts)):
    if (clusts[i]=='BNC'):
        continue
    else:
        y_plot=[row[i] for row in ys]
        #print x,y_plot
        plt.xticks(x, states)
        plt.plot(x,y_plot,label=clusts[i])
        plt.legend()
        plt.title('Ave_Crg of Cluster VS states')
plt.savefig(outputpathway+'/'+"Ave_Crg_Clust_2.png")

plt.clf()
'''
#print all_state_data_dict
for index,state in enumerate(strucs):
    x_state=list(range(len(snaps[state])))
    #x_label=[snap[-2:] for snap in sorted(snaps[state])]
    x_label=states
    plt.xticks(x_state,x_label)
    for i in range(len(clusts)):
        if (clusts[i] != 'BNC' and clusts[i] != 'P-exit' and clusts[i] != 'unknown' ):
            #print clusts[i]
            y_state_plot=all_state_data_dict[state][i]
            plt.plot(x_state,y_state_plot,label=clusts[i], alpha=1)
            plt.legend()
            plt.title('crg vs states at struc '+state)
            plt.ylim(-5.0,2.0)
    plt.savefig(outputpathway+'/'+'Crg_State_'+state+'_ba3.png')
    plt.clf()
'''
#print all_state_data_dict
x_f1=list(range(len(snaps['f1'])))
plt.xticks(x_f1,sorted(snaps['f1']))
for i in range(len(clusts)):
    if (clusts[i] != 'BNC'):
        #print clusts[i]
        y_f1_plot=all_state_data_dict['f1'][i]
        plt.plot(x_f1,y_f1_plot,label=clusts[i])
        plt.legend()
        plt.title('crg vs snap at f1 state')
plt.savefig('Crg_Snap_f1.png')
'''

'''
x_sum=[]
ys_sum=[]
for index,state in enumerate(states):
    x_sum.append(index)
    y_sum=np.sum(all_state_data_dict[state], axis=1)
    ys_sum.append(y_sum)

#print ys_sum
for i in range(len(clusts)):
    if (clusts[i]=='BNC'):
        continue
    else:
        y_plot_sum=[row[i] for row in ys_sum]
        #print x_sum,y_plot_sum
        plt.xticks(x_sum, states)
        plt.plot(x_sum,y_plot_sum,label=clusts[i])
        plt.legend()
        plt.title('Sum_Crg of Cluster VS states')
plt.savefig("Sum_Crg_Clust.png")
'''


