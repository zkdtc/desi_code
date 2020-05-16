import os
from os import listdir
import matplotlib.pyplot as plt
from astropy.io import fits
import numpy as np

import sys
night_arr=['20200315']
expid='00055709' #arc
expid='00055556' #twilight
expid='00055589' # science
#expid='00055713' # flat
add_keyword=' --scattered-light'

expid='00055555' # zero
add_keyword=''

night_arr=['20191231']
expid='00037053' # zero
add_keyword=''

night_arr=['20191110']
expid='00026341'
add_keyword=''

n_night=len(night_arr)

if True:
    
    sp_arr=['0','1','2','3','4','5','6','7','8','9']
    cam_arr=['b','r','z']
    for i in range(n_night):
        night=night_arr[i]
        outdir='/global/project/projectdirs/desi/users/zhangkai/redux_one_exp/'+night
        cmd='mkdir '+outdir
        a=os.system(cmd)
        expid_arr=[expid]
        for expid in expid_arr:
            filename='/global/cfs/cdirs/desi/spectro/data/'+night+'/'+expid+'/desi-'+expid+'.fits.fz'
            try:
                h1=fits.getheader(filename,1)
                print(night,expid,h1['OBSTYPE'].lower())
                for cam in cam_arr:
                    for sp in sp_arr:
                        camera=cam+sp
                        cmd='desi_preproc -i $DESI_SPECTRO_DATA/'+night+'/'+expid+'/desi-'+expid+'.fits.fz -o '+outdir+'/'+expid+'/preproc-'+camera+'-'+expid+'.fits --cameras '+camera+' '+add_keyword
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


    

