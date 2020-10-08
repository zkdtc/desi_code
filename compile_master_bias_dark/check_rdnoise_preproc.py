from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from os import listdir
import pdb

def calculate_one_exposure(night,expid,sp_arr,sm_arr,cam_arr,preproc_dir=None,visual_check=False,full_region=False):

    n_sp=len(sp_arr)

    df_output = pd.DataFrame({'night':[], 'expid':[],'mjd':[],'flavor':[],'obstype':[],'camera':[],'rdnoise_preproc_a':[],'rdnoise_header_a':[],'rdnoise_preproc_b':[],'rdnoise_header_b':[],'rdnoise_preproc_c':[],'rdnoise_header_c':[],'rdnoise_preproc_d':[],'rdnoise_header_d':[],'median_flux_all':[],'median_flux_a':[],'median_flux_b':[],'median_flux_c':[],'median_flux_d':[]})

    for cam in cam_arr:
        rdnoise_region_a_arr=[]
        rdnoise_header_a_arr=[]
        rdnoise_region_b_arr=[]
        rdnoise_header_b_arr=[]
        rdnoise_region_c_arr=[]
        rdnoise_header_c_arr=[]
        rdnoise_region_d_arr=[]
        rdnoise_header_d_arr=[]
        for i in range(n_sp):
            camera=cam.lower()+sp_arr[i]
            filename=preproc_dir+'/'+night+'/'+expid+'/preproc-'+cam+sp_arr[i]+'-'+expid+'.fits'
            print('Processing ',camera,expid)
            filename_raw='/global/cfs/cdirs/desi/spectro/data/'+night+'/'+expid+'/desi-'+expid+'.fits.fz'
            try:
                hdul=fits.open(filename)
                img_preproc=hdul['IMAGE'].data
                img_rdnoise=hdul['READNOISE'].data
                mjd=hdul[0].header['MJD-OBS']
                flavor=hdul[0].header['FLAVOR']
                header_raw=fits.getheader(filename_raw,1)
                obstype=header_raw['OBSTYPE']
                nx=len(img_preproc[0])
                ny=len(img_preproc)
                ###  Select regions [y1:y2,x1:x2] ####
                if full_region:
                    width=100
                    x_off=0
                    y1=0
                    y2=int(ny/2)-1
                    x1=0
                    x2=width-1
                else:
                    width=60
                    x_off=10
                    y1=250 #0
                    y2=y1+500 #int(ny/2)-1
                    x1=0+x_off
                    x2=width-1+x_off
                region_a=img_preproc.copy()[y1:y2,x1:x2]
                rdnoise_a=np.median(img_rdnoise[y1:y2,x1:x2])
                # B
                if full_region:
                    y1=0 
                    y2=int(ny/2)-1
                    x1=nx-width
                    x2=nx-1
                else:
                    y1=250 #
                    y2=y1+500 #int(ny/2)-1
                    x1=nx-width-x_off
                    x2=nx-1-x_off
                region_b=img_preproc.copy()[y1:y2,x1:x2]
                rdnoise_b=np.median(img_rdnoise[y1:y2,x1:x2])
                # C
                if full_region:
                    y1=int(ny/2)-1
                    y2=ny-1
                    x1=nx-width
                    x2=nx-1
                else:
                    y1=int(ny/2)-1+1250
                    y2=y1+500#ny-1
                    x1=nx-width-x_off
                    x2=nx-1-x_off
                region_c=img_preproc.copy()[y1:y2,x1:x2]
                rdnoise_c=np.median(img_rdnoise[y1:y2,x1:x2])
                # D 
                if full_region:
                    y1=int(ny/2)-1
                    y2=ny-1
                    x1=0
                    x2=width-1
                else:
                    y1=int(ny/2)-1+1250
                    y2=y1+500#ny-1
                    x1=0+x_off
                    x2=width-1+x_off 
                region_d=img_preproc.copy()[y1:y2,x1:x2]
                rdnoise_d=np.median(img_rdnoise[y1:y2,x1:x2])

                std_a=(np.percentile(region_a,84)-np.percentile(region_a,16))/2.
                std_b=(np.percentile(region_b,84)-np.percentile(region_b,16))/2.
                std_c=(np.percentile(region_c,84)-np.percentile(region_c,16))/2.
                std_d=(np.percentile(region_d,84)-np.percentile(region_d,16))/2.
                median_flux_all=np.median(img_preproc)
                print(median_flux_all)
                median_flux_a=np.median(region_a)
                median_flux_b=np.median(region_b)
                median_flux_c=np.median(region_c)
                median_flux_d=np.median(region_d)

                if (visual_check):# and flavor.lower=='twilight'):
                    plt.imshow(img_preproc,vmin=0,vmax=10)
                    plt.colorbar()
                    plt.show()
                    thres=0
                    nbin=25
                    vmin=-5
                    vmax=15
                    xrange=(-15,20)
                    if abs(rdnoise_a-std_a)>=thres or abs(rdnoise_b-std_b)>=thres or abs(rdnoise_c-std_c)>=thres or abs(rdnoise_d-std_d)>=thres:
                        plt.figure(figsize=(19,10))
                        plt.subplot(2,4,1)
                        plt.title(camera+' A header:'+str(rdnoise_a)[0:3]+' preproc:'+str(std_a)[0:3])
                        plt.hist(np.array(region_a[0:500,:]).ravel(),nbin,range=xrange,alpha=0.5,color='red',label='[0:500]')
                        plt.hist(np.array(region_a[500:1000,:]).ravel(),nbin,range=xrange,alpha=0.5,color='orange',label='[501:1000]')
                        plt.hist(np.array(region_a[1001:1500,:]).ravel(),nbin,range=xrange,alpha=0.5,color='yellow',label='[1001:1500]')
                        plt.hist(np.array(region_a[1501:,:]).ravel(),nbin,range=xrange,alpha=0.5,color='green',label='[1501:]')
                        plt.legend(loc=0)
                        plt.subplot(2,4,2)
                        plt.title(camera+' B header:'+str(rdnoise_b)[0:3]+' preproc:'+str(std_b)[0:3])
                        plt.hist(np.array(region_b[0:500,:]).ravel(),nbin,range=xrange,alpha=0.5,color='red')
                        plt.hist(np.array(region_b[500:1000,:]).ravel(),nbin,range=xrange,alpha=0.5,color='orange')
                        plt.hist(np.array(region_b[1001:1500,:]).ravel(),nbin,range=xrange,alpha=0.5,color='yellow')
                        plt.hist(np.array(region_b[1501:,:]).ravel(),nbin,range=xrange,alpha=0.5,color='green')
                        plt.subplot(2,4,3)
                        plt.title(camera+' C header:'+str(rdnoise_c)[0:3]+' preproc:'+str(std_c)[0:3])
                        plt.hist(np.array(region_c[0:500,:]).ravel(),nbin,range=xrange,alpha=0.5,color='red')
                        plt.hist(np.array(region_c[500:1000,:]).ravel(),nbin,range=xrange,alpha=0.5,color='orange')
                        plt.hist(np.array(region_c[1001:1500,:]).ravel(),nbin,range=xrange,alpha=0.5,color='yellow')
                        plt.hist(np.array(region_c[1501:,:]).ravel(),nbin,range=xrange,alpha=0.5,color='green')
                        plt.subplot(2,4,4)
                        plt.title(camera+' D header:'+str(rdnoise_d)[0:3]+' preproc:'+str(std_d)[0:3])
                        plt.hist(np.array(region_d[0:500,:]).ravel(),nbin,range=xrange,alpha=0.5,color='red')
                        plt.hist(np.array(region_d[500:1000,:]).ravel(),nbin,range=xrange,alpha=0.5,color='orange')
                        plt.hist(np.array(region_d[1001:1500,:]).ravel(),nbin,range=xrange,alpha=0.5,color='yellow')
                        plt.hist(np.array(region_d[1501:,:]).ravel(),nbin,range=xrange,alpha=0.5,color='green')

                        plt.subplot(2,4,5)
                        plt.imshow(region_a,vmin=vmin,vmax=vmax)
                        plt.title('A')
                        plt.subplot(2,4,6)
                        plt.imshow(region_b,vmin=vmin,vmax=vmax)
                        plt.title('B')
                        plt.subplot(2,4,7)
                        plt.title('C')
                        plt.imshow(region_c,vmin=vmin,vmax=vmax)
                        plt.subplot(2,4,8)
                        plt.title('D')
                        plt.imshow(region_d,vmin=vmin,vmax=vmax)
                        plt.show()

                d_this={'night':night, 'expid':expid,'mjd':mjd,'flavor':flavor,'obstype':obstype,'camera':camera,'rdnoise_preproc_a':std_a,'rdnoise_header_a':rdnoise_a,'rdnoise_preproc_b':std_b,'rdnoise_header_b':rdnoise_b,'rdnoise_preproc_c':std_c,'rdnoise_header_c':rdnoise_c,'rdnoise_preproc_d':std_d,'rdnoise_header_d':rdnoise_d,'median_flux_all':median_flux_all,'median_flux_a':median_flux_a,'median_flux_b':median_flux_b,'median_flux_c':median_flux_c,'median_flux_d':median_flux_d}
                df_output=df_output.append(d_this,ignore_index=True)
                #import pdb;pdb.set_trace()
            except:
                print('Fail to process '+camera)

    return df_output


