from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from os import listdir
import pdb
from matplotlib.backends.backend_pdf import PdfPages
from scipy.signal import butter, lfilter, freqz
from scipy.signal import savgol_filter


night="20200609"
camera_arr=["b0","b1","b2","r0","r1","r2","z0","z1","z2","b3","b4","b5","r3","r4","r5","z3","z4","z5","b6","b7","b8","b9","r6","r7","r8","r9","z6","z7","z8","z9"]
exptime_arr=[1,          2,         3,          4,         5,       6,          7,         8,         9,         10,       15,          20,      30,        40,         50,        60,        70,        80,       90,        100,       120,       140,        160,      180,     220,     240,       260,     280,      300,        350,    400,       450,      700,    1000,      1200]
expid_arr=["00056872","00056880","00056881","00056882","00056848","00056884","00056885","00056886","00056887","00056888","00056878","00056889","00056874","00056932","00056892","00056947","00056950","00056895","00056962","00056963","00056898","00056980","00056900","00056988","00056902","00056903","00056904","00056905","00056906","00056907","00056908","00056909","00056910","00056911","00056861"]

appendix='old'
preproc_dir1="/global/project/projectdirs/desi/users/zhangkai/redux_"+appendix+"bias/"
zmax=2
sp_arr=['0', '1','2','3','4','5','6','7','8','9']
sm_arr=['4','10','5','6','1','9','7','8','2','3']
cam_arr=['b','r','z']


for camera in camera_arr:
    with PdfPages('check_many_darks_to_verify_'+camera+'_'+appendix+'.pdf') as pdf:
        for expid,exptime in zip(expid_arr,exptime_arr):
            print(camera,expid,exptime)

            plt.figure(figsize=(18,18))
            font = {'family' : 'normal',
                 'size'   : 16}
            plt.rc('font', **font)

            file_preproc1=preproc_dir1+'/'+night+'/'+expid+'/preproc-'+camera+'-'+expid+'.fits'
            try:
                hdul1=fits.open(file_preproc1)
            except:
                continue
            nx=len(hdul1[0].data)
            x=np.arange(nx)
            y_hat1 = np.median(hdul1[0].data[:,1000:1500],axis=1)
            y_hat2 = np.median(hdul1[0].data[:,2500:3000],axis=1)
            y_hat3=np.median(hdul1[0].data[1000:1500,:],axis=0)
            y_hat4=np.median(hdul1[0].data[2500:3000,:],axis=0)


            # Filter the data, and plot both the original and filtered signals.
            #y_filter = butter_lowpass_filter(y_hat1, cutoff, fs, order)
            y_filter= savgol_filter(y_hat1, 101, 2)

            plt.subplot(2,2,1)
            plt.plot(x,y_hat1,label='[1000:1500] column median')
            plt.plot(x,y_hat2,label='[2500:3000] column median')
            plt.title('EXPID:'+expid+' EXPTIME='+str(hdul1[0].header['EXPTIME']))
            plt.axis([0,4200,-1,zmax])
            plt.yscale('linear')
            #plt.yscale('log')
            plt.xlabel('CCD row')
            plt.ylabel('electron/pix')
            plt.title(expid+' '+camera+' EXPTIME='+str(hdul1[0].header['EXPTIME']))
            plt.legend(loc=0)

            plt.subplot(2,2,2)
            plt.plot(y_hat3,label='[1000:1500] row median')
            plt.plot(y_hat4,label='[2500:3000] row median')
            plt.axis([0,4200,-1,zmax])
            plt.yscale('linear')
            #plt.yscale('log')
            plt.xlabel('CCD column')
            plt.ylabel('electron/pix')
            plt.title(expid+' '+camera)
            plt.legend(loc=0)

            plt.subplot(2,2,3)
            plt.imshow(hdul1[0].data,vmin=-1,vmax=zmax)
            plt.title(expid+' '+camera)
            plt.colorbar()
            
            data1d=hdul1[0].data.ravel()
            std=np.std(data1d[(data1d<10) & (data1d>-10)])

            plt.subplot(2,2,4)
            plt.hist(hdul1[0].data.ravel(),30,range=(-10,10),alpha=0.5)
            plt.title('Std='+str(std)[0:4])
            plt.colorbar()

            plt.tight_layout()
            pdf.savefig()
            plt.close()


