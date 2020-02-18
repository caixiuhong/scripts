
import os, re
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime

def readenergytable(f)->dict:
	#read opp file and return dictionary
	ans={}
	with open(f) as f1:
		lines=f1.readlines()
		for line in lines:
			tmp=line.strip().split()
			res=tmp[1]
			ele=tmp[2]
			ans[res]=float(ele)
	return ans

def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    added_max='None' if not added else max(d1[i] for i in added)
    removed = d2_keys - d1_keys
    removed_max='None' if not removed else max(d2[i] for i in removed)
    modified = {o : (d1[o]-d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    same = set(o for o in intersect_keys if d1[o] == d2[o])
    return added, added_max, removed, removed_max, modified, same


def compare2files(f1, f2):
	f1_dict=readenergytable(f1)
	f2_dict=readenergytable(f2)

	added, added_max, removed, removed_max, modified, same = dict_compare(f1_dict, f2_dict)

	return added,added_max, removed, removed_max, modified, same





if __name__ == '__main__':
	if len(sys.argv) < 5:
		print("./compare2energies.py ENERGIES1 ENERGIES2 OUTPUTFILE HIST_FIG")
		sys.exit()
	else:
		ene1=sys.argv[1]
		ene2=sys.argv[2]
		output=sys.argv[3]
		hist_fig=sys.argv[4]

	#write output
	f_out=open(output, "a")

	#read files from ene1 and ene2

	ene2_files=[file for file in os.listdir(ene2) if os.path.isfile(os.path.join(ene2,file))]

	fileInEne1NotEne2=[]
	fileInEne2NotEne1=[]

	#statistics
	modified_list=[] # store all modified pairwise difference 
	added_max_list=[] # store all added pairwise max
	removed_max_list=[] # store all removed pairwise max

	for file in os.listdir(ene1):
		if file not in ene2_files:
			fileInEne1NotEne2.append(file)
			#print('%s exists in %s but not in %s.' % (file, ene1, ene2))
		else:
			ene1filepath=os.path.join(ene1,file)
			ene2filepath=os.path.join(ene2,file)
			ene2_files.remove(file)
			f_out.write("%s in %s compared to %s:" % (file, ene1, ene2))
			added, added_max, removed, removed_max, modified, same= compare2files(ene1filepath, ene2filepath)  #####MARK
			if added:
				f_out.write(','.join([i for i in added])+' exitst in %s but not in %s with maximum value %s.\n' % (ene1, ene2, str(added_max)))
				added_max_list.append(added_max)
			if removed:
				f_out.write(','.join([i for i in removed])+' exitst in %s but not in %s with maximum value %s.\n' % (ene1, ene2, str(removed_max)))
				removed_max_list.append(removed_max)
			if modified:
				for key in modified:
					f_out.write(' %s in %s differs one in %s by % f.\n' % (key, ene1, ene2, modified[key]))
					modified_list.append(modified[key])

			f_out.write('\n')

	f_out.write(','.join([i for i in fileInEne1NotEne2])+' exists in %s but not in %s.\n' % (ene1, ene2))
	if ene2_files:
		fileInEne2NotEne1=ene2_files[:]
		f_out.write(','.join([i for i in fileInEne2NotEne1])+' exists in %s but not in %s.\n' % (ene2, ene1))
		
	f_out.close()

	fig = plt.hist(modified_list,)
	plt.title('difference hist')
	plt.xlabel("difference")
	plt.ylabel("Frequency")
	plt.savefig(hist_fig)
	readme= open('README.txt', 'a')
	readme.write(str(datetime.datetime.now()))
	readme.write('\n')
	readme.write('Result on %s compared to %s: \n added max value: %s.\n removed max value: %s.\n modified see the histograme.\n'\
	 % (ene1filepath, ene2filepath, 'None' if not added_max_list else str(max(added_max_list)), \
	 	'None' if not removed_max_list else  str(max(removed_max_list))))

	numlarger015 = sum(1 for i in modified_list if i > 0.15)
	numsmal015 = sum(1 for i in modified_list if i < -0.15)
	readme.write('Modified min and max are %f and %f \n and %f numbers larger than 0.15 \n and %f numbers smaller than -0.15.\n'\
	 % (min(modified_list), max(modified_list), numlarger015, numsmal015))

	readme.close()
