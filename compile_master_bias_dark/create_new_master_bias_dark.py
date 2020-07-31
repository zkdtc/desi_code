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
import matplotlib.pyplot as plt

"""
###################################################
############# Usage Manual ########################
###################################################

* Pipeline for gnerating new bias+dark files

** Steps
1) Run "python3 generate_darks_list.py". Revise the nights to search first. It will give you a list of dark exposures ordered by exptime. Use this list as a reference for the exptime grid you want to compile: exptime_set_arr in step 2.

2) Revise the "night_arr=['20200607','20200608','20200609'] exptime_set_arr=[1200,900,...,0] in this code below. Then "python3 create_new_master_bias_dark.py". The code will search the raw images in the listed night folders for zeros and darks, group them by the exptime_set_arr. Then it will generates master bias+dark grid file for each camera. Make sure the filenmae contains 'bias' and 'dark', they are used to judge if the new bias+dark subtraction code in desispec/preproc.py will be used.

4) Copy all the master bias+dark files to $DESI_SPECTRO_CALIB/ccd/ . Update the yaml files under $DESI_SPECTRO_CALIB/spec/sm?/sm?-?.yaml to use the new bias+dark images as bias. Dark will be suppressed by codes in preproc.py when reading bias.

5) Remove temporary files master_bias_dark_{camera}_{exptime}.fits

"""
##########################################
############# Input ######################
##########################################

night_arr=['20200607','20200608','20200609']  # Nights to search for raw exposures.
exptime_set_arr=[1200,1000,900,700,450,400,350,300,280,260,240,220,200,180,160,140,120,100,90,80,70,60,50,40,30,20,10,9,8,7,6,5,4,3,2,1,0]  # Exposure time 37 point grid
exptime_set_arr=[1200,900,450,300,200,140,100,50,20,10,1,0]  # Exposure time 15 point grid

exp_reject=[''] # Exposure time to reject 
output_prefix='master-bias-dark-20200607-' # Final output file prefix. The output file will be output_prefix+camera+.fits
output_dir='' # output direcotry. If current directory, use ''. Otherwise, use 


night_arr=['20200728','20200729','20200730']
exptime_set_arr=[0,1,2,3,5,7,10,20,40,60,80,100,200,300,450,700,900,1200]

exp_reject=[''] # Exposure time to reject
output_prefix='master-bias-dark-20200728-' # Final output file prefix. The output file will be output_prefix+camera+.fits
output_dir='' # output direcotry. If current directory, use ''. Otherwise, use


sp_arr=['0', '1','2','3','4','5','6','7','8','9']
sm_arr=['4','10','5','6','1','9','7','8','2','3']
cam_arr=['b','r','z']
##############################################################################################
############### Search all exposures with a specific exptime and compile them ################
##############################################################################################
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
            cmd='desi_compute_bias -i '+filename_list+' -o '+output_dir+'master_bias_dark_'+camera+'_'+str(int(exptime_set))+'.fits --camera '+camera
            print(cmd)
            os.system(cmd)

##############################################################################################
############### Compile the exposures at a specific exptime to a single file  ################
##############################################################################################
print('Now compile the exposures at a specific exptime to a single file')

for cam in cam_arr:
    for sp in sp_arr:
        camera=cam+sp
        hdus = fits.HDUList()
        output=output_dir+output_prefix+camera+'.fits'
        print(camera)
        print(output)
        cutout_flux=[]
        try:
            for exptime_set in exptime_set_arr:
                filename=output_dir+'master_bias_dark_'+camera+'_'+str(int(exptime_set))+'.fits'
                hdu_this = fits.open(filename)
                """
                ## Compress to 8 or 16 bits ##
                #import pdb;pdb.set_trace()
                data=hdu_this[0].data
                index1=np.where(data>15)
                index2=np.where(data<-10)
                data[index1]=15
                data[index2]=-10
                #print(len(index))
                #data[index]=100000
                cutout_flux.append(np.median(data[4140:,2450:2550]))
                #plt.imshow(data[4140:,2450:2550],vmin=-10,vmax=100)
                plt.imshow(data,vmin=-10,vmax=15)
                plt.title(camera+' '+str(exptime_set)+'s')
                plt.colorbar()
                plt.show()
    
                plt.hist(data,100)
                plt.yscale('log')
                plt.title(camera+' '+str(exptime_set))
                plt.xlabel('Counts')
                plt.ylabel('N')
                plt.show()
                """
                ## Store the max and min in the header ##

                dataHDU = fits.ImageHDU(hdu_this[0].data, header=hdu_this[0].header, name=str(exptime_set))
                hdus.append(dataHDU)
            #plt.plot(exptime_set_arr,cutout_flux)
            #plt.xlabel('exptime')
            #plt.ylabel('Median Flux')
            #plt.show()
            hdus.writeto(output)
        except:
            pass


