
# coding: utf-8

# In[3]:


from PIL import Image
def Fig2Tiff(oldfig, newfig):
    '''
    oldfig: file of old foramt figure
    newfig: file of new format figure
    '''
    im = Image.open(oldfig)
    im.save(newfig,quality=300)
    return


# In[4]:


import sys,os
if __name__=='__main__':
    if len(sys.argv) < 3:
        print("./ms_agg.py sheet_name")
        sys.exit()
    else:
        Fig2Tiff(sys.argv[1], sys.argv[2])

