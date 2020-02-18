import sys
import os
import numpy as np
import pandas as pd
import operator

###path: import categories to clusters
'''states=["f1","f2","f4"]'''
path = r"C:/Users/PC/Dropbox/cai/btype_cco/sequence/pls/"
''' change the path of list path '''
'''for state in states:'''

###import the hssp data want to search
state_sasa_files=[r"C:/Users/PC/Dropbox/cai/btype_cco/sequence/3s8f_hssp.txt"]
outputfile1=r'C:/Users/PC/Dropbox/cai/btype_cco/sequence/3s8f_pls.xlsx'
outputfile2=r'C:/Users/PC/Dropbox/cai/btype_cco/sequence/3s8f_pls_cons_res.xlsx'



AA_codes = { 'TYF':'Y','CYS': 'C', 'ASP' : 'D','SER':'S','GLN':'Q','LYS':'K','ILE':'I','PRO':'P','THR':'T','PHE':'F','ASN':'N','GLY':'G','HIS':'H','LEU':'L','ARG':'R','TRP':'W','ALA':'A','VAL':'V','GLU':'E','TYR':'Y','MET':'M'}

def populate_clusters(clusters,path):
	for k in clusters.keys():
		with open(path+k+'.dat', "r") as f:
			residues_in_k=[res.strip() for res in f.readlines()]
			for residue in residues_in_k:
				if residue[0:3] in AA_codes.keys():
					clusters[k].append(AA_codes[residue[0:3]]+residue[3:])
				else:
					clusters[k].append(residue)
	return clusters

def generate_hssp_data(res_list, res_hssp):
	resnums=[]
	for k in res_list:
		resname=k[:-5]
		reschain=k[-5]       #CORRESPONDS TO RESIDUE CHAIN NUMBER IN THE RESIDUE LIST
		residn=k[-4:]
		resid=int(residn)%10000
		##the key string to search in ress_hssp file
		resnumn=str(resid)+' '+str(reschain)+' '
		resnum=resnumn.rjust(7)
		resnums.append(resnum)
	
	hssp_data={}
	with open(res_hssp, "r") as f:
		lines=[l.rstrip() for l in f.readlines()]
		for l in lines:
			if l[-6:] == 'WEIGHT':
				hssp_data['test']=l[15:]
				hssp_data['test']=hssp_data['test'].strip().split()
			if l[6:13] in resnums:
				res_key = res_list[resnums.index(l[6:13])]
				if res_key not in res_list:
					print (hssp_data, res_key)
				else:
					hssp_data[res_key]=l[13:]
					hssp_data[res_key]=hssp_data[res_key].strip().split()
	return hssp_data


input_dir =path
if not os.path.isdir(input_dir):
		sys.exit("Input directory not found.")
else:
		cluster_files = [f[:-4]for f in os.listdir(input_dir)]
		cluster_dict={clust:[] for clust in cluster_files}
		cluster_dict = populate_clusters(cluster_dict, input_dir)




residue_list=[]
residue_hssp=[]
for cluster in cluster_dict:
		cluster_residues=cluster_dict[cluster]
		residue_list.extend(cluster_residues)
for index,state_sasa_files in enumerate(state_sasa_files):
	hssp_res=state_sasa_files
	residue_hssp.append(generate_hssp_data(residue_list, hssp_res))
writer=pd.ExcelWriter(outputfile1, engine='xlsxwriter')
column=residue_hssp[0]['test']
columns=['cluster','residue']
columns.extend(column)
states=["3s8f"]
sheets=[]
for index, state in enumerate(states):
	print ("Generating report for: ", state)
	state_residue_hssp=residue_hssp[index]
	table=[]
	for cluster in cluster_dict:
		if (cluster == 'water' or cluster == 'special'):
			continue
		cluster_residues=cluster_dict[cluster]
		for res in cluster_residues: 
			if res in ['HE3K9300', 'CUBK9500', 'PAAK9101', 'PDDK9102', 'PAAK9301', 'PDDK9302']:
				print ("No hssp data for:", res)
			else:
				res_hssp_data = [cluster, res]
				res_hssp_data.extend(state_residue_hssp[res])
				table.append(res_hssp_data)
	table=pd.DataFrame(table,columns=columns)
	table.to_excel(writer, sheet_name=state)
writer.save()


##output conserved residues

##criteria of conservation: need to satisfy these:
##1. conservation weight > 0.6
##2. amino acid that has largest probability to occur in the position is the same as in the protein.
amino_acid_list=['V','L','I','M','F','W','Y','G','A','P','S','T','C','H','R','K','Q','E','N','D']
##store residues' conservation at cons_dict
cons_dict={}
for res, hssp_detail in state_residue_hssp.items():
	##skip title line
	if (res=='test'):
		continue
	res_name=res[0]
	cons_values=hssp_detail[0:20]
	weight=hssp_detail[-1]
	max_index,max_value=max(enumerate(cons_values), key=operator.itemgetter(1))
	#check conditons
	if ( float(weight) >= 0.6 and amino_acid_list[max_index]==res_name):
		cons_dict[res]=[1, max_value, weight]
	else:
		cons_dict[res]=[0, max_value,weight]


writer=pd.ExcelWriter(outputfile2, engine='xlsxwriter')
column=['frequency','conservation weight']
columns=['cluster','residue']
columns.extend(column)
states=["3s8f"]
sheets=[]
for index, state in enumerate(states):
	print ("Generating conservation report for: ", state) 
	table2=[]
	for cluster in cluster_dict:
		if (cluster == 'water' or cluster == 'special'):
			continue
		cluster_residues=cluster_dict[cluster]
		for res in cluster_residues: 
			if res in ['HE3K9300', 'CUBK9500', 'PAAK9101', 'PDDK9102', 'PAAK9301', 'PDDK9302']:
				print ("No hssp data for:", res)
			else:
				##output conserved residues
				if (cons_dict[res][0]):
					cons_hssp_data=[cluster, res]
					cons_hssp_data.extend([cons_dict[res][1],cons_dict[res][2]])
					table2.append(cons_hssp_data)
	table=pd.DataFrame(table2,columns=columns)
	table.to_excel(writer, sheet_name=state)
writer.save()