def calculate_one_night(night,preproc_dir=None,max=None):
    #print('{} Checking for new files on {}'.format(time.asctime(), night))
    expids=listdir(preproc_dir+'/'+str(night)+'/')
    expids.sort(reverse=True)
    sp_arr=['0', '1','2','3','4','5','6','7','8','9']
    sm_arr=['4','10','5','6','1','9','7','8','2','3']
    cam_arr=['b','r','z']

    df_output = pd.DataFrame({'night':[], 'expid':[],'mjd':[],'flavor':[],'obstype':[],'camera':[],'rdnoise_preproc_a':[],'rdnoise_header_a':[],'rdnoise_preproc_b':[],'rdnoise_header_b':[],'rdnoise_preproc_c':[],'rdnoise_header_c':[],'rdnoise_preproc_d':[],'rdnoise_header_d':[],'median_flux_all':[],'median_flux_a':[],'median_flux_b':[],'median_flux_c':[],'median_flux_d':[]})
    if not max:
        max=len(expids)
    elif max>len(expids):
            max=len(expids)
    for i in range(max):
        expid=expids[i]
        print(night,' ',expid)
        # Check the redux folder for reduced files
        df_expid=calculate_one_exposure(str(night),expid,sp_arr,sm_arr,cam_arr,preproc_dir=preproc_dir)
        df_output=df_output.append(df_expid)
    return df_output

