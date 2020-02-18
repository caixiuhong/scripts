#!/usr/bin/python
import sys
import string
#import re
import mfe_adv






###                             Above is mfe.py code                            #######
################################################################################################################################################
###                             Below is to define the cluster and energy for the whole cluster                           ###

#ASP-A0287_;ASP-A0372_;HIS+A0376_;GLU-B0126_;PAA-K9301_;PDD-K9302_
cluster_residues=["ASP-A0287_", "ASP-A0372_" , "HIS+A0376_" , "GLU-B0126_" , "PAA-K9301_" , "PDD-K9302_"]
titr_point="7"
cut_off="2"
data={}
for cluster_residue in cluster_residues:
  data[cluster_residue]=mfe_adv.run_mfe(cluster_residue,titr_point, cut_off)
#  print data[cluster_residue].G

print "\n"
print "\n"


print "SUMMARY"
print "Residues %s %s %s %s %s %s interactions:" % (cluster_residues[0], cluster_residues[1],\
cluster_residues[2], cluster_residues[3], cluster_residues[4], cluster_residues[5])
charges={}
for cluster_residue in cluster_residues:
  resname=cluster_residue[0:3]+cluster_residue[4:9]
  charges[cluster_residue]=mfe_adv.print_crg(resname)
print "Residues %s %s %s %s %s %s" % (cluster_residues[0], cluster_residues[1],\
cluster_residues[2], cluster_residues[3], cluster_residues[4], cluster_residues[5])
print "Charge   %10.2f %10.2f %10.2f %10.2f %10.2f %10.2f" % (float(charges[cluster_residues[0]]), float(charges[cluster_residues[1]]),float(charges[cluster_residues[2]]),float(charges[cluster_residues[3]]),float(charges[cluster_residues[4]]),float(charges[cluster_residues[5]]))
print "Terms          pH     meV    Kcal"
sum_inter= mfe_adv.E_IONIZE()
sum_inter.vdw0 = sum(data[cluster_residue].vdw0 for cluster_residue in cluster_residues)
sum_inter.vdw1 = sum(data[cluster_residue].vdw1 for cluster_residue in cluster_residues)
sum_inter.tors = sum(data[cluster_residue].tors for cluster_residue in cluster_residues)
sum_inter.epol = sum(data[cluster_residue].epol for cluster_residue in cluster_residues)
sum_inter.dsolv = sum(data[cluster_residue].dsolv for cluster_residue in cluster_residues)
sum_inter.extra = sum(data[cluster_residue].extra for cluster_residue in cluster_residues)
sum_inter.pHeffect = sum(data[cluster_residue].pHeffect for cluster_residue in cluster_residues)
sum_inter.Eheffect = sum(data[cluster_residue].Eheffect for cluster_residue in cluster_residues)
sum_inter.TS = sum(data[cluster_residue].TS for cluster_residue in cluster_residues)
sum_inter.mfe_total = sum(data[cluster_residue].mfe_total for cluster_residue in cluster_residues)
sum_inter.G = sum(data[cluster_residue].G for cluster_residue in cluster_residues)
ph2Kcal=mfe_adv.ph2Kcal
mev2Kcal=mfe_adv.mev2Kcal
print "vdw0     %8.2f%8.2f%8.2f" % (sum_inter.vdw0/ph2Kcal, sum_inter.vdw0/mev2Kcal, sum_inter.vdw0)
print "vdw1     %8.2f%8.2f%8.2f" % (sum_inter.vdw1/ph2Kcal, sum_inter.vdw1/mev2Kcal, sum_inter.vdw1)
print "tors     %8.2f%8.2f%8.2f" % (sum_inter.tors/ph2Kcal, sum_inter.tors/mev2Kcal, sum_inter.tors)
print "ebkb     %8.2f%8.2f%8.2f" % (sum_inter.epol/ph2Kcal, sum_inter.epol/mev2Kcal, sum_inter.epol)
print "dsol     %8.2f%8.2f%8.2f" % (sum_inter.dsolv/ph2Kcal, sum_inter.dsolv/mev2Kcal, sum_inter.dsolv)
print "offset   %8.2f%8.2f%8.2f" % (sum_inter.extra/ph2Kcal, sum_inter.extra/mev2Kcal, sum_inter.extra)
print "pH&pK0   %8.2f%8.2f%8.2f" % (sum_inter.pHeffect/ph2Kcal, sum_inter.pHeffect/mev2Kcal, sum_inter.pHeffect)
print "Eh&Em0   %8.2f%8.2f%8.2f" % (sum_inter.Eheffect/ph2Kcal, sum_inter.Eheffect/mev2Kcal, sum_inter.Eheffect)
print "-TS      %8.2f%8.2f%8.2f" % (-sum_inter.TS/ph2Kcal, -sum_inter.TS/mev2Kcal, -sum_inter.TS)
print "residues %8.2f%8.2f%8.2f" % (sum_inter.mfe_total/ph2Kcal, sum_inter.mfe_total/mev2Kcal, sum_inter.mfe_total)
print "*********************************"

sum_inter.G_self= sum_inter.G - sum_inter.mfe_total + sum_inter.TS
print "SelfnoTS %8.2f%8.2f%8.2f" % (sum_inter.G_self/ph2Kcal, sum_inter.G_self/mev2Kcal, sum_inter.G_self)
print "Out_pair %8.2f%8.2f%8.2f" % (sum_inter.mfe_total/ph2Kcal, sum_inter.mfe_total/mev2Kcal, sum_inter.mfe_total)
print "TOTAL    %8.2f%8.2f%8.2f" % (sum_inter.G/ph2Kcal, sum_inter.G/mev2Kcal, sum_inter.G)
print "*********************************"
print "Done"
