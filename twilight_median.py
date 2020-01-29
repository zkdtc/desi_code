#!/usr/bin/env python
import os
import sys
import numpy as np
from desispec.io import read_frame,read_fiberflat,write_fiberflat
from astropy.table import Table
import matplotlib.pyplot as plt
import astropy.io.fits as fits

table=Table.read(os.environ["DESIMODEL"]+"/data/focalplane/desi-focalplane_2019-09-16T00:00:00.ecsv", format='ascii.ecsv')
ii=np.where((table["PETAL"]==0)&(table["FIBER"]>=0))[0]
xk="OFFSET_X"
yk="OFFSET_Y"
fiberid="FIBER"
dico={}
for i in ii :
   dico[table[fiberid][i]]=i
sp_arr=['0','1', '2','3','4','5','6','7','8','9']
sm_arr=['4','10','5','6','1','9','7','8','2','3']
sp_arr=['9']
sm_arr=['3']


new=False #True
"""
infile_b3='/global/project/projectdirs/desi/spectro/redux/daily/exposures/20191217/fiberflatnight-b3-20191217.fits' #'/software/datasystems/desi_spectro_calib/trunk/spec/sp3/fiberflat-sm4-b-20191022.fits'
infile_r3='/global/project/projectdirs/desi/spectro/redux/daily/exposures/20191217/fiberflatnight-r3-20191217.fits'
infile_z3='/global/project/projectdirs/desi/spectro/redux/daily/exposures/20191217/fiberflatnight-z3-20191217.fits'

outfile_b3='fiberflat-sm4-z-20191217.fits'
outfile_r3='fiberflat-sm4-r-20191217.fits'
outfile_z3='fiberflat-sm4-z-20191217.fits'

data_dir="/global/project/projectdirs/desi/spectro/redux/daily/exposures/20191219/"
expid_arr=['00033801']#['00022422','00022423','00022424','00022426','00022428','00022429','00022430','00022431','00022432','00022433','00022434','00022435','00022436'] #["00020206","00020207","00020208","00020209","00020210","00020211","00020212"]
"""

for num in range(len(sp_arr)):
    sp=sp_arr[num]
    sm=sm_arr[num]
    infile_b='/project/projectdirs/desi/spectro/desi_spectro_calib/trunk/spec/sm'+sm+'/fiberflatnight-b'+sp+'-20200125.fits'
    infile_r='/project/projectdirs/desi/spectro/desi_spectro_calib/trunk/spec/sm'+sm+'/fiberflatnight-r'+sp+'-20200125.fits'
    infile_z='/project/projectdirs/desi/spectro/desi_spectro_calib/trunk/spec/sm'+sm+'/fiberflatnight-z'+sp+'-20200125.fits'

    outfile_b='fiberflat-sm'+sm+'-b-20200127.fits'
    outfile_r='fiberflat-sm'+sm+'-r-20200127.fits'
    outfile_z='fiberflat-sm'+sm+'-z-20200127.fits'

    data_dir="/global/project/projectdirs/desi/spectro/redux/daily/exposures/20200127/"
    expid_arr=['00044457']


    fiberflat_b=read_fiberflat(infile_b)
    fiberflat_r=read_fiberflat(infile_r)
    fiberflat_z=read_fiberflat(infile_z)

    flux_b_all=[]
    flux_r_all=[]
    flux_z_all=[]

    for i in range(len(expid_arr)):
        expid=expid_arr[i]
        frame_b=read_frame(data_dir+expid+"/flatfielded-frame-b"+sp+"-"+expid+".fits")
        flux_b=np.median(frame_b.flux,axis=1)
        flux_b /= np.median(flux_b)

    frame_r=read_frame(data_dir+expid+"/flatfielded-frame-r"+sp+"-"+expid+".fits")
    flux_r=np.median(frame_r.flux,axis=1)
    flux_r /= np.median(flux_r)

    frame_z=read_frame(data_dir+expid+"/flatfielded-frame-z"+sp+"-"+expid+".fits")
    flux_z=np.median(frame_z.flux,axis=1)
    flux_z /= np.median(flux_z)

    flux_b_all.append(flux_b)
    flux_r_all.append(flux_r)
    flux_z_all.append(flux_z)

flux_b_median=np.median(np.array(flux_b_all),axis=0)
flux_r_median=np.median(np.array(flux_r_all),axis=0)
flux_z_median=np.median(np.array(flux_z_all),axis=0)
ind=np.where(flux_b_median<0.2)
flux_b_median[ind]=1.0
flux_r_median[ind]=1.0
flux_z_median[ind]=1.0

##############################################
########### Apply Correction #################
##############################################

for i in range(len(fiberflat_b.fiberflat)):
    fiberflat_b.fiberflat[i]*=flux_b_median[i]
    fiberflat_r.fiberflat[i]*=flux_r_median[i]
    fiberflat_z.fiberflat[i]*=flux_z_median[i]
    fiberflat_b.ivar[i]/=flux_b_median[i]**2
    fiberflat_r.ivar[i]/=flux_r_median[i]**2
    fiberflat_z.ivar[i]/=flux_z_median[i]**2

if new:
    write_fiberflat(outfile_b,fiberflat_b,header=fiberflat_b.header)
    write_fiberflat(outfile_r,fiberflat_r,header=fiberflat_r.header)
    write_fiberflat(outfile_z,fiberflat_z,header=fiberflat_z.header)

    #fits.append('fiberflat-sm4-b-20191022-twilightcorr.fits', flux_b3_median, name='TWILIGHTCORR')
    h=fits.open(outfile_b)
    h.append(fits.ImageHDU(flux_b_median,name="TWILIGHTCORR"))
    h.writeto(outfile_b,overwrite=True)

    h=fits.open(outfile_r)
    h.append(fits.ImageHDU(flux_r_median,name="TWILIGHTCORR"))
    h.writeto(outfile_r,overwrite=True)

    h=fits.open(outfile_z)
    h.append(fits.ImageHDU(flux_z_median,name="TWILIGHTCORR"))
    h.writeto(outfile_z,overwrite=True)


fiber=frame_b.fibermap["FIBER"]-500*int(sp)
x=np.zeros(fiber.size)
y=np.zeros(fiber.size)
for j,fib in enumerate(fiber) :
    x[j]=table[xk][dico[fib]]
    y[j]=table[yk][dico[fib]]
dist=np.sqrt(x**2+y**2)

plt.figure(0,figsize=(12,8))
plt.subplot(231)
plt.scatter(x,y,c=flux_b_median,cmap="plasma",vmin=0.95,vmax=1.05)
plt.colorbar()
plt.title('B')

plt.subplot(232)
plt.scatter(x,y,c=flux_r_median,cmap="plasma",vmin=0.95,vmax=1.05)
plt.colorbar()
plt.title('R')

plt.subplot(233)
plt.scatter(x,y,c=flux_z_median,cmap="plasma",vmin=0.95,vmax=1.05)
plt.colorbar()
plt.title('Z')

plt.subplot(234)
plt.scatter(dist,flux_b_median,color='blue',s=20)
plt.title('B')
plt.xlabel('Distance')
plt.ylabel('Correction')

plt.subplot(235)
plt.scatter(dist,flux_r_median,color='green',s=20)
plt.title('R')
plt.xlabel('Distance')
plt.ylabel('Correction')

plt.subplot(236)
plt.scatter(dist,flux_z_median,color='red',s=20)
plt.title('Z')
plt.xlabel('Distance')
plt.ylabel('Correction')


plt.tight_layout()


plt.show()