######################################
####### Main code ####################
######################################
### Find all nights ###
#######################
preproc_dir="/global/project/projectdirs/desi/users/zhangkai/redux_newbias/" #os.getenv('DESI_SPECTRO_REDUX')+'/daily/preproc/'
nights=listdir(preproc_dir)
nights=[int(x) for x in nights]
nights.sort(reverse=True)
read=True #False
add='all'
night_min=20200304
data_file='check_rdnoise_preproc_'+add+'.csv'

if read:
    df_all_nights = pd.read_csv(data_file)
else:
    
    df_all_nights = pd.DataFrame({'night':[], 'expid':[],'mjd':[],'flavor':[],'obstype':[],'camera':[],'rdnoise_preproc_a':[],'rdnoise_header_a':[],'rdnoise_preproc_b':[],'rdnoise_header_b':[],'rdnoise_preproc_c':[],'rdnoise_header_c':[],'rdnoise_preproc_d':[],'rdnoise_header_d':[],'median_flux_all':[],'median_flux_a':[],'median_flux_b':[],'median_flux_c':[],'median_flux_d':[]})

    n_night=len(nights)
    for j in range(n_night):
        night=nights[j]
        df_night=calculate_one_night(night,preproc_dir=preproc_dir)
        df_all_nights=df_all_nights.append(df_night)
    cmd='rm '+data_file
    a=os.system(cmd)
    df_all_nights.to_csv(data_file,index=False)


