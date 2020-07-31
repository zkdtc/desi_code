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


raw_dir=os.getenv('DESI_SPECTRO_DATA')

########## Long darks taken on 20200608-0609 ############

night_arr=['20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200609','20200608','20200608','20200608','20200608','20200608']
expid_arr=['00056872','00056880','00056881','00056882','00056883','00056884','00056885','00056886','00056887','00056888','00056889','00056890','00056891','00056892','00056893','00056894','00056895','00056896','00056897','00056898','00056899','00056900','00056901','00056902','00056903','00056904','00056905','00056906','00056907','00056908','00056909','00056910','00056911','00056868','00056848','00056828','00056664','00056644','00056624','00056617'] # 200s, 1200s
sp_arr=['0', '1','2','3','4','5','6','7','8','9']
sm_arr=['4','10','5','6','1','9','7','8','2','3']
cam_arr=['b','r','z']

### Regions to select ####
x1=0
x2=50
y1=1000
y2=1500

#camera='b0'
n_expid=len(expid_arr)
sec=True
if sec:
    output_file='check_dark_linearity_raw_sec.pdf'
else:
    output_file='check_dark_linearity_raw_'+str(x1)+'_'+str(x2)+'_'+str(y1)+'_'+str(y2)+'.pdf'

with PdfPages(output_file) as pdf:
    for cam in cam_arr:
        plt.figure(figsize=(12,10))
        font = {'family' : 'normal',
              'size'   : 16}
        plt.rc('font', **font)
        index=1
        for i in range(len(sp_arr)):
            sp=sp_arr[i]
            camera=cam+sp
            print(camera)
            x_arr=[]
            y_arr=[]
            for j in range(n_expid):
                night=night_arr[j]
                expid=expid_arr[j]
                file_raw=raw_dir+'/'+night+'/'+expid+'/desi-'+expid+'.fits.fz'
                try:
                    hdul1=fits.open(file_raw)
                    data=hdul1[camera]
                    
                except:
                    continue
                if sec:
                    x1,x2,y1,y2=[int(t) for t in data.header['ORSECA'][1:-1].replace(',',':').split(':')]
                nx=len(hdul1[camera].data)
                x_arr.append(hdul1[camera].header['EXPTIME'])
                y_arr.append(np.median(hdul1[camera].data[x1:x2,y1:y2]))

            if x_arr:
                x_arr=np.array(x_arr)
                y_arr=np.array(y_arr)
                print(x_arr,y_arr)
                plt.subplot(3,3,index)
                ind_fit=np.where(x_arr>150)
                plt.plot(x_arr,y_arr,'b+')
                if ind_fit:
                    z = np.polyfit(x_arr[ind_fit], y_arr[ind_fit], 1)
                    x=np.arange(1300)
                    #import pdb;pdb.set_trace()
                    plt.plot(x,z[1]+z[0]*x,color='blue')
                    y_fit=z[1]+z[0]*x_arr
                    #plt.plot(x_arr,y_arr-y_fit,'r+')
                    plt.text(500,0.3*(max(y_arr)-min(y_arr))+min(y_arr),'b='+str(z[1])[0:5])
                    plt.text(500,0.15*(max(y_arr)-min(y_arr))+min(y_arr),'slope='+str(z[0])[0:6])
                plt.xlabel('Exptime')
                plt.ylabel('Dark Current Counts')
                if index==2:
                    plt.title('Region:['+str(x1)+':'+str(x2)+','+str(y1)+':'+str(y2)+']')
                else:
                    plt.title(camera)
                index+=1
        
        plt.tight_layout()
        pdf.savefig()
        plt.close()


