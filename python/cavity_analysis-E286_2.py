import sys
import os
import numpy as np
import pandas as pd
AA_codes = { 'C':'CYS', 'D':'ASP','S':'SER','Q':'GLN','K':'LYS','I':'ILE','P':'PRO','T':'THR','F':'PHE','N':'ASN','G':'GLY','H':'HIS','L':'LEU','R':'ARG','W':'TRP','A':'ALA','V':'VAL','E':'GLU','Y':'TYR','M':'MET', 'HEM3':'HE3', 'CUB':'CUB','PAA':'PAA','PDD':'PDD'}

def populate_clusters(clusters,path):
	'''Transfer one code to three code '''
	for k in clusters.keys():
		with open(path+k+".dat", "r") as f:
			residues_in_k=[res.strip() for res in f.readlines()]
			for residue in residues_in_k:
				if residue[0:3] in AA_codes.keys():
					clusters[k].append(residue)
				elif residue[0:4] in AA_codes.keys():
					clusters[k].append(AA_codes[residue[0:4]]+residue[4:])
				else:
					clusters[k].append(AA_codes[residue[0:1]]+residue[1:])
	return clusters

'''states=["f1","f2","f4"]'''
path = "C:\Users\PC\Dropbox\cai\more_trj_aa3\\new-list\\"
''' change the pathway of list path '''
'''for state in states:'''
input_dir =path
if not os.path.isdir(input_dir):
		sys.exit("Input directory not found.")
else:
		cluster_files = [f[:-4]for f in os.listdir(input_dir)]
		cluster_dict={clust:[] for clust in cluster_files}
		cluster_dict = populate_clusters(cluster_dict, input_dir)
		
def generate_cavity_data(path_list, path_file):
	"""Returns water cavities in cco.

	Parameters
	----------
	path_list : dictionary
		A dictionary of clusters, where each key is cluster and values
		are residues in that cluster.
	path_file: string
		Filename for a data file containing water medicated h-bonds.

	Returns
	-------
	water_path : dictionary
		A dictionary whose keys are snapshot numbers and values are water cavities
	"""
	water_path={}
	water_least_num={}
	for i in range(1, 13):
		water_path[i] = [set({}), set({}), set({}), set({}),set({}), set({}), set({}), set({}),set({}), set({}), set({}), set({})]
		water_least_num[i] = [6,6,6,6,6,6,6,6,6,6,6,6]
	with open(path_file, "r") as f:
		lines=[l.replace(',','').split() for l in f.readlines()]
		i=0
		for l in lines:
			if "processing..." in l:
				i=i+1
			# begin iterating over paths
			if "GET:" in l:
				if l[1] in path_list['BNC'] or l[-1] in path_list['BNC']:
					if l[1] in path_list['PLS'] or l[-1] in path_list['PLS']:
						# begin iterating over residues in that path
						if water_least_num[i][0] > len(l[2:-1]):
							water_least_num[i][0]=len(l[2:-1])
						for j in range(len(l[2:-1])):
							water_path[i][0].add(l[2+j])				
					elif l[1] == 'GLUA0286' or l[-1] == 'GLUA0286':
						
						if water_least_num[i][1] > len(l[2:-1]):
							water_least_num[i][1]=len(l[2:-1])
						for j in range(len(l[2:-1])):
							water_path[i][1].add(l[2+j])
				elif l[1]=='GLUA0286' or l[-1]=='GLUA0286':
					if l[1] in path_list['PLS'] or l[-1] in path_list['PLS']:
						
						if water_least_num[i][2] > len(l[2:-1]):
							water_least_num[i][2]=len(l[2:-1])
						for j in range(len(l[2:-1])):
							water_path[i][2].add(l[2+j])
					elif ( l[1] in path_list['D-channel'] and l[1] != 'GLUA0286' ) or ( l[-1] in path_list['D-channel'] and l[-1] != 'GLUA0286' ):
						
						if water_least_num[i][10] > len(l[2:-1]):
							water_least_num[i][10]=len(l[2:-1])
						for j in range(len(l[2:-1])):
							water_path[i][10].add(l[2+j])
				elif l[1] in path_list['PLS'] or l[-1] in path_list['PLS']:
					if l[1] in path_list['external'] or l[-1] in path_list['external']:
						#print len(l[2:-1]), water_least_num, i
						if water_least_num[i][3] > len(l[2:-1]):
							water_least_num[i][3]=len(l[2:-1])

						for j in range(len(l[2:-1])):
							water_path[i][3].add(l[2+j])
					if l[1] in path_list['cluster1'] or l[-1] in path_list['cluster1']:
						
						if water_least_num[i][4] > len(l[2:-1]):
							water_least_num[i][4]=len(l[2:-1])

						for j in range(len(l[2:-1])):
							water_path[i][4].add(l[2+j])
					if l[1] in path_list['cluster2'] or l[-1] in path_list['cluster2']:
						
						if water_least_num[i][5] > len(l[2:-1]):
							water_least_num[i][5]=len(l[2:-1])

						for j in range(len(l[2:-1])):
							water_path[i][5].add(l[2+j])
				elif l[1] in path_list['PLS-add'] or l[-1] in path_list['PLS-add']:
					if l[1] in path_list['external'] or l[-1] in path_list['external']:
						
						if water_least_num[i][6] > len(l[2:-1]):
							water_least_num[i][6]=len(l[2:-1])

						for j in range(len(l[2:-1])):
							water_path[i][6].add(l[2+j])
					if l[1] in path_list['cluster1'] or l[-1] in path_list['cluster1']:
						
						if water_least_num[i][7] > len(l[2:-1]):
							water_least_num[i][7]=len(l[2:-1])

						for j in range(len(l[2:-1])):
							water_path[i][7].add(l[2+j])
					if l[1] in path_list['cluster2'] or l[-1] in path_list['cluster2']:
						
						if water_least_num[i][8] > len(l[2:-1]):
							water_least_num[i][8]=len(l[2:-1])

						for j in range(len(l[2:-1])):
							water_path[i][8].add(l[2+j])
				elif l[1] in path_list['cluster1'] or l[-1] in path_list['cluster1']:
					if l[1] in path_list['cluster2'] or l[-1] in path_list['cluster2']:
						
						if water_least_num[i][9] > len(l[2:-1]):
							water_least_num[i][9]=len(l[2:-1])

						for j in range(len(l[2:-1])):
							water_path[i][9].add(l[2+j])
					if l[1] in path_list['external-add'] or l[-1] in path_list['external-add']:
						
						if water_least_num[i][11] > len(l[2:-1]):
							water_least_num[i][11]=len(l[2:-1])

						for j in range(len(l[2:-1])):
							water_path[i][11].add(l[2+j])


	'''correct initial assignment for water_least_num'''
	for k in range(1, i+1):
		for j in range(12):
			if water_least_num[k][j]==6:
				water_least_num[k][j]='N'
	
	return i, water_path, water_least_num

