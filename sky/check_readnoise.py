import re
import os
import numpy as np
import scipy.interpolate
from pkg_resources import resource_exists, resource_filename

from scipy import signal

from desispec.image import Image
from desispec import cosmics
from desispec.maskbits import ccdmask
from desiutil.log import get_logger
from desispec.calibfinder import CalibFinder
from desispec.darktrail import correct_dark_trail
#from desispec.scatteredlight import model_scattered_light
from desispec.io.xytraceset import read_xytraceset
from desispec.maskedmedian import masked_median
from desispec import preproc
from astropy.io import fits
import matplotlib.pyplot as plt


night='20200315'
expid='00055692'
filename=os.getenv('DESI_SPECTRO_DATA')+'/'+str(night)+'/'+str(expid).zfill(8)+'/desi-'+str(expid).zfill(8)+'.fits.fz'
primary_header=fits.getheader(filename,1)
#flavor=h1['flavor'].strip()
hdul = fits.open(filename)

_overscan=preproc._overscan
log=preproc.get_logger()
sp_arr=['0', '1','2','3','4','5','6','7','8','9']
sm_arr=['4','10','5','6','1','9','7','8','2','3']
parse_sec_keyword=preproc.parse_sec_keyword
n_sp=len(sp_arr)
cam_arr=['b','r','z']
rdnoise_median1_arr=[]
rdnoise_median2_arr=[]
rdnoise_median3_arr=[]
rdnoise_median4_arr=[]

def cal_rdnoise(hdul,camera,ccd_calibration_filename,use_overscan_row,overscan_per_row,use_active):
    if True:
        hdul_this=hdul[camera]
        header=hdul_this.header
        rawimage=hdul_this.data
        # works!  preproc.preproc(hdul['B0'].data,hdul['B0'].header,h1)
        amp_ids=preproc.get_amp_ids(header)

        #- Output arrays
        ny=0
        nx=0
        for amp in amp_ids :
            yy, xx = parse_sec_keyword(header['CCDSEC%s'%amp])
            ny=max(ny,yy.stop)
            nx=max(nx,xx.stop)
        image = np.zeros((ny,nx))

        readnoise = np.zeros_like(image)
        nogain=False

        cfinder = None

        if ccd_calibration_filename is not False:
            cfinder = CalibFinder([header, primary_header], yaml_file=ccd_calibration_filename)

        for amp in amp_ids:
            # Grab the sections
            ov_col = parse_sec_keyword(header['BIASSEC'+amp])
            ov_row = parse_sec_keyword(header['ORSEC'+amp])

            if use_active:
                if amp=='A' or amp=='D':
                    ov_col2=np.s_[ov_col[1].start:ov_col[1].stop, 0:100]
                else:
                    ov_col2=np.s_[ov_col[1].start:ov_col[1].stop, 0:100]
            import pdb;pdb.set_trace()

            if 'ORSEC'+amp in header.keys():
                ov_row = parse_sec_keyword(header['ORSEC'+amp])
            elif use_overscan_row:
                log.error('No ORSEC{} keyword; not using overscan_row'.format(amp))
                use_overscan_row = False

            if nogain :
                gain = 1.
            else :
                #- Initial teststand data may be missing GAIN* keywords; don't crash
                if 'GAIN'+amp in header:
                    gain = header['GAIN'+amp]          #- gain = electrons / ADU
                else:
                    if cfinder and cfinder.haskey('GAIN'+amp) :
                        gain = float(cfinder.value('GAIN'+amp))
                        log.info('Using GAIN{}={} from calibration data'.format(amp,gain))
                    else :
                        gain = 1.0
                        log.warning('Missing keyword GAIN{} in header and nothing in calib data; using {}'.format(amp,gain))


            #- Add saturation level
            if 'SATURLEV'+amp in header:
                saturlev = header['SATURLEV'+amp]          # in electrons
            else:
                if cfinder and cfinder.haskey('SATURLEV'+amp) :
                    saturlev = float(cfinder.value('SATURLEV'+amp))
                    log.info('Using SATURLEV{}={} from calibration data'.format(amp,saturlev))
                else :
                    saturlev = 200000
                    log.warning('Missing keyword SATURLEV{} in header and nothing in calib data; using 200000'.format(amp,saturlev))

            # Generate the overscan images
            raw_overscan_col = rawimage[ov_col].copy() # 2064*64

            if use_overscan_row:
                raw_overscan_row = rawimage[ov_row].copy() # 32*2057
                overscan_row = np.zeros_like(raw_overscan_row)

                # Remove overscan_col from overscan_row
                raw_overscan_squared = rawimage[ov_row[0], ov_col[1]].copy() # 32*64
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
                o,r =  _overscan(raw_overscan_col)
                overscan_col += o
                rdnoise  += r

            rdnoise *= gain
            median_rdnoise  = np.median(rdnoise)
            median_overscan = np.median(overscan_col)
    return rdnoise,median_rdnoise

for cam in cam_arr:
    for i in range(n_sp):
        camera=cam.upper()+sp_arr[i]
        ccd_calibration_filename=os.getenv('DESI_SPECTRO_CALIB')+'/spec/sm'+sm_arr[i]+'/sm'+sm_arr[i]+'-'+cam+'.yaml'
        #rdnoise_arr,rdnoise=cal_rdnoise(hdul,camera,ccd_calibration_filename,use_overscan_row,overscan_per_row)
        rdnoise_arr1,rdnoise_median1=cal_rdnoise(hdul,camera,ccd_calibration_filename,False,False,False)
        rdnoise_arr2,rdnoise_median2=cal_rdnoise(hdul,camera,ccd_calibration_filename,True,False,False)
        rdnoise_arr3,rdnoise_median3=cal_rdnoise(hdul,camera,ccd_calibration_filename,True,True,False)
        rdnoise_arr4,rdnoise_median4=cal_rdnoise(hdul,camera,ccd_calibration_filename,False,False,True)
        rdnoise_median1_arr.append(rdnoise_median1)
        rdnoise_median2_arr.append(rdnoise_median2)
        rdnoise_median3_arr.append(rdnoise_median3)
        rdnoise_median4_arr.append(rdnoise_median4)

plt.plot(rdnoise_median1_arr,rdnoise_median2_arr,'+',label='use_overscan_row=True,overscan_per_row=False')
plt.plot(rdnoise_median1_arr,rdnoise_median3_arr,'o',label='use_overscan_row=True,overscan_per_row=True')
plt.plot(rdnoise_median1_arr,rdnoise_median3_arr,'v',label='use_overscan_row=False,overscan_per_row=True')
plt.xlabel('rdnoise use_overscan_row=False')
plt.ylabel('rdnoise')
plt.legend(loc=0)
plt.show()



import pdb;pdb.set_trace()

