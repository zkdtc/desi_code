#!/usr/bin/env python
import os
import sys
import numpy as np
from desispec.io import read_frame
from astropy.table import Table
import matplotlib.pyplot as plt
camera="b3"
table=Table.read(os.environ["DESIMODEL"]+"/data/focalplane/desi-focalplane_2019-09-16T00:00:00.ecsv", format='ascii.ecsv')
ii=np.where((table["PETAL"]==0)&(table["FIBER"]>=0))[0]
xk="OFFSET_X"
yk="OFFSET_Y"
fiberid="FIBER"
dico={}
for i in ii :
   dico[table[fiberid][i]]=i
expid="00020207"   # 00020205 z band saturates, 00020206 good. 
frame_b3=read_frame("flatfielded-frame-b3-"+expid+".fits")
flux_b3=np.median(frame_b3.flux,axis=1)
flux_b3 /= np.median(flux_b3)

frame_r3=read_frame("flatfielded-frame-r3-"+expid+".fits")
flux_r3=np.median(frame_r3.flux,axis=1)
flux_r3 /= np.median(flux_r3)

frame_z3=read_frame("flatfielded-frame-z3-"+expid+".fits")
flux_z3=np.median(frame_z3.flux,axis=1)
flux_z3 /= np.median(flux_z3)



fiber=frame_b3.fibermap["FIBER"]-1500
x=np.zeros(fiber.size)
y=np.zeros(fiber.size)

for j,fib in enumerate(fiber) :
   x[j]=table[xk][dico[fib]]
   y[j]=table[yk][dico[fib]]



################################################
##############  Plot  ##########################
################################################

s1=20
dist=np.sqrt(x**2+y**2)

plt.figure(0,figsize=(12,10))
plt.subplot(331)
plt.scatter(x,y,c=flux_b3,cmap="plasma",vmin=0.95,vmax=1.05,s=s1)
plt.colorbar()
plt.title('b3')

plt.subplot(332)
plt.scatter(x,y,c=flux_r3,cmap="plasma",vmin=0.95,vmax=1.05,s=s1)
plt.colorbar()
plt.title('r3')

plt.subplot(333)
plt.scatter(x,y,c=flux_z3,cmap="plasma",vmin=0.95,vmax=1.05,s=s1)
plt.colorbar()
plt.title('z3')

s=10
plt.subplot(334)
plt.scatter(dist,flux_b3,c='blue',s=s)
plt.xlabel('Distance')
plt.ylabel('b3 Flux')
plt.axis([0,500,0.95,1.05])

plt.subplot(335)
plt.scatter(dist,flux_b3,c='green',s=s)
plt.xlabel('Distance')
plt.ylabel('r3 Flux')
plt.axis([0,500,0.95,1.05])

plt.subplot(336)
plt.scatter(dist,flux_z3,c='red',s=s)
plt.xlabel('Distance')
plt.ylabel('z3 Flux')
plt.axis([0,500,0.95,1.05])

########################################

plt.subplot(337)
plt.scatter(flux_b3,flux_r3,c='blue',s=s)
plt.plot([0,2],[0,2],c='black',linestyle='dashed')
plt.xlabel('b3 Flux')
plt.ylabel('r3 Flux')
plt.axis([0.95,1.05,0.95,1.05])

plt.subplot(338)
plt.scatter(flux_b3,flux_z3,c='red',s=s)
plt.plot([0,2],[0,2],c='black',linestyle='dashed')
plt.xlabel('b3 Flux')
plt.ylabel('z3 Flux')
plt.axis([0.95,1.05,0.95,1.05])






plt.tight_layout()
plt.show()
