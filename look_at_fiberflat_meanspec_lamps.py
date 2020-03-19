import matplotlib.pyplot as plt
from desispec.io import read_fiberflat
import numpy as np


data_dir='/global/project/projectdirs/desi/spectro/redux/daily/calibnight/'
night='20191115'
camera4='r4'
camera0='r0'

#data_dir='/project/projectdirs/desi/spectro/redux/minisv0c/calibnight/'
night='20200125'
camera4='r4'
camera0='r0'

f4_0=data_dir+night+'/tmp/fiberflatnight-camera-'+camera4+'-lamp-0.fits'
f4_1=data_dir+night+'/tmp/fiberflatnight-camera-'+camera4+'-lamp-1.fits'
f4_2=data_dir+night+'/tmp/fiberflatnight-camera-'+camera4+'-lamp-2.fits'
f4_3=data_dir+night+'/tmp/fiberflatnight-camera-'+camera4+'-lamp-3.fits'

f0_0=data_dir+night+'/tmp/fiberflatnight-camera-'+camera0+'-lamp-0.fits'
f0_1=data_dir+night+'/tmp/fiberflatnight-camera-'+camera0+'-lamp-1.fits'
f0_2=data_dir+night+'/tmp/fiberflatnight-camera-'+camera0+'-lamp-2.fits'
f0_3=data_dir+night+'/tmp/fiberflatnight-camera-'+camera0+'-lamp-3.fits'

d4_0=read_fiberflat(f4_0)
d4_1=read_fiberflat(f4_1)
d4_2=read_fiberflat(f4_2)
d4_3=read_fiberflat(f4_3)

d0_0=read_fiberflat(f0_0)
d0_1=read_fiberflat(f0_1)
d0_2=read_fiberflat(f0_2)
d0_3=read_fiberflat(f0_3)
plt.subplot(2,2,1)
plt.plot(d0_0.wave,d0_0.meanspec,label=camera0+' lamp0')
plt.plot(d4_0.wave,d4_0.meanspec,label=camera4+' lamp0')
plt.xlabel('Wavelength')
plt.ylabel('Flux')
plt.legend(loc='upper right')
plt.title(night)
plt.subplot(2,2,2)
start=0
end=500
plt.plot(d4_0.wave[start:end],d4_0.meanspec[start:end],label=camera4+' lamp0')
plt.plot(d4_1.wave,d4_1.meanspec,label=camera4+' lamp1')
plt.plot(d4_2.wave,d4_2.meanspec,label=camera4+' lamp2')
plt.plot(d4_3.wave,d4_3.meanspec,label=camera4+' lamp3')
plt.xlabel('Wavelength')
plt.legend(loc='upper right')

plt.subplot(2,2,3)
plt.plot(d0_0.wave,np.median(d0_0.fiberflat,axis=0),label=camera0+' lamp0')
plt.plot(d4_0.wave,np.median(d4_0.fiberflat,axis=0),label=camera4+' lamp0')
plt.xlabel('Wavelength')
plt.ylabel('Fiberflat')
plt.legend(loc='upper right')




plt.show()









