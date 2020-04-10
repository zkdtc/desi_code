from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
night='20200315'
expid='00055692'

sp_arr=['0', '1','2','3','4','5','6','7','8','9']
sm_arr=['4','10','5','6','1','9','7','8','2','3']
n_sp=len(sp_arr)
cam_arr=['b','r','z']

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
        camera=cam.upper()+sp_arr[i]
        filename='/project/projectdirs/desi/spectro/redux/daily/preproc/'+night+'/'+expid+'/preproc-'+cam+sp_arr[i]+'-'+expid+'.fits'
        hdul = fits.open(filename)
        img_preproc=hdul['IMAGE'].data
        img_rdnoise=hdul['READNOISE'].data
        nx=len(img_preproc[0])
        ny=len(img_preproc)
        width=50
        region_a=img_preproc.copy()[0:width-1,0:int(ny/2)-1]
        rdnoise_a=np.median(img_rdnoise[0:width-1,0:int(ny/2)-1])
        region_b=img_preproc.copy()[nx-width:nx-1,0:int(ny/2)-1]
        rdnoise_b=np.median(img_rdnoise[nx-width:nx-1,0:int(ny/2)-1])
        region_c=img_preproc.copy()[nx-width:nx-1,int(ny/2)-1:ny-1]
        rdnoise_c=np.median(img_rdnoise[nx-width:nx-1,int(ny/2)-1:ny-1])
        region_d=img_preproc.copy()[0:width-1,int(ny/2)-1:ny-1]
        rdnoise_d=np.median(img_rdnoise[0:width-1,int(ny/2)-1:ny-1])

        std_a=(np.percentile(region_a,84)-np.percentile(region_a,16))/2.
        std_b=(np.percentile(region_b,84)-np.percentile(region_b,16))/2.
        std_c=(np.percentile(region_c,84)-np.percentile(region_c,16))/2.
        std_d=(np.percentile(region_d,84)-np.percentile(region_d,16))/2.
         
        rdnoise_region_a_arr.append(std_a)
        rdnoise_header_a_arr.append(rdnoise_a)
        rdnoise_region_b_arr.append(std_b)
        rdnoise_header_b_arr.append(rdnoise_b)
        rdnoise_region_c_arr.append(std_c)
        rdnoise_header_c_arr.append(rdnoise_c)
        rdnoise_region_d_arr.append(std_d)
        rdnoise_header_d_arr.append(rdnoise_d)
    if cam=='b':
        num=1
    elif cam=='r':
        num=2
    else:
        num=3
    plt.subplot(2,2,num)
    plt.plot(rdnoise_header_a_arr,rdnoise_region_a_arr,'+',label='Amp A')
    plt.plot(rdnoise_header_b_arr,rdnoise_region_b_arr,'o',label='Amp B')
    plt.plot(rdnoise_header_c_arr,rdnoise_region_c_arr,'v',label='Amp C')
    plt.plot(rdnoise_header_d_arr,rdnoise_region_d_arr,'1',label='Amp D')
    plt.axis([1,6,1,6])
    plt.title(cam)
    plt.xlabel('RDNOISE in header')
    plt.ylabel('RDNOISE measured')
    plt.plot([0,100],[0,100],color='black')
    plt.legend(loc=0)
plt.show()

import pdb;pdb.set_trace()