sp_arr=['0', '1','2','3','4','5','6','7','8','9']
sm_arr=['4','10','5','6','1','9','7','8','2','3']
cam_arr=['b','r','z']
obstype_arr=['zero','dark']
#obstype_arr=['twilight','flat','arc','science']

from matplotlib.backends.backend_pdf import PdfPages

with PdfPages('check_rdnoise_preproc_1_'+add+'.pdf') as pdf:
    for obstype in obstype_arr:
        print(obstype)
        if True:
            for cam in cam_arr:
                plt.figure(figsize=(20,15))
                font = {'family' : 'normal',
                'size'   : 22}
                plt.rc('font', **font)
                for i in range(len(sp_arr)):
                    sp=sp_arr[i]
                    camera=cam+sp
                    print(camera)
                    #import pdb;pdb.set_trace()
                    try:
                        ind=np.where((df_all_nights['night']>=night_min) & (df_all_nights['camera'].str.lower()==camera) & (df_all_nights['obstype'].str.lower()==obstype))
                    except:
                        continue
                    print(ind)
                    plt.subplot(3,4,i+1)
                    try:
                        x=df_all_nights.iloc[ind]['mjd']-int(min(df_all_nights.iloc[ind]['mjd']))
                    except:
                        continue
                    plt.plot(x,df_all_nights.iloc[ind]['rdnoise_preproc_a'],'+',color='red',label='Amp A preproc')
                    plt.plot(x,df_all_nights.iloc[ind]['rdnoise_preproc_b'],'+',color='yellow',label='Amp B preproc')
                    plt.plot(x,df_all_nights.iloc[ind]['rdnoise_preproc_c'],'+',color='blue',label='Amp C preproc')
                    plt.plot(x,df_all_nights.iloc[ind]['rdnoise_preproc_d'],'+',color='green',label='Amp D preproc')
                    #plt.plot(x,df_all_nights.iloc[ind]['rdnoise_preproc_a'].tolist(),color='red')
                    #plt.plot(x,df_all_nights.iloc[ind]['rdnoise_preproc_b'].tolist(),color='yellow')
                    #plt.plot(x,df_all_nights.iloc[ind]['rdnoise_preproc_c'].tolist(),color='blue')
                    #plt.plot(x,df_all_nights.iloc[ind]['rdnoise_preproc_d'].tolist(),color='green')
                    plt.plot(x,df_all_nights.iloc[ind]['rdnoise_header_a'],'o',color='red',label='Amp A header')
                    plt.plot(x,df_all_nights.iloc[ind]['rdnoise_header_b'],'o',color='yellow',label='Amp B header')
                    plt.plot(x,df_all_nights.iloc[ind]['rdnoise_header_c'],'o',color='blue',label='Amp C header')
                    plt.plot(x,df_all_nights.iloc[ind]['rdnoise_header_d'],'o',color='green',label='Amp D header')
                    #plt.plot(x,df_all_nights.iloc[ind]['rdnoise_header_a'].tolist(),color='red')
                    #plt.plot(x,df_all_nights.iloc[ind]['rdnoise_header_b'].tolist(),color='yellow')
                    #plt.plot(x,df_all_nights.iloc[ind]['rdnoise_header_c'].tolist(),color='blue')
                    #plt.plot(x,df_all_nights.iloc[ind]['rdnoise_header_d'].tolist(),color='green')
                    plt.axis([0,max(x)+10,2,6])
                    plt.title(camera+' '+obstype)
                    if sp=='0':
                        plt.legend(loc=0)
                    if sp=='4':
                        plt.ylabel('RDNOISE')
                    if sp=='9':
                        plt.xlabel('MJD-'+str(int(min(df_all_nights.iloc[ind]['mjd']))))
                pdf.savefig()
                plt.close()
        else:
            pass

