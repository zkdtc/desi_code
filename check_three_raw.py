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


raw_dir1=os.getenv('DESI_SPECTRO_DATA')
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

night2='20191231'
expid2='00037053' # zero

night='20191110'
expid='00026967'
label1='zero'
night2='20191110'
expid2='00026341' # dark
label2='dark'
night3='20191110'
expid3='00026971' # arc
label3='arc'
add='zero_arc_dark'

night='20200110'
expid='00039276'
label1='first zero'
night2='20200110'
expid2='00039299'
label2='middle zero'
night3='20200110'
expid3='00039317'
label3='last zero'
add='zero_same_night'

night='20200315'
expid='00055555'
label1='20200315 zero'
night2='20200110'
expid2='00039373'
label2='20200110 zero'
night3='20191110'
expid3='00026966'
label3='20191110 zero'
add='zero_different_night'
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
########## Long darks ############
night='20191110'
expid='00026341' # dark
add='dark'
zmax=50
"""

sp_arr=['0', '1','2','3','4','5','6','7','8','9']
sm_arr=['4','10','5','6','1','9','7','8','2','3']
cam_arr=['b','r','z']

#camera='b0'
file_raw1=raw_dir1+'/'+night+'/'+expid+'/desi-'+expid+'.fits.fz'
hdul1=fits.open(file_raw1)
file_raw2=raw_dir1+'/'+night2+'/'+expid2+'/desi-'+expid2+'.fits.fz'
try:
    hdul2=fits.open(file_raw2)
except:
    pass
file_raw3=raw_dir1+'/'+night3+'/'+expid3+'/desi-'+expid3+'.fits.fz'
try:
    hdul3=fits.open(file_raw3)
except:
    pass

with PdfPages('check_three_raw_'+night+'_'+add+'.pdf') as pdf:
    for cam in cam_arr:
        for i in range(len(sp_arr)):
            plt.figure(figsize=(12,22))
            font = {'family' : 'normal',
                 'size'   : 16}
            plt.rc('font', **font)
            sp=sp_arr[i]
            camera=cam+sp
            print(camera)

            file_raw1=raw_dir1+'/'+night+'/'+expid+'/desi-'+expid+'.fits.fz'
            try:
                hdul_this=hdul1[camera.upper()]
            except:
                continue
            try:
                hdul_this2=hdul2[camera.upper()]
            except:
                pass
            try:
                hdul_this3=hdul3[camera.upper()]
            except:
                pass

            nx=len(hdul_this.data)
            x=np.arange(nx)
            y_hat1 = np.median(hdul_this.data[:,1000:2000],axis=1)
            y_hat2=np.median(hdul_this.data[1000:2000,:],axis=0)
            try:
                y_hat3 = np.median(hdul_this2.data[:,1000:2000],axis=1)
                y_hat4=np.median(hdul_this2.data[1000:2000,:],axis=0)
            except:
                pass
            try:
                y_hat5 = np.median(hdul_this3.data[:,1000:2000],axis=1)
                y_hat6=np.median(hdul_this3.data[1000:2000,:],axis=0)
            except:
                pass

            # Filter the data, and plot both the original and filtered signals.
            #y_filter = butter_lowpass_filter(y_hat1, cutoff, fs, order)
            y_filter= savgol_filter(y_hat1, 101, 2)

            plt.subplot(3,1,1)
            plt.plot(x,y_hat1,label=label1)
            try:
                plt.plot(x,y_hat3,label=label2)
            except:
                pass
            try:
                plt.plot(x,y_hat5,label=label3)
            except:
                pass
            #plt.plot(x,y_filter,color='red',label='Fitered')
            plt.axis([-20,4200,np.median(y_hat1)-20,max(y_hat1)+10])
            plt.yscale('linear')
            #plt.yscale('log')
            plt.xlabel('CCD row')
            plt.ylabel('electron/pix')
            plt.title(expid+' '+camera)
            plt.legend(loc=0)

            plt.subplot(3,1,2)
            plt.plot(y_hat2,label=label1)
            try:
                plt.plot(y_hat4,label=label2)
            except:
                pass
            try:
                plt.plot(y_hat6,label=label3)
            except:
                pass

            plt.axis([-20,4300,np.median(y_hat2)-20,max(y_hat2)+10])
            plt.yscale('linear')
            #plt.yscale('log')
            plt.xlabel('CCD column')
            plt.ylabel('electron/pix')
            plt.title(expid+' '+camera)
            plt.legend(loc=0)

            plt.subplot(3,1,3)
            plt.imshow(hdul_this.data,vmin=np.median(y_hat1)-20,vmax=max(y_hat1)+10)
            plt.title(expid+' '+camera)
            plt.colorbar()
            pdf.savefig()
            plt.close()


