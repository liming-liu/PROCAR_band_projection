#!/usr/env/bin python

# To project band on atoms for a MD run
# By Liming Liu

import linecache as lc
import numpy as np
import operator as op
import os
from functools import reduce

# the band projection function
def band_proj(wd):
    
    print(wd) 
    # get total atom number
    N = int(lc.getline('./'+wd+'/PROCAR', 2).split()[-1])
    
    # read PROCAR into buffer
    with open('./'+wd+'/PROCAR','r') as f:
        lines=f.readlines()
    f.close()
    
    # screen band 295 from buffer
    band = []
    for i in range(len(lines)):
        if 'band   292' in lines[i]:
            band.append(lines[i+3:i+3+N])
    # change the band data to numeric array
    a1 = np.array(reduce(op.add, reduce(op.add, band)).split(),\
    dtype='float')   # a temporary 1D array to hold data of band
    db = a1.reshape(int(np.size(a1)/11), 11)   # reashape a1 to sensible size
    
    # cut off spin down part data
    hdb = db[0:int(np.shape(db)[0]/2),:]
    
    # sorting atoms according total contribution to a band
    atom_num = hdb[np.argsort(hdb[:,-1]), 0]
    # append data to file
    out.write(wd+' '+str(atom_num[-1])+'\n')
   
out = open('out', 'a+')

for k in sorted(os.listdir()):
    if k.isdigit():
        band_proj(k)

out.close()

# sketch a figure
import matplotlib.pyplot as plt

x = np.loadtxt('out', dtype='float')
plt.plot(x[:,0], x[:,1], 'r-')
plt.xlabel('Time (fs)')
plt.ylabel('Band projection on atoms (a.u.)')
plt.savefig('band_proj.png', dpi=300)
plt.show()