with PdfPages('check_rdnoise_preproc_2_'+add+'.pdf') as pdf:
    for obstype in obstype_arr:
        print(obstype)
        if True:
            for cam in cam_arr:
                plt.figure(figsize=(20,15))
                font = {'family' : 'normal',
                'size'   : 22}
                plt.rc('font', **font)
        
                for i in range(len(sp_arr)):
                    sp=sp_arr[i]
                    camera=cam+sp
                    ind=np.where((df_all_nights['night']>=night_min) & (df_all_nights['camera'].str.lower()==camera) & (df_all_nights['obstype'].str.lower()==obstype))
                    plt.subplot(3,4,i+1)
                    try:
                        x=df_all_nights.iloc[ind]['mjd']-int(min(df_all_nights.iloc[ind]['mjd']))
                    except:
                        continue
                    y=df_all_nights.iloc[ind]['rdnoise_preproc_a']-df_all_nights.iloc[ind]['rdnoise_header_a']
                    plt.plot(x,y,'+',color='red',label='Amp A')
                    #plt.plot(x,y,color='red')

                    y=df_all_nights.iloc[ind]['rdnoise_preproc_b']-df_all_nights.iloc[ind]['rdnoise_header_b']
                    plt.plot(x,y,'+',color='yellow',label='Amp B')
                    #plt.plot(x,y,color='yellow')
            
                    y=df_all_nights.iloc[ind]['rdnoise_preproc_c']-df_all_nights.iloc[ind]['rdnoise_header_c']
                    plt.plot(x,y,'+',color='green',label='Amp C')
                    #plt.plot(x,y,color='green')
            
                    y=df_all_nights.iloc[ind]['rdnoise_preproc_d']-df_all_nights.iloc[ind]['rdnoise_header_d']
                    plt.plot(x,y,'+',color='blue',label='Amp D')
                    #plt.plot(x,y,color='blue')
                    plt.axis([0,max(x)+10,-1,2])
                    plt.plot([0,10000],[0,0],'--',color='black')
                    plt.title(camera+' '+obstype)
                    if sp=='0':
                        plt.legend(loc=0)
                    if sp=='4':
                        plt.ylabel('RDNOISE(preproc-header')
                    if sp=='9':
                        plt.xlabel('MJD-'+str(int(min(df_all_nights.iloc[ind]['mjd']))))
                pdf.savefig()
                plt.close()


with PdfPages('check_rdnoise_preproc_3_'+add+'.pdf') as pdf:
    for obstype in obstype_arr:
        print(obstype)
        if True:

            for cam in cam_arr:
                plt.figure(figsize=(20,15))
                font = {'family' : 'normal',
                'size'   : 12}
                plt.rc('font', **font)

                for i in range(len(sp_arr)):
                    sp=sp_arr[i]
                    camera=cam+sp

                    ind=np.where((df_all_nights['night']>=night_min) & (df_all_nights['camera'].str.lower()==camera) & (df_all_nights['obstype'].str.lower()==obstype))
                    x=df_all_nights.iloc[ind]['rdnoise_header_a']
                    y=df_all_nights.iloc[ind]['rdnoise_preproc_a']
                    plt.subplot(3,4,i+1)
                    plt.plot(x,y,'+',label='Amp A')
                    x=df_all_nights.iloc[ind]['rdnoise_header_b']
                    y=df_all_nights.iloc[ind]['rdnoise_preproc_b']
                    plt.plot(x,y,'o',label='Amp B')
                    x=df_all_nights.iloc[ind]['rdnoise_header_c']
                    y=df_all_nights.iloc[ind]['rdnoise_preproc_c']
                    plt.plot(x,y,'v',label='Amp C')
                    x=df_all_nights.iloc[ind]['rdnoise_header_d']
                    y=df_all_nights.iloc[ind]['rdnoise_preproc_d']
                    plt.plot(x,y,'1',label='Amp D')
                    plt.axis([1,6,1,6])
                    plt.title(camera+' '+obstype)
                    plt.xlabel('RDNOISE in header')
                    plt.ylabel('RDNOISE measured')
                    plt.plot([0,100],[0,100],color='black')
                    plt.legend(loc=0)
                pdf.savefig()
                plt.close()

