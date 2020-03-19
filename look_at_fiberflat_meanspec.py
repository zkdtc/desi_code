import matplotlib.pyplot as plt
from desispec.io import read_fiberflat
import numpy as np


########### Fiberflat Night #############
data_dir='/project/projectdirs/desi/spectro/redux/minisv0c/calibnight/'
night='20200125'

#data_dir='/global/project/projectdirs/desi/spectro/redux/daily/calibnight/'
#night='20200301'
#night='20200202'

channel='r'
camera0=channel+'0'
camera1=channel+'1'
camera2=channel+'2'
camera3=channel+'3'
camera4=channel+'4'
camera5=channel+'5'
camera6=channel+'6'
camera7=channel+'7'
camera8=channel+'8'
camera9=channel+'9'

f0=data_dir+night+'/fiberflatnight-'+camera0+'-'+night+'.fits'
f1=data_dir+night+'/fiberflatnight-'+camera1+'-'+night+'.fits'
f2=data_dir+night+'/fiberflatnight-'+camera2+'-'+night+'.fits'
f3=data_dir+night+'/fiberflatnight-'+camera3+'-'+night+'.fits'
f4=data_dir+night+'/fiberflatnight-'+camera4+'-'+night+'.fits'
f5=data_dir+night+'/fiberflatnight-'+camera5+'-'+night+'.fits'
f6=data_dir+night+'/fiberflatnight-'+camera6+'-'+night+'.fits'
f7=data_dir+night+'/fiberflatnight-'+camera7+'-'+night+'.fits'
f8=data_dir+night+'/fiberflatnight-'+camera8+'-'+night+'.fits'
f9=data_dir+night+'/fiberflatnight-'+camera9+'-'+night+'.fits'


######### Individual fiberflat ###########
#data_dir='/global/project/projectdirs/desi/spectro/redux/daily/exposures/'
#night='20191024'
#exp='00020676'
#night='20200308'
#exp='00054444'
#night='20191115'
#exp='00028364'

#f0=data_dir+'/'+night+'/'+exp+'/fiberflat-'+camera0+'-'+exp+'.fits'
#f1=data_dir+'/'+night+'/'+exp+'/fiberflat-'+camera1+'-'+exp+'.fits'
#f2=data_dir+'/'+night+'/'+exp+'/fiberflat-'+camera2+'-'+exp+'.fits'
#f3=data_dir+'/'+night+'/'+exp+'/fiberflat-'+camera3+'-'+exp+'.fits'
#f4=data_dir+'/'+night+'/'+exp+'/fiberflat-'+camera4+'-'+exp+'.fits'
#f5=data_dir+'/'+night+'/'+exp+'/fiberflat-'+camera5+'-'+exp+'.fits'
#f6=data_dir+'/'+night+'/'+exp+'/fiberflat-'+camera6+'-'+exp+'.fits'
#f7=data_dir+'/'+night+'/'+exp+'/fiberflat-'+camera7+'-'+exp+'.fits'
#f8=data_dir+'/'+night+'/'+exp+'/fiberflat-'+camera8+'-'+exp+'.fits'
#f9=data_dir+'/'+night+'/'+exp+'/fiberflat-'+camera9+'-'+exp+'.fits'
try:
    d0=read_fiberflat(f0)
except:
    pass
try:
    d1=read_fiberflat(f1)
except:
    pass
try:
    d2=read_fiberflat(f2)
except:
    pass
try:
    d3=read_fiberflat(f3)
except:
    pass
try:
    d4=read_fiberflat(f4)
except:
    pass
try:
    d5=read_fiberflat(f5)
except:
    pass
try:
    d6=read_fiberflat(f6)
except:
    pass
try:
    d7=read_fiberflat(f7)
except:
    pass
try:
    d8=read_fiberflat(f8)
except:
    pass
try:
    d9=read_fiberflat(f9)
except:
    pass

plt.subplot(2,2,1)
try:
    plt.plot(d0.wave,d0.meanspec,label=camera0)
except:
    pass
try:
    plt.plot(d1.wave,d1.meanspec,label=camera1)
except:
    pass
try:
    plt.plot(d2.wave,d2.meanspec,label=camera2)
except:
    pass
try:
    plt.plot(d3.wave,d3.meanspec,label=camera3)
except:
    pass
try:
    plt.plot(d4.wave,d4.meanspec,label=camera4)
except:
    pass
try:
    plt.plot(d5.wave,d5.meanspec,label=camera5)
except:
    pass
try:
    plt.plot(d6.wave,d6.meanspec,label=camera6)
except:
    pass
try:
    plt.plot(d7.wave,d7.meanspec,label=camera7)
except:
    pass
try:
    plt.plot(d8.wave,d8.meanspec,label=camera8)
except:
    pass
try:
    plt.plot(d9.wave,d9.meanspec,label=camera9)
except:
    pass

