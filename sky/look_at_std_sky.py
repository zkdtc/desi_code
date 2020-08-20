import json
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter

#date_arr=['20191111','20191111','20191111','20191111','20191111','20191111','20191112']
expnum_arr=['00027278']#,'00027281','00027282','00027297','00027299','00027301','00027405']
#expnum_arr=['00027410','00027412','00027413','00027415']
cam_arr=['b','r','z']
num_arr=['0','1','2','3','4','5','6','7']
tail=''
"""
expnum_arr=['00022536'] #,'00022549','00022543','00022546','00022577','00022580','00022583','00022586']
cam_arr=['b','r','z']
num_arr=['3']
tail=''

expnum_arr=['00050988','00050995']
expnum_arr=['00053127','00053128','53129']
cam_arr=['b','r','z']
num_arr=['0','3','6','7','9']
#sm_num_arr=['4','6','7','8','3']
tail='_skyonly'
"""

expnum_arr=['00055590']
#expnum_arr=['00055643'] #['00055589','00055590','00055591','00055592','00055593','00055594']#,'00055611','00055612','00055613','00055626','00055627','00055628','00055639','00055640','00055641','00055642','00055643']

#expnum_arr=['00053743']
cam_arr=['z','r','b']
num_arr=['0','1','2','3','4','5','6','7','8','9']
#num_arr=['0','3','6','7','9']
#sm_num_arr=['4','6','7','8','3']
#tail='_skyonly' # normal product
tail='newbias_skyonly' # product newbias


expnum_arr_int=np.array(list(map(int, expnum_arr)))

sky_std_b=[]
sky_std_b0=[]
sky_std_b1=[]
sky_std_b2=[]
sky_std_b3=[]
sky_std_b4=[]
sky_std_b5=[]
sky_std_b6=[]
sky_std_b7=[]
sky_std_b8=[]
sky_std_b9=[]

sky_std_r=[]
sky_std_r0=[]
sky_std_r1=[]
sky_std_r2=[]
sky_std_r3=[]
sky_std_r4=[]
sky_std_r5=[]
sky_std_r6=[]
sky_std_r7=[]
sky_std_r8=[]
sky_std_r9=[]

sky_std_z=[]
sky_std_z0=[]
sky_std_z1=[]
sky_std_z2=[]
sky_std_z3=[]
sky_std_z4=[]
sky_std_z5=[]
sky_std_z6=[]
sky_std_z7=[]
sky_std_z8=[]
sky_std_z9=[]

median_flux_b0=[]
median_flux_b1=[]
median_flux_b2=[]
median_flux_b3=[]
median_flux_b4=[]
median_flux_b5=[]
median_flux_b6=[]
median_flux_b7=[]
median_flux_b8=[]
median_flux_b9=[]

median_flux_r0=[]
median_flux_r1=[]
median_flux_r2=[]
median_flux_r3=[]
median_flux_r4=[]
median_flux_r5=[]
median_flux_r6=[]
median_flux_r7=[]
median_flux_r8=[]
median_flux_r9=[]

median_flux_z0=[]
median_flux_z1=[]
median_flux_z2=[]
median_flux_z3=[]
median_flux_z4=[]
median_flux_z5=[]
median_flux_z6=[]
median_flux_z7=[]
median_flux_z8=[]
median_flux_z9=[]

stds_b0=[]
stds_b1=[]
stds_b2=[]
stds_b3=[]
stds_b4=[]
stds_b5=[]
stds_b6=[]
stds_b7=[]
stds_b8=[]
stds_b9=[]

stds_r0=[]
stds_r1=[]
stds_r2=[]
stds_r3=[]
stds_r4=[]
stds_r5=[]
stds_r6=[]
stds_r7=[]
stds_r8=[]
stds_r9=[]

stds_z0=[]
stds_z1=[]
stds_z2=[]
stds_z3=[]
stds_z4=[]
stds_z5=[]
stds_z6=[]
stds_z7=[]
stds_z8=[]
stds_z9=[]

errors_mean_b0=[]
errors_mean_b1=[]
errors_mean_b2=[]
errors_mean_b3=[]
errors_mean_b4=[]
errors_mean_b5=[]
errors_mean_b6=[]
errors_mean_b7=[]
errors_mean_b8=[]
errors_mean_b9=[]

