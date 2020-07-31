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
product='extendwavelength'
night='20200315'
expid='00055589' # science

redux_dir=os.getenv('DESI_SPECTRO_REDUX')+'/'+product+'/exposures_backup/'+night+'/'+expid+'/'


sp_arr=['0', '1','2','3','4','5','6','7','8','9']
sm_arr=['4','10','5','6','1','9','7','8','2','3']
cam_arr=['b']#,'r','z']
fiber_arr=np.arange(5)*100
#camera='b0'
with PdfPages('check_spectra_'+expid+'.pdf') as pdf:
    for cam in cam_arr:

        plt.figure(figsize=(12,22))
        font = {'family' : 'normal',
             'size'   : 16}
        plt.rc('font', **font)
        plt.subplot(3,1,1)

        for i in range(len(sp_arr)):
            sp=sp_arr[i]
            camera=cam+sp
            print(camera)
            file_frame=redux_dir+'/flatfielded-frame-'+camera+'-'+expid+'.fits'

            try:
                hdul1=fits.open(file_frame)
            except:
                continue
            wave=hdul1['WAVELENGTH'].data
            for fiber in fiber_arr:
                flux=hdul1['FLUX'].data[fiber]
                sn=flux*np.sqrt(hdul1['IVAR'].data[fiber])


                # Filter the data, and plot both the original and filtered signals.
                flux_smooth= savgol_filter(flux, 51, 3)
                sn_smooth=savgol_filter(sn, 51, 3)
                
                plt.plot(wave,flux_smooth,label='frame')
                plt.plot(wave,sn_smooth,'--',label='S/N')
                #plt.plot(wave,flux_smooth,label='smoothed')

            plt.axis([min(wave)-10,min(wave)+100,-3,30])
            plt.yscale('linear')
            #plt.yscale('log')
            plt.xlabel('Wavelength')
            plt.ylabel('Flux')
            plt.title(expid)
            #plt.legend(loc=0)

        pdf.savefig()
        plt.close()


