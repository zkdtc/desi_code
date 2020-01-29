import os

raw_dir='/exposures/desi/20191023/'
expid_arr=['00020206','00020207']
camera_arr=['b3','r3','z3']
wavelength_arr=['3579.0,5934.0,0.8','5635.0,7731.0,0.8','7445.4,9824.0,0.8']
for expid in expid_arr:
    for i in range(len(camera_arr)):
        cmd='desi_process_exposure -i frame-'+camera_arr[i]+'-'+expid+'.fits --fiberflat fiberflat-sm4-'+camera_arr[i][0]+'-20191022-twilightcorr.fits -o flatfielded-frame-'+camera_arr[i]+'-'+expid+'-twilightcorr.fits'
        print(cmd)
        os.system(cmd)