errors_mean_r0=[]
errors_mean_r1=[]
errors_mean_r2=[]
errors_mean_r3=[]
errors_mean_r4=[]
errors_mean_r5=[]
errors_mean_r6=[]
errors_mean_r7=[]
errors_mean_r8=[]
errors_mean_r9=[]

errors_mean_z0=[]
errors_mean_z1=[]
errors_mean_z2=[]
errors_mean_z3=[]
errors_mean_z4=[]
errors_mean_z5=[]
errors_mean_z6=[]
errors_mean_z7=[]
errors_mean_z8=[]
errors_mean_z9=[]

n_sp=len(num_arr)
n_exp=len(expnum_arr)
for i in range(n_exp):
    expnum=expnum_arr[i]

    if True:
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
                median_flux=data['median_fflux']  # Notice I change to fflux here and after !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                std_sky=np.nan_to_num(data['std_sky'])
                print(std_sky)
                std_sky_hat = savgol_filter(std_sky, 51, 3)
                stds=np.nan_to_num(data['stds'])
                errors_mean=np.nan_to_num(data['errors_mean'])
                erms1=data['erms1']
                print(cam+num,np.median(std_sky_hat))
                cmd='sky_std_'+cam+num+'.append(np.median(std_sky_hat))'
                a=exec(cmd)
                cmd='median_flux_'+cam+num+'.append(np.median(median_flux))'
                a=exec(cmd)
                cmd='stds_'+cam+num+'.append(np.median(stds))'
                a=exec(cmd)
                cmd='errors_mean_'+cam+num+'.append(np.median(errors_mean))'
                a=exec(cmd)

                if cam=='b':
                    sky_std_b.append(np.median(std_sky_hat))
                elif cam == 'r':
                    sky_std_r.append(np.median(std_sky_hat))
                else:
                    sky_std_z.append(np.median(std_sky_hat))

                cmd='plt.subplot(4,3,'+str(index)+')'
                a=exec(cmd)
                tx1=str(100*np.sqrt(np.median(std_sky_hat)))[0:4]
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
                yt=0.05
                plt.plot(wave,std_sky,color=color,alpha=0.6)
                plt.plot(wave,std_sky_hat,color='k',alpha=0.5)
                plt.axis([3500,10000,-0.1,0.1])
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
    else:
        pass

for i in range(n_exp):
    expnum=expnum_arr[i]

    if True:
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
                median_flux=data['median_fflux']  # Notice I change to fflux here and after !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                std_sky=np.nan_to_num(data['std_sky'])
                print(std_sky)
                std_sky_hat = savgol_filter(std_sky, 51, 3)
                stds=np.nan_to_num(data['stds'])
                errors_mean=np.nan_to_num(data['errors_mean'])
                erms1=data['erms1']
                print(cam+num,np.median(std_sky_hat))
                tx1=str(100*np.sqrt(np.median(std_sky_hat)))[0:4]
                std_sky_hat=100*np.sqrt(std_sky_hat)
                cmd='plt.subplot(4,3,'+str(index)+')'
                a=exec(cmd)
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
                yt=0.05
                #plt.plot(wave,std_sky,color=color,alpha=0.6)
                plt.plot(wave,std_sky_hat,color=color,alpha=0.5)
                plt.axis([3500,10000,0,8])
                plt.text(4000,6,'sp'+num)
                plt.text(xt,yt,tx1)
                if index==2 or n_sp<2:
                    plt.title('Expnum '+expnum)
                elif index==4 or n_sp<2:
                    plt.ylabel('100*STD(Residual)/Sky')
                elif index==8 or n_sp<2:
                    plt.xlabel('Wavelength')
            index+=1
        plt.tight_layout()
        plt.savefig('std_sky_ratio_'+expnum+tail+'.pdf',format='pdf')
        plt.close()
    else:
        pass

