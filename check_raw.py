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
import desispec.preproc
from desispec.calibfinder import parse_date_obs, CalibFinder
#img = desispec.preproc.preproc(rawimage, header, primary_header, **kwargs)


#from desispec.scripts import preproc
#preproc.main(preproc.parse())


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

def subtract_overscan(fx,camera):
    import desispec.preproc
    from desispec.calibfinder import parse_date_obs, CalibFinder
    rawimage = fx[camera.upper()].data
    rawimage = rawimage.astype(np.float64)
    header = fx[camera.upper()].header
    hdu=0
    primary_header= fx[hdu].header
    ccd_calibration_filename=None
    log=desispec.preproc.get_logger()

    cfinder = CalibFinder([header, primary_header], yaml_file=ccd_calibration_filename)
    amp_ids = desispec.preproc.get_amp_ids(header)
    #######################
    use_overscan_row = False
    overscan_per_row=False
    #######################
    # Subtract overscan 
    for amp in amp_ids:
        # Grab the sections
        ov_col = desispec.preproc.parse_sec_keyword(header['BIASSEC'+amp])
        if 'ORSEC'+amp in header.keys():
            ov_row = desispec.preproc.parse_sec_keyword(header['ORSEC'+amp])
        elif use_overscan_row:
            log.error('No ORSEC{} keyword; not using overscan_row'.format(amp))
            use_overscan_row = False

        # Generate the overscan images
        raw_overscan_col = rawimage[ov_col].copy()

        if use_overscan_row:
            raw_overscan_row = rawimage[ov_row].copy()
            overscan_row = np.zeros_like(raw_overscan_row)

            # Remove overscan_col from overscan_row
            raw_overscan_squared = rawimage[ov_row[0], ov_col[1]].copy()
            for row in range(raw_overscan_row.shape[0]):
                o,r = _overscan(raw_overscan_squared[row])
                overscan_row[row] = raw_overscan_row[row] - o

        # Now remove the overscan_col
        nrows=raw_overscan_col.shape[0]
        log.info("nrows in overscan=%d"%nrows)
        overscan_col = np.zeros(nrows)
        rdnoise  = np.zeros(nrows)
        if (cfinder and cfinder.haskey('OVERSCAN'+amp) and cfinder.value("OVERSCAN"+amp).upper()=="PER_ROW") or overscan_per_row:
            log.info("Subtracting overscan per row for amplifier %s of camera %s"%(amp,camera))
            for j in range(nrows) :
                if np.isnan(np.sum(overscan_col[j])) :
                    log.warning("NaN values in row %d of overscan of amplifier %s of camera %s"%(j,amp,camera))
                    continue
                o,r =  _overscan(raw_overscan_col[j])
                #log.info("%d %f %f"%(j,o,r))
                overscan_col[j]=o
                rdnoise[j]=r
        else :
            log.info("Subtracting average overscan for amplifier %s of camera %s"%(amp,camera))
            o,r =  desispec.preproc._overscan(raw_overscan_col)
            overscan_col += o
            rdnoise  += r

        #- subtract overscan from data region and apply gain
        jj = desispec.preproc.parse_sec_keyword(header['DATASEC'+amp])
        kk = desispec.preproc.parse_sec_keyword(header['CCDSEC'+amp])

        data = rawimage[jj].copy()
        # Subtract columns
        for k in range(nrows):
            data[k] -= overscan_col[k]
        # And now the rows
        if use_overscan_row:
            # Savgol?
            if use_savgol:
                log.info("Using savgol")
                collapse_oscan_row = np.zeros(overscan_row.shape[1])
                for col in range(overscan_row.shape[1]):
                    o, _ = _overscan(overscan_row[:,col])
                    collapse_oscan_row[col] = o
                oscan_row = _savgol_clipped(collapse_oscan_row, niter=0)
                oimg_row = np.outer(np.ones(data.shape[0]), oscan_row)
                data -= oimg_row
            else:
                o,r = _overscan(overscan_row)
                data -= o
        rawimage[jj]=data
    return rawimage


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
night='20191110'
expid='00026341' # dark
add='dark'
zmax=50

sp_arr=['0', '1','2','3','4','5','6','7','8','9']
sm_arr=['4','10','5','6','1','9','7','8','2','3']
cam_arr=['b','r','z']

#camera='b0'
file_raw1=raw_dir1+'/'+night+'/'+expid+'/desi-'+expid+'.fits.fz'
hdul1=fits.open(file_raw1,memmap=False)
#fx = fits.open(filename, memmap=False)

with PdfPages('check_raw_'+night+'_'+add+'.pdf') as pdf:
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
                rawimage = subtract_overscan(hdul1,camera)
            except:
                continue
            nx=len(hdul_this.data)
            x=np.arange(nx)
            y_hat1 = np.median(rawimage[:,1400:2400],axis=1)
            y_hat3=np.median(rawimage[1400:2400,:],axis=0)

            # Filter the data, and plot both the original and filtered signals.
            #y_filter = butter_lowpass_filter(y_hat1, cutoff, fs, order)
            y_filter= savgol_filter(y_hat1, 101, 2)

            plt.subplot(3,1,1)
            plt.plot(x,y_hat1,label='Raw')

            #plt.plot(x,y_filter,color='red',label='Fitered')
            #plt.axis([-20,4200,np.median(y_hat1)-20,max(y_hat1)+10]) # original one
            plt.axis([-20,4200,-5,20])
            plt.yscale('linear')
            #plt.yscale('log')
            plt.xlabel('CCD row')
            plt.ylabel('electron/pix')
            plt.title(expid+' '+camera)
            plt.legend(loc=0)

            plt.subplot(3,1,2)
            plt.plot(y_hat3,label='With scattered light')
            #plt.axis([-20,4300,np.median(y_hat3)-20,max(y_hat3)+10])
            plt.axis([-20,4200,-5,20])
            plt.yscale('linear')
            #plt.yscale('log')
            plt.xlabel('CCD column')
            plt.ylabel('electron/pix')
            plt.title(expid+' '+camera)
            plt.legend(loc=0)

            plt.subplot(3,1,3)
            plt.imshow(rawimage,vmin=-5,vmax=20)#vmin=np.median(y_hat1)-20,vmax=max(y_hat1)+10)
            plt.title(expid+' '+camera)
            plt.colorbar()
            pdf.savefig()
            plt.close()