state_path_files=["C:\Users\PC\Dropbox\cai\more_trj_aa3\water_alys\\0w_allres\F51_out_path.txt", "C:\Users\PC\Dropbox\cai\more_trj_aa3\water_alys\\0w_allres\F52_out_path.txt", \
 "C:\Users\PC\Dropbox\cai\more_trj_aa3\water_alys\\0w_allres\F62_out_path.txt", "C:\Users\PC\Dropbox\cai\more_trj_aa3\water_alys\\0w_allres\\r41_out_path.txt", \
 "C:\Users\PC\Dropbox\cai\more_trj_aa3\water_alys\\0w_allres\\r42_out_path.txt", "C:\Users\PC\Dropbox\cai\more_trj_aa3\water_alys\\0w_allres\\r51_out_path.txt", \
 "C:\Users\PC\Dropbox\cai\more_trj_aa3\water_alys\\0w_allres\\r52_out_path.txt", "C:\Users\PC\Dropbox\cai\more_trj_aa3\water_alys\\0w_allres\\r62_out_path.txt"]

cavity_data=[]
cavity_num=[]
snap_nums=[]
'''
for cluster in cluster_dict:
		cluster_residues=cluster_dict[cluster]
		residue_list.extend(cluster_residues)
'''
for index,state_path_files in enumerate(state_path_files):
	snap_num, water_paths, water_least_nums=generate_cavity_data(cluster_dict,state_path_files)
	cavity_data.append(water_paths)
	cavity_num.append(water_least_nums)
	snap_nums.append(snap_num)
	

writer=pd.ExcelWriter('C:\Users\PC\Dropbox\cai\more_trj_aa3\water_alys\water_path_0w_allres.xlsx', engine='xlsxwriter')
columns=['snapshot','D>E286','min_wat D>E286','E286>BNC', 'min_wat E286>BNC', 'insec D>E286 & E286>BNC',\
 'insec E286>PLS & PLS>PE', 'E286>PLS','min_wat E286>PLS','BNC>PLS','min_wat BNC>PLS','PLS>PE', 'min_wat PLS>PE','PLS>C1','min_wat PLS>C1',\
  'PLS>C2', 'min_wat PLS>C2', 'PLS\'>PE','min_wat PLS\'>PE','PLS\'>C1', 'min_wat PLS\'>C1', 'PLS\'>C2',\
   'min_wat PLS\'>C2','C1>C2', 'min_wat C1>C2', 'C1>PE\'', 'min_wat C1>PE\'']
states=["F51","F52","F62","r41","r42","r51",'r52', "r62"]
sheets=[]
for index, state in enumerate(states):
	print "Generating report for: ", state
	state_cavity_data=cavity_data[index]
	state_cavity_num=cavity_num[index]
	state_snap_num=snap_nums[index]
	table=[]
	for i in range(1,state_snap_num+1):
		table.append([i,list(state_cavity_data[i][10]), state_cavity_num[i][10], list(state_cavity_data[i][1]), \
			state_cavity_num[i][1], list(state_cavity_data[i][10].intersection(state_cavity_data[i][1])), \
			list(state_cavity_data[i][2].intersection(state_cavity_data[i][3])),list(state_cavity_data[i][2]), \
			state_cavity_num[i][2],list(state_cavity_data[i][0]), state_cavity_num[i][0],list(state_cavity_data[i][3]),\
			 state_cavity_num[i][3],list(state_cavity_data[i][4]), state_cavity_num[i][4], list(state_cavity_data[i][5]),\
			 state_cavity_num[i][5],list(state_cavity_data[i][6]),state_cavity_num[i][6],list(state_cavity_data[i][7]),\
			 state_cavity_num[i][7],list(state_cavity_data[i][8]),state_cavity_num[i][8],list(state_cavity_data[i][9]),\
			 state_cavity_num[i][9], list(state_cavity_data[i][11]), state_cavity_num[i][11]])
	table=pd.DataFrame(table,columns=columns)
	table.to_excel(writer, sheet_name=state)
writer.save()