for i in range(n_exp):
    expnum=expnum_arr[i]

    if True:
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
                median_flux=data['median_fflux']  # Notice I change to fflux here and after !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                std_sky=np.nan_to_num(data['std_sky'])
                print(std_sky)
                std_sky_hat = savgol_filter(std_sky, 51, 3)
                stds=np.nan_to_num(data['stds'])
                errors_mean=np.nan_to_num(data['errors_mean'])
                erms1=data['erms1']
                print(cam+num,np.median(std_sky_hat))
                tx1=str(100*np.sqrt(np.median(std_sky_hat)))[0:4]
                std_sky_hat=100*np.sqrt(std_sky_hat)
                cmd='plt.subplot(4,3,'+str(index)+')'
                a=exec(cmd)
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
                yt=0.05
                #plt.plot(wave,std_sky,color=color,alpha=0.6)
                plt.plot(median_flux,std_sky_hat,'+',color=color,alpha=0.5)
                plt.axis([0,5000,0,8])
                plt.text(400,6,'sp'+num)
                plt.text(xt,yt,tx1)
                if index==2 or n_sp<2:
                    plt.title('Expnum '+expnum)
                elif index==4 or n_sp<2:
                    plt.ylabel('100*STD(Residual)/Sky')
                elif index==8 or n_sp<2:
                    plt.xlabel('Wavelength')
            index+=1
        plt.tight_layout()
        plt.savefig('std_sky_ratio_vs_flux_'+expnum+tail+'.pdf',format='pdf')
        plt.close()
    else:
        pass



plt.figure(0,figsize=(12,4))
font = {'family' : 'sans-serif',
        'weight' : 'normal',
        'size'   : 10}
plt.rc('font', **font)
plt.subplot(1,3,1)
plt.hist(sky_std_b,20, density=True, facecolor='g', alpha=0.75)
plt.xlabel('B')
plt.ylabel('100*STD(Residual)/Sky')

plt.subplot(1,3,2)
plt.hist(sky_std_r,20, density=True, facecolor='g', alpha=0.75)
plt.xlabel('R')
plt.ylabel('100*STD(Residual)/Sky')

plt.subplot(1,3,3)
plt.hist(sky_std_z,20, density=True, facecolor='g', alpha=0.75)
plt.xlabel('Z')
plt.ylabel('100*STD(Residual)/Sky')

plt.tight_layout()
plt.savefig('sky_std_hist.pdf',format='pdf')
plt.close()


plt.figure(0,figsize=(12,10))
font = {'family' : 'sans-serif',
        'weight' : 'normal',
        'size'   : 10}
plt.rc('font', **font)
plt.subplot(3,3,1)
for num in num_arr:
    cmd='plt.plot(expnum_arr_int-expnum_arr_int[0],sky_std_b'+num+',label="b'+num+'")'
    a=exec(cmd)
plt.ylabel('(STD(Residual)**2-1/IVAR)/Sky**2')
plt.legend(loc=0)

plt.subplot(3,3,2)
for num in num_arr:
    cmd='plt.plot(expnum_arr_int-expnum_arr_int[0],sky_std_r'+num+',label="r'+num+'")'
    a=exec(cmd)
plt.xlabel('Expnum-'+str(expnum_arr_int[0]))
plt.legend(loc=0)

plt.subplot(3,3,3)
for num in num_arr:
    cmd='plt.plot(expnum_arr_int-expnum_arr_int[0],sky_std_z'+num+',label="z'+num+'")'
    a=exec(cmd)
plt.legend(loc=0)


plt.subplot(3,3,4)
for num in num_arr:
    cmd='plt.plot(expnum_arr_int-expnum_arr_int[0],median_flux_b'+num+',label="b'+num+'")'
    a=exec(cmd)
plt.ylabel('Median Flux')
plt.legend(loc=0)

plt.subplot(3,3,5)
for num in num_arr:
    cmd='plt.plot(expnum_arr_int-expnum_arr_int[0],median_flux_r'+num+',label="r'+num+'")'
    a=exec(cmd)
plt.xlabel('Expnum-'+str(expnum_arr_int[0]))
plt.legend(loc=0)

plt.subplot(3,3,6)
for num in num_arr:
    cmd='plt.plot(expnum_arr_int-expnum_arr_int[0],median_flux_z'+num+',label="z'+num+'")'
    a=exec(cmd)
plt.legend(loc=0)
plt.tight_layout()
plt.savefig('sky_std_time.pdf',format='pdf')
plt.close()




plt.figure(0,figsize=(12,10))
font = {'family' : 'sans-serif',
        'weight' : 'normal',
        'size'   : 10}
