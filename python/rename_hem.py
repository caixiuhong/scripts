#!/usr/bin/python
import os, re, sys

def rename_hem_atom(line):
	ori_hem_atom = ['O1A', 'O2A', 'CGA', 'CBA', 'CAA', 'O2D', 'O1D', 'CGD', 'CBD', 'CAD', 'CMA', 'C3A', 'C2A', 'C1A', 'CHA', 'C4D', 'C3D', 'C2D', 'CMD', 'OMD', 'C4A', 'NA', 'ND', 'C1D']
	new_hem_atom = ['O1D', 'O2D', 'CGD', 'CBD', 'CAD', 'O2A', 'O1A', 'CGA', 'CBA', 'CAA', 'CMD', 'C2D', 'C3D', 'C4D', 'CHA', 'C1A', 'C2A', 'C3A', 'CMA', 'OMA', 'C1D', 'ND', 'NA', 'C4A']
	words = line.split()
	for index, atom in enumerate(ori_hem_atom):
		if atom in words:
			new_line = re.sub(atom, new_hem_atom[index], line)
			break
		else: 
			new_line = line
	return new_line



if __name__ == '__main__':
	if len(sys.argv) < 3 :
		print "rename_hem input_file output_file"
		sys.exit(0)
	else:
		input_file = sys.argv[1]
		output_file = sys.argv[2]


	#read pdb file
	with open(output_file,mode='w') as out_file:
		with open(input_file,mode='r') as in_file:
			all_line = in_file.readlines()
			hem_res_name = 'HAS'
			for line in all_line:
				if 'HAS' in line:
					new_line=rename_hem_atom(line)
				else: 
					new_line=line
				out_file.write(new_line)
