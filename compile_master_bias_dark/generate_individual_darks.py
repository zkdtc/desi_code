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
exptime_set_arr=[0]#[1200,1000,900,700,450,400,350,300,280,260,240,220,200,180,160,140,120,100,90,80,70,60,50,40,30,20,10,9,8,7,6,5,4,3,2,1]
exp_reject=['']
sp_arr=['0', '1','2','3','4','5','6','7','8','9']
sm_arr=['4','10','5','6','1','9','7','8','2','3']
cam_arr=['b','r','z']


for exptime_set in exptime_set_arr:
    
    filename_list=''
    print('Searching exptime='+str(exptime_set)+' exposures.\n')

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

            if((str(expid).zfill(8) not in exp_reject) and (flavor=='zero' or flavor=='dark') and (int(exptime)==int(exptime_set))):
                print(expid,flavor,exptime)
                filename_list=filename_list+filename+' '



    for cam in cam_arr:
        for sp in sp_arr:
            camera=cam+sp
            cmd='desi_compute_bias -i '+filename_list+' -o '+'master_bias_dark_'+camera+'_'+str(int(exptime_set))+'.fits --camera '+camera
            print(cmd)
            os.system(cmd)