plt.rc('font', **font)
plt.subplot(3,3,1)
for num in num_arr:
    cmd='x = median_flux_b'+num
    a=exec(cmd)
    cmd='y = np.square(stds_b'+num+')'
    a=exec(cmd)
    z = np.polyfit(x, y, 1)
    cmd='plt.plot(median_flux_b'+num+',np.square(stds_b'+num+'),"+",label="b'+num+' y="+str(z[0])[0:4]+"x + "+str(z[1])[0:3])'
    a=exec(cmd)

plt.ylabel('(STD(Residual)**2')
plt.legend(loc=0)

plt.subplot(3,3,2)
for num in num_arr:
    channel='r'
    num=channel+num
    cmd='x = median_flux_'+num
    a=exec(cmd)
    cmd='y = np.square(stds_'+num+')'
    a=exec(cmd)
    z = np.polyfit(x, y, 1)
    cmd='plt.plot(median_flux_'+num+',np.square(stds_'+num+'),"+",label="'+num+' y="+str(z[0])[0:4]+"x + "+str(z[1])[0:3])'
    a=exec(cmd)

plt.xlabel('Median Flux')
plt.legend(loc=0)

plt.subplot(3,3,3)
for num in num_arr:
    channel='z'
    num=channel+num
    cmd='x = median_flux_'+num
    a=exec(cmd)
    cmd='y = np.square(stds_'+num+')'
    a=exec(cmd)
    z = np.polyfit(x, y, 1)
    cmd='plt.plot(x,y,"+",label="'+num+' y="+str(z[0])[0:4]+"x + "+str(z[1])[0:3])'
    a=exec(cmd)

plt.legend(loc=0)

plt.subplot(3,3,4)
for num in num_arr:
    channel='b'
    num=channel+num
    cmd='x = median_flux_'+num
    a=exec(cmd)
    cmd='y = errors_mean_'+num
    a=exec(cmd)
    z = np.polyfit(x, y, 1)
    cmd='plt.plot(x,y,"+",label="'+num+' y="+str(z[0])[0:4]+"x + "+str(z[1])[0:3])'
    a=exec(cmd)

plt.ylabel('1/IVAR')
plt.legend(loc=0)

plt.subplot(3,3,5)
for num in num_arr:
    channel='r'
    num=channel+num
    cmd='x = median_flux_'+num
    a=exec(cmd)
    cmd='y = errors_mean_'+num
    a=exec(cmd)
    z = np.polyfit(x, y, 1)
    cmd='plt.plot(x,y,"+",label="'+num+' y="+str(z[0])[0:4]+"x + "+str(z[1])[0:3])'
    a=exec(cmd)
plt.xlabel('Median Flux')
plt.legend(loc=0)

plt.subplot(3,3,6)
for num in num_arr:
    channel='z'
    num=channel+num
    cmd='x = median_flux_'+num
    a=exec(cmd)
    cmd='y = errors_mean_'+num
    a=exec(cmd)
    z = np.polyfit(x, y, 1)
    cmd='plt.plot(x,y,"+",label="'+num+' y="+str(z[0])[0:4]+"x + "+str(z[1])[0:3])'
    a=exec(cmd)
plt.legend(loc=0)



plt.subplot(3,3,7)
for num in num_arr:
    channel='b'
    num=channel+num
    cmd='x = median_flux_'+num
    a=exec(cmd)
    cmd='y = np.square(stds_'+num+')-errors_mean_'+num
    a=exec(cmd)
    z = np.polyfit(x, y, 1)
    cmd='plt.plot(x,y,"+",label="'+num+'")'
    a=exec(cmd)

plt.ylabel('STD(Residual)**2-1/IVAR')
plt.legend(loc=0)

plt.subplot(3,3,8)
for num in num_arr:
    channel='r'
    num=channel+num
    cmd='x = median_flux_'+num
    a=exec(cmd)
    cmd='y = np.square(stds_'+num+')-errors_mean_'+num
    a=exec(cmd)
    z = np.polyfit(x, y, 1)
    cmd='plt.plot(x,y,"+",label="'+num+'")'
    a=exec(cmd)

plt.xlabel('Median Flux')
plt.legend(loc=0)

