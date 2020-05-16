import os
from os import listdir
import matplotlib.pyplot as plt
from astropy.io import fits
import numpy as np

import sys
night_arr=[sys.argv[1]]
print(night_arr)

n_night=len(night_arr)

if True:
    
    sp_arr=['0','1','2','3','4','5','6','7','8','9']
    cam_arr=['b','r','z']
    for i in range(n_night):
        night=night_arr[i]
        outdir='/global/project/projectdirs/desi/users/zhangkai/redux_zeros/'+night
        cmd='mkdir '+outdir
        a=os.system(cmd)
        expid_arr=listdir('/global/cfs/cdirs/desi/spectro/data/'+night)
        for expid in expid_arr:
            filename='/global/cfs/cdirs/desi/spectro/data/'+night+'/'+expid+'/desi-'+expid+'.fits.fz'
            try:
                h1=fits.getheader(filename,1)
                print(night,expid,h1['OBSTYPE'].lower())
                if h1['OBSTYPE'].lower()=='zero':
                    for cam in cam_arr:
                        for sp in sp_arr:
                            camera=cam+sp
                            cmd='desi_preproc -i $DESI_SPECTRO_DATA/'+night+'/'+expid+'/desi-'+expid+'.fits.fz -o '+outdir+'/'+expid+'/preproc-'+camera+'-'+expid+'.fits --cameras '+camera
                            a=os.system(cmd)
            except:
                pass


"""
hdul=fits.open('test.fits')
plt.imshow(hdul[0].data,vmin=0,vmax=10)
plt.show()
plt.hist(np.array(hdul[0].data).ravel(),50,range=(-10,10))
plt.show()
"""


    

