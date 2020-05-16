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

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Filter requirements.
order = 3
fs = 10.0       # sample rate, Hz
cutoff = 0.1# 3.667  # desired cutoff frequency of the filter, Hz

# Get the filter coefficients so we can check its frequency response.
b, a = butter_lowpass(cutoff, fs, order)


preproc_dir2='/project/projectdirs/desi/spectro/redux/daily/preproc/'
preproc_dir1='//global/project/projectdirs/desi/users/zhangkai/redux_one_exp/'
####################################################
# Perffect night 20200315 before covid-19 shutdown
####################################################
night='20200315'
expid='00055709' # arc
add='arc'
zmax=5
expid='00055589' # science
add='science'
zmax=5
expid='00055556' # twilight
add='twilight'
zmax=20
#expid='00055713' # flat
#add='flat'
#zmax=20
expid='00055555' # zero
add='zero'
zmax=5
"""
####################################################
# arcs with different exposure time  
####################################################
night='20191126'
expid='00030174' # 60s arc
add='arc_60s'
zmax=5
night='20191202'
expid='00030507' # 1200s arc
add='arc_1200s'
zmax=20
expid='00030524' # 5s arc
add='arc_5s'
zmax=20

night='20191205'
expid='00030784'
add='arc_120s'
zmax=20

night='20191206'
expid='00030847'
add='arc_10s'
zmax=20
#expid='00030842'
#add='arc_5s'
#zmax=20

night='20191216'
expid='00032722'
add='arc_5s'
zmax=20

night='20200131'
expid='00045433'
add='arc_10s'
zmax=5
expid='00045428'
add='arc_5s'
zmax=5

########## Old zeros on 20191231 ############
night='20191231'
expid='00037053' # zero
add='zero'
zmax=5
########## Old arcs on 20191212 ############
night='20191212'
expid='00031357' # arc
add='arc'
zmax=5
"""
########## Long darks ############
night='20191110'
expid='00026341' # dark
add='dark'
zmax=5
sp_arr=['0', '1','2','3','4','5','6','7','8','9']
sm_arr=['4','10','5','6','1','9','7','8','2','3']
cam_arr=['b','r','z']

#camera='b0'
with PdfPages('check_scattered_light_'+night+'_'+add+'.pdf') as pdf:
    for cam in cam_arr:
        for i in range(len(sp_arr)):
            plt.figure(figsize=(12,22))
            font = {'family' : 'normal',
                 'size'   : 16}
            plt.rc('font', **font)
            sp=sp_arr[i]
            camera=cam+sp
            print(camera)

            file_preproc1=preproc_dir1+'/'+night+'/'+expid+'/preproc-'+camera+'-'+expid+'.fits'
            file_dark='/project/projectdirs/desi/spectro/desi_spectro_calib/trunk/ccd/dark-sm'+sm_arr[i]+'-'+cam+'-20191021.fits'
            file_dark2='/project/projectdirs/desi/spectro/desi_spectro_calib/trunk/ccd/dark-sm'+sm_arr[i]+'-'+cam+'-20200209.fits'
            file_bias='/project/projectdirs/desi/spectro/desi_spectro_calib/trunk/ccd/bias-sm'+sm_arr[i]+'-'+cam+'-20191021.fits'
            file_bias2='/project/projectdirs/desi/spectro/desi_spectro_calib/trunk/ccd/bias-sm'+sm_arr[i]+'-'+cam+'-20200123.fits'
            file_preproc2=''#preproc_dir2+'/'+night+'/'+expid+'/preproc-'+camera+'-'+expid+'.fits'
            print('Try1')
            try:
                hdul1=fits.open(file_preproc1)
                try:
                    hdul_dark=fits.open(file_dark)
                except:
                    hdul_dark=fits.open(file_dark2)
                try:
                    hdul_bias=fits.open(file_bias)
                except:
                    hdul_bias=fits.open(file_bias2)
            except:
                continue
            nx=len(hdul1[0].data)
            x=np.arange(nx)
            y_hat1 = np.median(hdul1[0].data[:,1400:2400],axis=1)
            y_hat3=np.median(hdul1[0].data[1400:2400,:],axis=0)
            y_dark=np.median(hdul_dark[0].data[:,1400:2400],axis=1)*hdul1[0].header['EXPTIME']
            y_bias=np.median(hdul_bias[0].data[:,1400:2400],axis=1)

            # Filter the data, and plot both the original and filtered signals.
            #y_filter = butter_lowpass_filter(y_hat1, cutoff, fs, order)
            y_filter= savgol_filter(y_hat1, 101, 2)
            print('Try2')
            try:
                hdul2=fits.open(file_preproc2)
                y_hat2 = np.median(hdul2[0].data[:,1400:2400],axis=1)
                y_hat4=np.median(hdul2[0].data[1400:2400,:],axis=0)
            except:
                pass

            plt.subplot(3,1,1)
            plt.plot(x,y_hat1,label='With scattered light')
            plt.plot(x,y_dark,label='master dark*exptime',color='black')
            plt.plot(y_bias,label='master bias',color='red')

            print('Try3')
            try:
                plt.plot(x,y_hat2,label='scattered light remove on')
            except:
                pass
            #plt.plot(x,y_filter,color='red',label='Fitered')
            plt.axis([0,4200,0,zmax])
            plt.yscale('linear')
            #plt.yscale('log')
            plt.xlabel('CCD row')
            plt.ylabel('electron/pix')
            plt.title(expid+' '+camera)
            plt.legend(loc=0)

            plt.subplot(3,1,2)
            plt.plot(y_hat3,label='With scattered light')
            print('Try4')
            try:
                plt.plot(y_hat4,label='scattered light remove on')
            except:
                pass
            plt.axis([0,4200,0,zmax])
            plt.yscale('linear')
            #plt.yscale('log')
            plt.xlabel('CCD column')
            plt.ylabel('electron/pix')
            plt.title(expid+' '+camera)
            plt.legend(loc=0)

            plt.subplot(3,1,3)
            plt.imshow(hdul1[0].data,vmin=0,vmax=zmax)
            plt.title(expid+' '+camera)
            plt.colorbar()
            pdf.savefig()
            plt.close()