plt.subplot(3,3,9)
for num in num_arr:
    channel='z'
    num=channel+num
    cmd='x = median_flux_'+num
    a=exec(cmd)
    cmd='y = np.square(stds_'+num+')-errors_mean_'+num
    a=exec(cmd)
    z = np.polyfit(x, y, 1)
    cmd='plt.plot(x,y,"+",label="'+num+'")'
    a=exec(cmd)

plt.legend(loc=0)

plt.tight_layout()
plt.savefig('stds_errors_flux.pdf',format='pdf')
plt.close()

from matplotlib.backends.backend_pdf import PdfPages

with PdfPages('all_errors_wavelength.pdf') as pdf:
    for i in range(n_exp):
        expnum=expnum_arr[i]
        index=1
        plt.figure(0,figsize=(12,10))
        font = {'family' : 'sans-serif',
                           'weight' : 'normal',
                           'size'   : 10}
        plt.rc('font', **font)
        
        for num in num_arr:
            cmd='plt.subplot(4,3,'+str(index)+')'
            a=exec(cmd)
            for cam in cam_arr:
                with open('frame-'+cam+num+'-'+expnum+'.fits'+tail+'.dat') as json_file:
                    data=json.load(json_file)

                wave=data['wave']
                median_flux=data['median_fflux']
                std_sky=np.nan_to_num(data['std_sky'])
                std_sky_hat = savgol_filter(std_sky, 51, 3)
                stds=np.nan_to_num(data['stds'])
                stds_hat = savgol_filter(stds, 51, 3)
                errors_mean=np.nan_to_num(data['errors_mean'])
                errors_mean_hat = savgol_filter(errors_mean, 51, 3)
                errors_res=np.square(stds)-errors_mean
                errors_res_hat = savgol_filter(errors_res, 51, 3)

                erms1=data['erms1']
                print(cam+num,np.median(std_sky_hat))
                tx1=str(np.median(std_sky_hat))[0:4]
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
                
                plt.plot(wave,errors_res,color=color,alpha=0.6)
                plt.plot(wave,errors_res_hat,color='k',alpha=0.6)
                plt.axis([3300,10000,-200,3000])
                if index==2 or n_sp<2:
                    plt.title('Expnum '+expnum)
                elif index==4 or n_sp<2:
                    plt.ylabel('STD(Residual)**2-1/IVAR')
                elif index==8 or n_sp<2:
                    plt.xlabel('Wavelength')
            index+=1
        pdf.savefig()  # saves the current figure into a pdf page
        plt.close()

with PdfPages('all_errors_flux.pdf') as pdf:
    for i in range(n_exp):
        expnum=expnum_arr[i]
        index=1
        plt.figure(0,figsize=(12,10))
        font = {'family' : 'sans-serif',
                           'weight' : 'normal',
                           'size'   : 10}
        plt.rc('font', **font)

        for num in num_arr:
            cmd='plt.subplot(4,3,'+str(index)+')'
            a=exec(cmd)
            for cam in cam_arr:
                with open('frame-'+cam+num+'-'+expnum+'.fits'+tail+'.dat') as json_file:
                    data=json.load(json_file)

                wave=data['wave']
                median_flux=data['median_fflux']
                window=11
                median_flux_hat=savgol_filter(median_flux, window, 3)
                std_sky=np.nan_to_num(data['std_sky'])
                std_sky_hat = savgol_filter(std_sky, window, 3)
                stds=np.nan_to_num(data['stds'])
                stds_hat = savgol_filter(stds, window, 3)
                errors_mean=np.nan_to_num(data['errors_mean'])
                errors_mean_hat = savgol_filter(errors_mean, window, 3)
                errors_res=np.square(stds)-errors_mean
                errors_res_hat = savgol_filter(errors_res, window, 3)

                erms1=data['erms1']
                print(cam+num,np.median(std_sky_hat))
                tx1=str(np.median(std_sky_hat))[0:4]
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

                plt.plot(median_flux_hat,errors_res_hat,'+',markersize=3,color=color,alpha=0.6)
                plt.axis([-200,1000,-200,1000])
                if index==2 or n_sp<2:
                    plt.title('Expnum '+expnum)
                elif index==4 or n_sp<2:
                    plt.ylabel('STD(Residual)**2-1/IVAR')
                elif index==8 or n_sp<2:
                    plt.xlabel('Median Flux')
            x_line=np.arange(10000)
            y1_line=np.square(0.01*x_line)
            y2_line=np.square(0.02*x_line)
            y5_line=np.square(0.05*x_line)
            plt.plot(x_line,y1_line,color='black',label='1% subtraction line')
            plt.plot(x_line,y2_line,'--',color='black',label='2%')
            plt.plot(x_line,y5_line,'-.',color='black',label='5%')
            plt.legend(loc=1)
            index+=1
        pdf.savefig()  # saves the current figure into a pdf page
        plt.close()


