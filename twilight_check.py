#!/usr/bin/env python
import os
import sys
import numpy as np
from desispec.io import read_frame,read_fiberflat,write_fiberflat
from astropy.table import Table
import matplotlib.pyplot as plt
from astropy.io import fits

table=Table.read(os.environ["DESIMODEL"]+"/data/focalplane/desi-focalplane_2019-09-16T00:00:00.ecsv", format='ascii.ecsv')
ii=np.where((table["PETAL"]==0)&(table["FIBER"]>=0))[0]
xk="OFFSET_X"
yk="OFFSET_Y"
fiberid="FIBER"
dico={}
for i in ii :
   dico[table[fiberid][i]]=i

expid_arr=["00033801"]#["00020206","00020207"]
flux_b3_all=[]
flux_r3_all=[]
flux_z3_all=[]

for i in range(len(expid_arr)):
    expid=expid_arr[i]
    frame_b3=read_frame("flatfielded-frame-b3-"+expid+"-twilightcorr.fits")
    flux_b3=np.median(frame_b3.flux,axis=1)
    flux_b3 /= np.median(flux_b3)

    frame_r3=read_frame("flatfielded-frame-r3-"+expid+"-twilightcorr.fits")
    flux_r3=np.median(frame_r3.flux,axis=1)
    flux_r3 /= np.median(flux_r3)

    frame_z3=read_frame("flatfielded-frame-z3-"+expid+"-twilightcorr.fits")
    flux_z3=np.median(frame_z3.flux,axis=1)
    flux_z3 /= np.median(flux_z3)

    flux_b3_all.append(flux_b3)
    flux_r3_all.append(flux_r3)
    flux_z3_all.append(flux_z3)

flux_b3_median=np.median(np.array(flux_b3_all),axis=0)
flux_r3_median=np.median(np.array(flux_r3_all),axis=0)
flux_z3_median=np.median(np.array(flux_z3_all),axis=0)
ind=np.where(flux_b3_median<0.2)
flux_b3_median[ind]=1.0
flux_r3_median[ind]=1.0
flux_z3_median[ind]=1.0



fiber=frame_b3.fibermap["FIBER"]-1500
x=np.zeros(fiber.size)
y=np.zeros(fiber.size)
for j,fib in enumerate(fiber) :
    x[j]=table[xk][dico[fib]]
    y[j]=table[yk][dico[fib]]

plt.subplot(131)
plt.scatter(x,y,c=flux_b3_median,cmap="plasma",vmin=0.95,vmax=1.05)
plt.colorbar()

plt.subplot(132)
plt.scatter(x,y,c=flux_r3_median,cmap="plasma",vmin=0.95,vmax=1.05)
plt.colorbar()

plt.subplot(133)
plt.scatter(x,y,c=flux_z3_median,cmap="plasma",vmin=0.95,vmax=1.05)
plt.colorbar()

plt.tight_layout()


plt.show()
