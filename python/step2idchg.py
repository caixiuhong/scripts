
# coding: utf-8

# In[1]:

import os, re


# inputpathway of initial step2_out.pdb, outputpathway of modified step2_out.pdb, name it step2_out.pdb_new
inputpathway='C:/Users/PC/Dropbox/cai/python/'
outputpathway='C:/Users/PC/Dropbox/cai/python/'

with open(outputpathway+'step2_out.pdb_new', mode='w', encoding='utf-8') as f1:
    #output file name: 
    with open(inputpathway+'step2_out.pdb',mode='r',encoding='utf-8') as f2:
        print("processing %s." % (str(f2)))
        lines=[l for l in f2.readlines()]
        for l in lines:
            res_chain=l[21]
            if (res_chain == "A"):
                resid=l[22:26]
                #print("resid in lines: "+resid)
                #change residue id to resid_new
                resid_new_n=int(resid)+1

                resid_new=str(resid_new_n).zfill(4)
                l_new=re.sub(l[22:26],resid_new,l)
            else:
                l_new=l
            f1.write(l_new)


            
     


# In[ ]:





