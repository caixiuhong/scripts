import os, re
def water_mc(input_file, output_file):
	with open(output_file,mode='w',encoding='utf-8') as out_file:
		with open(input_file,mode='r',encoding='utf-8') as in_file:
			lines=[l.split() for l in in_file.readlines()]
			res_set=set()
			for l in lines:
				if 'HOH+1' in l[0] and float(l[1]) > 0.0:
					resn=l[0][0:3]
					resid=l[0][5:10]
					res=resn+resid
					res_set.add(res)
					outputstr=l[0]+'  '+l[1]+'\n'
					out_file.write(outputstr)
			return res_set
		

inputpathway='/Users/PC/Dropbox/hbonds/data20160926/water-cavity/water_analysis/water_MC/inputdir'
outputpathway='/Users/PC/Dropbox/hbonds/data20160926/water-cavity/water_analysis/water_MC/h3o_occ_dir'
mainpathway='/Users/PC/Dropbox/hbonds/data20160926/water-cavity/water_analysis/water_MC/'

with open(mainpathway+'h3o_occ', mode='w', encoding='utf-8') as wat_file:
	h3o_dict={}
	for root,dirs,files in os.walk(inputpathway):
		for subdir in dirs:
			subdirpath=os.path.join(root,subdir)
			outputsubdir=re.sub(inputpathway,outputpathway,subdirpath) 
			os.mkdir(outputsubdir)
		for name in files:
			snap=name[-4:]
			print(snap)
			inputfilepath=os.path.join(root,name)
			outputfilepath_1=re.sub(inputpathway,outputpathway,inputfilepath)
			outputfilepath=re.sub('fort.38','h3o.occ',outputfilepath_1)
			print("creating %s." % (str(outputfilepath)))
			h3o_dict[snap]=water_mc(inputfilepath,outputfilepath)
			if h3o_dict[snap]:
				outstr=snap+'  '+ str(h3o_dict[snap])+'\n'
			else:
				outstr=snap+'  '+'NULL' +'\n'
			wat_file.write(outstr)




