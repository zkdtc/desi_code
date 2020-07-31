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

product='andes'
product1='extendwavelength'
night1='20200315'
expid1='00055589' # science
product2=product1
night2='20200315'
expid2='00055589' # science

redux_dir1=os.getenv('DESI_SPECTRO_REDUX')+'/'+product1+'/exposures/'+night1+'/'+expid1+'/'
redux_dir2=os.getenv('DESI_SPECTRO_REDUX')+'/'+product2+'/exposures/'+night2+'/'+expid2+'/backup/'


sp_arr=['0']#, '1','2','3','4','5','6','7','8','9']
sm_arr=['4','10','5','6','1','9','7','8','2','3']
cam_arr=['b']#,'r','z']
fiber_arr=np.arange(5)*100
#camera='b0'
nn=0
color_arr=['red','orange','yellow','green','blue','purple']
n_color=len(color_arr)

with PdfPages('check_two_spectra_'+expid1+'_'+expid2+'.pdf') as pdf:
    for cam in cam_arr:

        plt.figure(figsize=(12,22))
        font = {'family' : 'normal',
             'size'   : 16}
        plt.rc('font', **font)
        plt.subplot(2,1,1)

        for i in range(len(sp_arr)):
            sp=sp_arr[i]
            camera=cam+sp
            print(camera)
            file_frame1=redux_dir1+'/frame-'+camera+'-'+expid1+'.fits'
            file_frame2=redux_dir2+'/frame-'+camera+'-'+expid2+'.fits'
            try:
                hdul1=fits.open(file_frame1)
                hdul2=fits.open(file_frame2)
            except:
                continue
            wave1=hdul1['WAVELENGTH'].data
            wave2=hdul2['WAVELENGTH'].data
            for fiber in fiber_arr:
                smooth_len=21
                flux1=hdul1['FLUX'].data[fiber]
                sn1=flux1*np.sqrt(hdul1['IVAR'].data[fiber])
                # Filter the data, and plot both the original and filtered signals.
                flux_smooth1= savgol_filter(flux1, smooth_len, 3)
                sn_smooth1=savgol_filter(sn1, smooth_len, 3)

                flux2=hdul2['FLUX'].data[fiber]
                sn2=flux2*np.sqrt(hdul2['IVAR'].data[fiber])
                # Filter the data, and plot both the original and filtered signals.
                flux_smooth2= savgol_filter(flux2, smooth_len, 3)
                sn_smooth2=savgol_filter(sn2, smooth_len, 3)

                #plt.plot(wave1,flux1,color=color_arr[nn%n_color],label='frame')
                plt.plot(wave1,flux_smooth1,color=color_arr[nn%n_color],label='frame')
                #plt.plot(wave1,sn_smooth1,'--',label='S/N')
                #plt.plot(wave2,flux2,'--',color=color_arr[nn%n_color],label='frame')
                plt.plot(wave2,flux_smooth2,'--',color=color_arr[nn%n_color],label='frame')
                #plt.plot(wave2,sn_smooth2,'--',label='S/N')
                nn+=1



            plt.axis([min(wave1)-10,min(wave1)+300,-50,50])
            plt.yscale('linear')
            #plt.yscale('log')
            plt.xlabel('Wavelength')
            plt.ylabel('Flux')
            plt.title(expid1+' vs '+expid2)
            #plt.legend(loc=0)

        pdf.savefig()
        plt.close()


