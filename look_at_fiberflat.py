import os
import numpy as np
from desispec.io import read_frame
from astropy.table import Table
import fitsio
import matplotlib.pyplot as plt
from astropy.stats import sigma_clip

table=Table.read(os.environ["DESIMODEL"]+"/data/focalplane/desi-focalplane_2019-09-16T00:00:00.ecsv", format='ascii.ecsv')
ii=np.where((table["PETAL"]==0)&(table["FIBER"]>=0))[0]
xk="OFFSET_X"
yk="OFFSET_Y"
fiberid="FIBER"
dico={}
for i in ii :
   dico[table[fiberid][i]]=i



ff_file_b3='/project/projectdirs/desi/spectro/desi_spectro_calib/trunk/spec/sp3/fiberflat-sm4-b-20191022.fits'
ff_file_r3='/project/projectdirs/desi/spectro/desi_spectro_calib/trunk/spec/sp3/fiberflat-sm4-r-20191022.fits'
ff_file_z3='/project/projectdirs/desi/spectro/desi_spectro_calib/trunk/spec/sp3/fiberflat-sm4-z-20191022.fits'


fff_b3=fitsio.FITS(ff_file_b3)
fff_r3=fitsio.FITS(ff_file_r3)
fff_z3=fitsio.FITS(ff_file_z3)

ff_b3=fff_b3['FIBERFLAT'][:,:]
ff_r3=fff_r3['FIBERFLAT'][:,:]
ff_z3=fff_z3['FIBERFLAT'][:,:]
frame_b3=read_frame('/project/projectdirs/desi/spectro/redux/v0/exposures/20191028/00022301/frame-b3-00022301.fits')

fiber=frame_b3.fibermap["FIBER"]-1500
x=np.zeros(fiber.size)
y=np.zeros(fiber.size)

for j,fib in enumerate(fiber) :
   x[j]=table[xk][dico[fib]]
   y[j]=table[yk][dico[fib]]
ff_b3_median=np.median(ff_b3,axis=1)
ff_r3_median=np.median(ff_r3,axis=1)
ff_z3_median=np.median(ff_z3,axis=1)

s1=30
contrast=2
plt.figure(0,figsize=(12,10))
plt.subplot(331)
plt.scatter(x,y,c=ff_b3_median,cmap="plasma",vmin=0.9,vmax=1.1,s=s1)
plt.colorbar()
plt.title('Fiberflat B3')

plt.subplot(332)
plt.scatter(x,y,c=ff_r3_median,cmap="plasma",vmin=0.9,vmax=1.1,s=s1)
plt.colorbar()
plt.title('Fiberflat R3')

plt.subplot(333)
plt.scatter(x,y,c=ff_z3_median,cmap="plasma",vmin=0.9,vmax=1.1,s=s1)
plt.colorbar()
plt.title('Fiberflat Z3')


plt.tight_layout()
plt.show()
import pdb;pdb.set_trace()

