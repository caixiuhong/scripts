import os, re
import sys


def get_template(template_file):
	with open(template_file,mode='r',encoding='utf-8') as f1:
		lines=[l for l in f1.readlines()]
		node_cord={}
		for i in range(len(lines)):
			if '<node id' in lines[i]:	
				label=(lines[i]).split()[2][7:-1]
				node_cord[label]=lines[i+1]
	return node_cord
		

def re_cord_input(in_file, out_file, template_file):
	template_inf=get_template(template_file)
	#print(template_inf)
	with open(in_file,mode='r',encoding='utf-8') as f1:
		with open(out_file,mode='w',encoding='utf-8') as f2:
			lines=[l for l in f1.readlines()]
			#print(lines)
			node_cord={}
			i=0
			while (i < len(lines)):
				f2.write(lines[i])
				if '<node id' in lines[i]:	
					label=(lines[i]).split()[2][7:-1]
					if label in template_inf.keys():
						f2.write(template_inf[label])
						i=i+1
				i=i+1
	return 
		


#template='/home/cai/cytoxyz/template'
#inputfile='/home/cai/cytoxyz/10231-10502-f2_inter_ft.xgmml'
#outputfile='/home/cai/cytoxyz/10231-10502-f2_inter_ft.xgmml_test'

#print(sys.argv) # prints command
if (len(sys.argv)!=4):
    print("Usage: python3 cyto.py input template output\n")
    sys.exit()


if(re_cord_input(sys.argv[1], sys.argv[3], sys.argv[2])):
	print("Error.")
else:
	print("Done")
