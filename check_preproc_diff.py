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

######## Zeros ########
preproc_dir1='/global/project/projectdirs/desi/users/zhangkai/redux_zeros/'
preproc_dir2=preproc_dir1

night1='20200305'
expid1='00053190'

#night1='20200315'
#expid1='00055554'

night2='20200315'
expid2='00055555'
########## Darks 
preproc_dir1='/global/project/projectdirs/desi/users/zhangkai/redux_nodark/'
preproc_dir2=preproc_dir1

night1='20200609' # 1200s darks
expid1='00056841'
night2='20200609'
expid2='00056842'

night1='20200608' # 900s darks
expid1='00056624'
night2='20200608'
expid2='00056628'

night1='20200609' # 100s darks
expid1='00056873'
night2='20200609'
expid2='00056897'

night1='20200609' # 1s darks
expid1='00056870'
night2='20200609'
expid2='00056869'

night1='20200608' # 0s bias
expid1='00056619'
night2='20200608'
expid2='00056620'

sp_arr=['0', '1','2','3','4','5','6','7','8','9']
sm_arr=['4','10','5','6','1','9','7','8','2','3']
cam_arr=['b','r','z']
### Regions selected for comparison
x1=0
x2=50
y1=500
y2=1500

with PdfPages('check_preproc_diff_'+expid1+'_'+expid2+'_'+str(x1)+':'+str(x2)+','+str(y1)+':'+str(y2)+'.pdf') as pdf:
    for cam in cam_arr:
        plt.figure(figsize=(12,12))
        font = {'family' : 'normal',
             'size'   : 16}
        plt.rc('font', **font)
        index=1
        for i in range(len(sp_arr)):
            sp=sp_arr[i]
            camera=cam+sp
            print(camera)

            file_preproc1=preproc_dir1+'/'+night1+'/'+expid1+'/preproc-'+camera+'-'+expid1+'.fits'
            file_preproc2=preproc_dir2+'/'+night2+'/'+expid2+'/preproc-'+camera+'-'+expid2+'.fits'
            file_preproc1_flip=preproc_dir1+'/'+night1+'/'+expid1+'/preproc-'+expid1+'-'+camera+'.fits'
            file_preproc2_flip=preproc_dir2+'/'+night2+'/'+expid2+'/preproc-'+expid2+'-'+camera+'.fits'

            print('Try1')
            #import pdb;pdb.set_trace()
            try:
                hdul1=fits.open(file_preproc1)
                hdul2=fits.open(file_preproc2)
            except:
                try:
                    hdul1=fits.open(file_preproc1_flip)
                    hdul2=fits.open(file_preproc2_flip)
                except:
                    continue
            nx=len(hdul1[0].data)
            x=np.arange(nx)
            diff=hdul1[0].data[x1:x2,y1:y2]-hdul2[0].data[x1:x2,y1:y2]
            plt.subplot(4,3,index)
            #import pdb;pdb.set_trace()
            n, bins, patches = plt.hist(diff.ravel(), 40, range=(-20,20),alpha=0.5)
            if index==2:
                plt.title(camera+' Region ['+str(x1)+':'+str(x2)+','+str(y1)+':'+str(y2)+']')
            else:
                plt.title(camera)
            plt.text(5, max(n)*0.85, 'median='+str(np.median(diff))[0:5],fontsize=10)
            plt.xlabel('Count Difference')
            plt.ylabel('N')
            index+=1
          
        plt.tight_layout()
        pdf.savefig()
        plt.close()