with PdfPages('res_stack.pdf') as pdf:
    for i in range(n_exp):
        expnum=expnum_arr[i]
        index=1
        plt.figure(0,figsize=(12,10))
        font = {'family' : 'sans-serif',
                           'weight' : 'normal',
                           'size'   : 10}
        plt.rc('font', **font)

        for num in num_arr:
            cmd='plt.subplot(4,3,'+str(index)+')'
            a=exec(cmd)
            for cam in cam_arr:
                with open('frame-'+cam+num+'-'+expnum+'.fits'+tail+'.dat') as json_file:
                    data=json.load(json_file)
                window=11
                wave=data['wave']
                median_flux=data['median_fflux']
                res_stack=data['res_stack']
                res_stack_hat=savgol_filter(res_stack, window, 3)
                if cam == 'b':
                    color='blue'
                    xt=3800
                elif cam=='r':
                    color='green'
                    xt=6500
                else:
                    color='red'
                    xt=8500
                yt=7.

                plt.plot(wave,res_stack,markersize=3,color=color,alpha=0.6)
                plt.axis([3300,10000,-5,20])
                if index==2 or n_sp<2:
                    plt.title('Expnum '+expnum)
                elif index==4 or n_sp<2:
                    plt.ylabel('Sky Residual')
                elif index==8 or n_sp<2:
                    plt.xlabel('Wavelength')
            index+=1
        pdf.savefig()  # saves the current figure into a pdf page
        plt.close()

with PdfPages('res_stack_subtract.pdf') as pdf:
    ### Use the first exposure as a template ###
    expnum=expnum_arr[0]
    for num in num_arr:
        for cam in cam_arr:
            with open('frame-'+cam+num+'-'+expnum+'.fits'+tail+'.dat') as json_file:
                data=json.load(json_file)
            cmd="wave0_"+cam+num+"=data['wave0']"
            a=exec(cmd)
            cmd="res_stack0_"+cam+num+"=np.array(data['res_stack0'])"
            a=exec(cmd)



    for i in range(n_exp-1):
        expnum=expnum_arr[i+1]
        index=1
        plt.figure(0,figsize=(12,10))
        font = {'family' : 'sans-serif',
                           'weight' : 'normal',
                           'size'   : 10}
        plt.rc('font', **font)

        for num in num_arr:
            cmd='plt.subplot(4,3,'+str(index)+')'
            a=exec(cmd)
            for cam in cam_arr:
                with open('frame-'+cam+num+'-'+expnum+'.fits'+tail+'.dat') as json_file:
                    data=json.load(json_file)
                window=11
                wave0=data['wave0']
                res_stack0=np.array(data['res_stack0'])
                res_stack_hat0=savgol_filter(res_stack0, window, 3)
                if cam == 'b':
                    color='blue'
                    xt=3800
                elif cam=='r':
                    color='green'
                    xt=6500
                else:
                    color='red'
                    xt=8500
                yt=7.

                cmd='plt.plot(wave0,res_stack0-res_stack0_'+cam+num+',markersize=3,color=color,alpha=0.6)'
                #import pdb;pdb.set_trace()
                a=exec(cmd)
                plt.axis([3300,10000,-5,20])
                if index==2 or n_sp<2:
                    plt.title('Expnum '+expnum)
                elif index==4 or n_sp<2:
                    plt.ylabel('Sky Residual')
                elif index==8 or n_sp<2:
                    plt.xlabel('Wavelength')
            index+=1
        pdf.savefig()  # saves the current figure into a pdf page
        plt.close()

import pdb;pdb.set_trace()
