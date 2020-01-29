import json
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

#date_arr=['20191111','20191111','20191111','20191111','20191111','20191111','20191112']
expnum_arr=['00027278','00027281','00027282','00027297','00027299','00027301','00027405']
#expnum_arr=['00027410','00027412','00027413','00027415']
cam_arr=['b','r','z']
num_arr=['0','1','2','3','4','5','6','7']
tail=''
"""
expnum_arr=['00022536'] #,'00022549','00022543','00022546','00022577','00022580','00022583','00022586']
cam_arr=['b','r','z']
num_arr=['3']
tail=''
"""
n_sp=len(num_arr)
n_exp=len(expnum_arr)
for i in range(n_exp):
    expnum=expnum_arr[i]

    try:
        index=1
        plt.figure(0,figsize=(12,10))
        font = {'family' : 'sans-serif',
                           'weight' : 'normal',
                           'size'   : 10}
        plt.rc('font', **font)

        for num in num_arr:
            for cam in cam_arr:
                with open('frame-'+cam+num+'-'+expnum+'.fits'+tail+'.dat') as json_file:
                    data=json.load(json_file)
                wave=data['wave']
                std_sky=np.nan_to_num(data['std_sky'])
                std_sky_hat = savgol_filter(std_sky, 51, 3)
                stds=np.nan_to_num(data['stds'])
                erms1=data['erms1']
                print(cam+num,np.median(std_sky))
                cmd='plt.subplot(33'+str(index)+')'
                a=exec(cmd)
                tx1=str(np.median(std_sky))[0:4]
                if cam == 'b':
                    color='blue'
                    xt=3800
                    tx1='median='+tx1
                elif cam=='r':
                    color='green'
                    xt=6500
                else:
                    color='red'
                    xt=8500
                yt=7.
                plt.plot(wave,std_sky,color=color,alpha=0.6)
                plt.plot(wave,std_sky_hat,color='k',alpha=0.5)
                plt.axis([3500,10000,-1,10])
                plt.text(4000,9,'sp'+num)
                plt.text(xt,yt,tx1)
                if index==2 or n_sp<2:
                    plt.title('Expnum '+expnum)
                elif index==4 or n_sp<2:
                    plt.ylabel('100*STD(Residual)/Sky')
                elif index==8 or n_sp<2:
                    plt.xlabel('Wavelength')
            index+=1
        plt.tight_layout()
        plt.savefig('std_sky_'+expnum+tail+'.pdf',format='pdf')
        plt.close()
    except:
        pass


for i in range(n_exp):
    expnum=expnum_arr[i]

    try:
        index=1
        plt.figure(0,figsize=(12,10))
        font = {'family' : 'sans-serif',
                           'weight' : 'normal',
                           'size'   : 10}
        plt.rc('font', **font)

        for num in num_arr:
            for cam in cam_arr:
                with open('frame-'+cam+num+'-'+expnum+'.fits'+tail+'.dat') as json_file:
                    data=json.load(json_file)

                wave=data['wave']
                median_flux=data['median_flux']
                std_sky=np.nan_to_num(data['std_sky'])
                std_sky_hat = savgol_filter(std_sky, 51, 3)
                stds=np.nan_to_num(data['stds'])
                erms1=data['erms1']
                print(cam+num,np.median(std_sky))
                cmd='plt.subplot(33'+str(index)+')'
                a=exec(cmd)
                tx1=str(np.median(std_sky))[0:4]
                if cam == 'b':
                    color='blue'
                    xt=3800
                    tx1='median='+tx1
                elif cam=='r':
                    color='green'
                    xt=6500
                else:
                    color='red'
                    xt=8500
                yt=7.

                plt.plot(median_flux,std_sky,'+',color=color,alpha=0.6)
                #plt.plot(median_flux,std_sky_hat,color='k',alpha=0.5)
                plt.axis([15,50000,-1,20])
                plt.xscale('log')
                #plt.text(4000,9,'sp'+num)
                #plt.text(xt,yt,tx1)
                if index==2 or n_sp<2:
                    plt.title('Expnum '+expnum)
                elif index==4 or n_sp<2:
                    plt.ylabel('100*STD(Residual)/Sky')
                elif index==8 or n_sp<2:
                    plt.xlabel('Median Flux')
            index+=1
        plt.tight_layout()
        plt.savefig('std_sky_median_flux_'+expnum+tail+'.pdf',format='pdf')
        plt.close()
    except:
        pass

for i in range(n_exp):
    expnum=expnum_arr[i]

    try:
        index=1
        plt.figure(0,figsize=(12,10))
        font = {'family' : 'sans-serif',
                           'weight' : 'normal',
                           'size'   : 10}
        plt.rc('font', **font)

        for num in num_arr:
            for cam in cam_arr:
                with open('frame-'+cam+num+'-'+expnum+'.fits'+tail+'.dat') as json_file:
                    data=json.load(json_file)

                wave=data['wave']
                median_flux=data['median_flux']
                std_sky=np.nan_to_num(data['std_sky'])
                std_sky_hat = savgol_filter(std_sky, 51, 3)
                stds=np.nan_to_num(data['stds'])
                erms1=data['erms1']
                print(cam+num,np.median(std_sky))
                cmd='plt.subplot(33'+str(index)+')'
                a=exec(cmd)
                tx1=str(np.median(std_sky))[0:4]
                if cam == 'b':
                    color='blue'
                    xt=3800
                    tx1='median='+tx1
                elif cam=='r':
                    color='green'
                    xt=6500
                else:
                    color='red'
                    xt=8500
                yt=7.

                plt.plot(wave,median_flux,color=color,alpha=0.6)
                plt.axis([3500,10000,15,50000])
                plt.yscale('log')
                #plt.text(4000,9,'sp'+num)
                #plt.text(xt,yt,tx1)
                if index==2 or n_sp<2:
                    plt.title('Expnum '+expnum)
                elif index==4 or n_sp<2:
                    plt.ylabel('100*STD(Residual)/Sky')
                elif index==8 or n_sp<2:
                    plt.xlabel('Median Flux')
            index+=1
        plt.tight_layout()
        plt.savefig('std_sky_wave_flux_'+expnum+tail+'.pdf',format='pdf')
        plt.close()
    except:
        pass

