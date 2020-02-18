
#!/usr/bin/python
import sys
import string
#import re
from mfe_adv import *

class MSRECORD:
   def __init__(self):
      self.counter = []


conformers=[]
grouped_ms_states=[]
ms_states=[]

def read_re_ms():
	global ms_states
	lines = read_file_respect_comments("re_ms.dat")
	del lines[:2]   # remove the two lines
	if len(ms_states) > 0:
		print "WARNING: adding to non empty microstate list."

	#read head3.lst to read charges for each conformer
	read_headlst()


	for i in range(0, len(lines), 3):
		ms_state =MSRECORD()
		confid_list = lines[i].split()
		energies = lines[i+1].split()
		avenergies = lines[i+2].split()
#		print energies
#		print avenergies
#		print confid_list
		ms_state.confseq = confid_list
		ms_state.cumE = float(energies[2])
		ms_state.cumE2 = float(energies[5])
		ms_state.counter = int(energies[-1])
		ms_state.E = float(avenergies[-1])
		ms_state.id = i
		#assign charge state for the microstate
		ms_state.crg = 0
		for index in ms_state.confseq:
			ms_state.crg += conformers[int(index)].crg
			confid = conformers[int(index)].id
			ms_state.confidseq.append(confid)
		ms_states.append(ms_state)
	return

def group_ms():
	global grouped_ms_states
	if len(ms_states) < 1:
		print "WARNING: no microstate to evaluate."
		return     # no microstates

	#acumulate the duplicated microstte, dulicated microstate judging standard: same ms_state.confseq
	seen_ms_state=[]
	for ms_state in ms_states:
		seen_confseq_list = [ ms_state.confseq for ms_state in seen_ms_state]
		if ms_state.confseq in seen_confseq_list:
			seen_index = seen_confseq_list.index(ms_state.confseq)
			seen_ms_state[seen_index].cumE += ms_state.cumE
			seen_ms_state[seen_index].cumE2 += ms_state.cumE2
			seen_ms_state[seen_index].counter += ms_state.counter
			seen_ms_state[seen_index].E = seen_ms_state[seen_index].cumE/seen_ms_state[seen_index].counter
		else:
			seen_ms_state.append(ms_state)
	grouped_ms_states = seen_ms_state
	return


if __name__ == '__main__':
	
	#read head list
	read_re_ms()

	#group same microstates together
	group_ms()

	print "MS_id    Microstate    Tot_Crg   Ave_E(Kcal)  Counter"
	print "----------------------------------------------"
	for ms_state in grouped_ms_states:
		print "Conf_seq_num: "+ms_state.confseq
		print "conf_seq_id: "+ms_state.confidseq
		print "Charge: "+ms_state.crg
		print "Ave_E: "+ms_state.E
		print "Counter: "+ms_state.counter
		print  "\n"
'''
   print "vdw1     %8.2f%8.2f%8.2f" % (dG_point.vdw1/ph2Kcal, dG_point.vdw1/mev2Kcal, dG_point.vdw1)
   print "tors     %8.2f%8.2f%8.2f" % (dG_point.tors/ph2Kcal, dG_point.tors/mev2Kcal, dG_point.tors)
   print "ebkb     %8.2f%8.2f%8.2f" % (dG_point.epol/ph2Kcal, dG_point.epol/mev2Kcal, dG_point.epol)
   print "dsol     %8.2f%8.2f%8.2f" % (dG_point.dsolv/ph2Kcal, dG_point.dsolv/mev2Kcal, dG_point.dsolv)
   print "offset   %8.2f%8.2f%8.2f" % (dG_point.extra/ph2Kcal, dG_point.extra/mev2Kcal, dG_point.extra)
   print "pH&pK0   %8.2f%8.2f%8.2f" % (dG_point.pHeffect/ph2Kcal, dG_point.pHeffect/mev2Kcal, dG_point.pHeffect)
   print "Eh&Em0   %8.2f%8.2f%8.2f" % (dG_point.Eheffect/ph2Kcal, dG_point.Eheffect/mev2Kcal, dG_point.Eheffect)
   print "-TS      %8.2f%8.2f%8.2f" % (-dG_point.TS/ph2Kcal, -dG_point.TS/mev2Kcal, -dG_point.TS)
   print "residues %8.2f%8.2f%8.2f" % (dG_point.mfe_total/ph2Kcal, dG_point.mfe_total/mev2Kcal, dG_point.mfe_total)
   print "*********************************"
   print "TOTAL    %8.2f%8.2f%8.2f%8.9s" % (dG_point.G/ph2Kcal, dG_point.G/mev2Kcal, 
dG_point.G,"  sum_crg")
   print "*********************************"

'''