plt.xlabel('Wavelength')
plt.ylabel('Meanspec')
#plt.legend(loc='upper right')

plt.subplot(2,2,2)
try:
    plt.plot(d0.wave,np.median(d0.fiberflat,axis=0),label=camera0)
except:
    pass
try:
    plt.plot(d1.wave,np.median(d1.fiberflat,axis=0),label=camera1)
except:
    pass
try:
    plt.plot(d2.wave,np.median(d2.fiberflat,axis=0),label=camera2)
except:
    pass
try:
    plt.plot(d3.wave,np.median(d3.fiberflat,axis=0),label=camera3)
except:
    pass
try:
    plt.plot(d4.wave,np.median(d4.fiberflat,axis=0),label=camera4)
except:
    pass
try:
    plt.plot(d5.wave,np.median(d5.fiberflat,axis=0),label=camera5)
except:
    pass
try:
    plt.plot(d6.wave,np.median(d6.fiberflat,axis=0),label=camera6)
except:
    pass
try:
    plt.plot(d7.wave,np.median(d7.fiberflat,axis=0),label=camera7)
except:
    pass
try:
    plt.plot(d8.wave,np.median(d8.fiberflat,axis=0),label=camera8)
except:
    pass
try:
    plt.plot(d9.wave,np.median(d9.fiberflat,axis=0),label=camera9)
except:
    pass
plt.xlabel('Wavelength')
plt.ylabel('Fiberflat')


plt.subplot(2,2,3)
try:
    plt.plot(d0.wave,np.median(d0.fiberflat,axis=0),label=camera0)
except:
    pass
try:
    plt.plot(d1.wave,np.median(d1.fiberflat,axis=0),label=camera1)
except:
    pass
try:
    plt.plot(d2.wave,np.median(d2.fiberflat,axis=0),label=camera2)
except:
    pass
try:
    plt.plot(d3.wave,np.median(d3.fiberflat,axis=0),label=camera3)
except:
    pass
try:
    plt.plot(d4.wave,np.median(d4.fiberflat,axis=0),label=camera4)
except:
    pass
try:
    plt.plot(d5.wave,np.median(d5.fiberflat,axis=0),label=camera5)
except:
    pass
try:
    plt.plot(d6.wave,np.median(d6.fiberflat,axis=0),label=camera6)
except:
    pass
try:
    plt.plot(d7.wave,np.median(d7.fiberflat,axis=0),label=camera7)
except:
    pass
try:
    plt.plot(d8.wave,np.median(d8.fiberflat,axis=0),label=camera8)
except:
    pass
try:
    plt.plot(d9.wave,np.median(d9.fiberflat,axis=0),label=camera9)
except:
    pass

start=0
end=300
try:
    plt.xlim(d0.wave[start],d0.wave[end])
except:
    pass
plt.xlabel('Wavelength')
plt.ylabel('Fiberflat')
#plt.legend(loc='upper right')

plt.subplot(2,2,4)
try:
    plt.plot(d0.wave,np.median(d0.fiberflat,axis=0),label=camera0)
except:
    pass
try:
    plt.plot(d1.wave,np.median(d1.fiberflat,axis=0),label=camera1)
except:
    pass
try:
    plt.plot(d2.wave,np.median(d2.fiberflat,axis=0),label=camera2)
except:
    pass
try:
    plt.plot(d3.wave,np.median(d3.fiberflat,axis=0),label=camera3)
except:
    pass
try:
    plt.plot(d4.wave,np.median(d4.fiberflat,axis=0),label=camera4)
except:
    pass
try:
    plt.plot(d5.wave,np.median(d5.fiberflat,axis=0),label=camera5)
except:
    pass
try:
    plt.plot(d6.wave,np.median(d6.fiberflat,axis=0),label=camera6)
except:
    pass
try:
    plt.plot(d7.wave,np.median(d7.fiberflat,axis=0),label=camera7)
except:
    pass
try:
    plt.plot(d8.wave,np.median(d8.fiberflat,axis=0),label=camera8)
except:
    pass
try:
    plt.plot(d9.wave,np.median(d9.fiberflat,axis=0),label=camera9)
except:
    pass

start=-300
end=-1
try:
    plt.xlim(d0.wave[start],d0.wave[end])
except:
    pass
plt.xlabel('Wavelength')
plt.ylabel('Fiberflat')
plt.legend(loc='upper left')

plt.show()
tmp=d4.fiberflat #np.median(d6.fiberflat,axis=0)
x=[2,2.5,2.6,2.7,2.8,2.9,3]

y=[np.sum(tmp>=2),np.sum(tmp>=2.5),np.sum(tmp>=2.6),np.sum(tmp>=2.7),np.sum(tmp>=2.8),np.sum(tmp>=2.9),np.sum(tmp>=3)]
plt.plot(x,y)
plt.xlabel('Threshold')
plt.ylabel('R4 Masked Pixels Number')
plt.show()
import pdb;pdb.set_trace()