with PdfPages('check_rdnoise_preproc_4_'+add+'.pdf') as pdf:
    for cam in cam_arr:
        plt.figure(figsize=(20,15))
        font = {'family' : 'normal',
        'size'   : 12}
        plt.rc('font', **font)

        for i in range(len(sp_arr)):
            sp=sp_arr[i]
            camera=cam+sp

            ind=np.where((df_all_nights['night']>=night_min) & (df_all_nights['camera']==camera))
            x=df_all_nights.iloc[ind]['median_flux_all']
            y=df_all_nights.iloc[ind]['median_flux_a']
            plt.subplot(3,4,i+1)
            plt.plot(x,y,'+',label='Amp A')
            x=df_all_nights.iloc[ind]['median_flux_all']
            y=df_all_nights.iloc[ind]['median_flux_b']
            plt.plot(x,y,'o',label='Amp B')
            x=df_all_nights.iloc[ind]['median_flux_all']
            y=df_all_nights.iloc[ind]['median_flux_c']
            plt.plot(x,y,'v',label='Amp C')
            x=df_all_nights.iloc[ind]['median_flux_all']
            y=df_all_nights.iloc[ind]['median_flux_d']
            plt.plot(x,y,'1',label='Amp D')
            if (add=="zero"):
                plt.axis([0,5,0,5])
                plt.plot([0,5],[0,5],color='black')
            else:
                plt.axis([0,1100,0,20])
                plt.plot([0,1100],[0,20],color='black')

            plt.title(camera)
            plt.xlabel('Median Flux All Image')
            plt.ylabel('Median Flux regions')
            plt.legend(loc=0)
        pdf.savefig()
        plt.close()

with PdfPages('check_rdnoise_preproc_5_'+add+'.pdf') as pdf:
    for cam in cam_arr:
        plt.figure(figsize=(20,15))
        font = {'family' : 'normal',
        'size'   : 12}
        plt.rc('font', **font)

        for i in range(len(sp_arr)):
            sp=sp_arr[i]
            camera=cam+sp

            ind=np.where((df_all_nights['night']>=night_min) & (df_all_nights['camera']==camera))
            x=df_all_nights.iloc[ind]['median_flux_all']
            y=df_all_nights.iloc[ind]['rdnoise_preproc_a']-df_all_nights.iloc[ind]['rdnoise_header_a']
            plt.subplot(3,4,i+1)
            plt.plot(x,y,'+',label='Amp A')
            x=df_all_nights.iloc[ind]['median_flux_all']
            y=df_all_nights.iloc[ind]['rdnoise_preproc_a']-df_all_nights.iloc[ind]['rdnoise_header_a']
            plt.plot(x,y,'o',label='Amp B')
            x=df_all_nights.iloc[ind]['median_flux_all']
            y=df_all_nights.iloc[ind]['rdnoise_preproc_a']-df_all_nights.iloc[ind]['rdnoise_header_a']
            plt.plot(x,y,'v',label='Amp C')
            x=df_all_nights.iloc[ind]['median_flux_all']
            y=df_all_nights.iloc[ind]['rdnoise_preproc_a']-df_all_nights.iloc[ind]['rdnoise_header_a']
            plt.plot(x,y,'1',label='Amp D')
            plt.axis([0,1100,0,2])
            plt.title(camera)
            plt.xlabel('Median Flux All Image')
            plt.ylabel('RDNOISE Difference (preproc-overscan)')
            plt.plot([0,1100],[0,2],color='black')
            plt.legend(loc=0)
        pdf.savefig()
        plt.close()

