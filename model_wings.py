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
from desispec import io
"""
img = io.read_raw(args.infile, camera,
                              fibermapfile=args.fibermap,
                              bias=bias, dark=dark, pixflat=pixflat, mask=mask, bkgsub=args.bkgsub,
                              nocosmic=args.nocosmic,
                              cosmics_nsig=args.cosmics_nsig,
                              cosmics_cfudge=args.cosmics_cfudge,
                              cosmics_c2fudge=args.cosmics_c2fudge,
                              ccd_calibration_filename=ccd_calibration_filename,
                              nocrosstalk=args.nocrosstalk,
                              nogain=args.nogain,
                              use_savgol=args.use_savgol,
                              nodarktrail=args.nodarktrail,
                              fill_header=args.fill_header,
                              remove_scattered_light=args.scattered_light
            )

io.write_image(outfile, img)
    #- Actually write or update the file
    if os.path.exists(filename):
        hdus = fits.open(filename, mode='append', memmap=False)
        if extname in hdus:
            hdus.close()
            raise ValueError('Camera {} already in {}'.format(camera, filename))
        else:
            hdus.append(dataHDU)
            hdus.flush()
            hdus.close()
    else:
        hdus = fits.HDUList()
        add_dependencies(primary_header)
        hdus.append(fits.PrimaryHDU(None, header=primary_header))
        hdus.append(dataHDU)
        hdus.writeto(filename)

salloc -N 10 -t 0:30:00 -C haswell -q realtime
time srun -N 10 -c 2 desi_proc --mpi --traceshift -n 20200315 -e 55589


"""


preproc_dir1='/global/project/projectdirs/desi/users/zhangkai/redux_one_exp/'
preproc_dir_dark='/global/project/projectdirs/desi/users/zhangkai/redux_one_exp/'
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

#expid='00055556' # twilight
#add='twilight'
#zmax=20
#expid='00055713' # flat
#add='flat'
#zmax=20
#expid='00055555' # zero
#add='zero'
#zmax=5
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
night_dark='20191110'
expid_dark='00026341' # dark
sp_arr=['0', '1','2','3','4','5','6','7','8','9']
sm_arr=['4','10','5','6','1','9','7','8','2','3']
cam_arr=['b']#,'r','z']
plot=False
overwrite=True
output_dir='/project/projectdirs/desi/spectro/redux/extendwavelength/preproc/'+night+'/'+expid+'/'

for cam in cam_arr:
    for i in range(len(sp_arr)):
        sp=sp_arr[i]
        camera=cam+sp
        print(camera)

        file_preproc1=preproc_dir1+'/'+night+'/'+expid+'/preproc-'+camera+'-'+expid+'.fits'
        file_dark=preproc_dir_dark+'/'+night_dark+'/'+expid_dark+'/preproc-'+camera+'-'+expid_dark+'.fits'
        file_output=output_dir+'/preproc-'+camera+'-'+expid+'.fits'
        #import pdb;pdb.set_trace()
        try:
            hdul1=fits.open(file_preproc1,mode='append', memmap=False)
            hdul_dark=fits.open(file_dark)
        except:
            continue
        hdul1[0].data=hdul1[0].data-hdul_dark[0].data
        hdul1.writeto(file_output,overwrite=overwrite)

        if plot:
            print('Plot')
            plt.subplot(3,2,1)
            plt.imshow(hdul1[0].data-hdul_dark[0].data,vmin=0,vmax=5)
            plt.title(expid+' '+camera)
            plt.colorbar()
            plt.subplot(3,2,2)
            y=np.median(hdul1[0].data[:,1400:2400],axis=1)
            y_smooth=savgol_filter(y, 11, 2)
            plt.plot(y)
            plt.axis([0,300,-2,20])
            plt.plot([0,10000],[0,0],'b--')
            plt.ylabel('Flux')
            plt.xlabel('CCD column')

            plt.subplot(3,2,3)
            plt.imshow(hdul_dark[0].data,vmin=0,vmax=5)
            plt.title(expid_dark+' '+camera)
            plt.colorbar()
            plt.subplot(3,2,4)
            y=hdul_dark[0].data
            y=np.median(y[:,1400:2400],axis=1)
            y_smooth=savgol_filter(y, 11, 2)
            plt.plot(y)
            plt.axis([0,300,-2,20])
            plt.plot([0,10000],[0,0],'b--')
            plt.ylabel('900s dark flux')
            plt.xlabel('CCD column')


            plt.subplot(3,2,5)
            y=hdul1[0].data-hdul_dark[0].data
            plt.imshow(y,vmin=0,vmax=5)
            plt.title(expid+'-'+expid_dark+' '+camera)
            plt.colorbar()
            plt.subplot(3,2,6)
            y=np.median(y[:,1400:2400],axis=1)
            y_smooth=savgol_filter(y, 11, 2)
            plt.plot(y)
            plt.axis([0,300,-2,20])
            plt.plot([0,10000],[0,0],'b--')
            plt.ylabel('Residual')
            plt.xlabel('CCD column')

            plt.tight_layout()
            plt.show()


