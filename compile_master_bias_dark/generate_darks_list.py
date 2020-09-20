import argparse
import os
import fitsio
import astropy.io.fits as pyfits
from astropy.io import fits
import subprocess
import pandas as pd
import time
import numpy as np
import psycopg2
import hashlib
import pdb
from os import listdir

night_arr=['20200607','20200608','20200609']
#night_arr=['20200729']
#night_arr=['20200730']
night_arr=['20200728','20200729','20200730']
night_arr=['20200609']

expid_all=[]
exptime_all=[]
flavor_all=[]
night_all=[]

for night in night_arr:
    expid_arr=listdir(os.getenv('DESI_SPECTRO_DATA')+'/'+night+'/')
    expid_arr.sort(reverse=False)
    for expid in expid_arr:
        filename=os.getenv('DESI_SPECTRO_DATA')+'/'+str(night)+'/'+str(expid).zfill(8)+'/desi-'+str(expid).zfill(8)+'.fits.fz'
        try:
            h1=fits.getheader(filename,1)
        except:
            continue
        flavor=h1['flavor'].strip()
        exptime=h1['EXPTIME']
        print(expid,flavor,exptime)
        if flavor=='dark':
            expid_all.append(expid)
            exptime_all.append(exptime)
            flavor_all.append(flavor)
            night_all.append(night)



expid_all=np.array(expid_all)
exptime_all=np.array(exptime_all)
flavor_all=np.array(flavor_all)
night_all=np.array(night_all)
ind=np.argsort(exptime_all)
n=len(expid_all)
for i in range(n):
    ind_this=ind[i]
    print(night_all[ind_this],expid_all[ind_this],flavor_all[ind_this],exptime_all[ind_this])

output_str="expid_arr=["
output_str2="night_arr=["

for i in range(len(expid_all)):
    if i==0:
        output_str=output_str+"'"+expid_all[i]
        output_str2=output_str2+"'"+night_all[i]
    else:
        output_str=output_str+"','"+expid_all[i]
        output_str2=output_str2+"','"+night_all[i]
output_str=output_str+"']"
output_str2=output_str2+"']"


print(output_str2)

print(output_str)


