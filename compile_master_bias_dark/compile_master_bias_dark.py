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

exptime_set_arr=[1200,1000,900,700,450,400,350,300,280,260,240,220,200,180,160,140,120,100,90,80,70,60,50,40,30,20,10,9,8,7,6,5,4,3,2,1]
exp_reject=['']
sp_arr=['0', '1','2','3','4','5','6','7','8','9']
sm_arr=['4','10','5','6','1','9','7','8','2','3']
cam_arr=['b','r','z']


for cam in cam_arr:
    for sp in sp_arr:
        camera=cam+sp
        print(camera)
        hdus = fits.HDUList()
        output='master_bias_dark_'+camera+'.fits'
        try:
            for exptime_set in exptime_set_arr:
                filename='master_bias_dark_'+camera+'_'+str(int(exptime_set))+'.fits'
                hdu_this = fits.open(filename)
                dataHDU = fits.ImageHDU(hdu_this[0].data, header=hdu_this[0].header, name=str(exptime_set))
                hdus.append(dataHDU)
            hdus.writeto(output)
        except:
            pass



