import os

frame_dir='/exposures/nightwatch/redux/v0/exposures/20191028/'
data_dir='/software/datasystems/users/zhangkai/20191028/'
expid_arr=['00022434','00022435','00022436'] #['00022422','00022423','00022424','00022425','00022426','00022427','00022428','00022429','00022430','00022431','00022432','00022433',]
camera_arr=['b3','r3','z3']
wavelength_arr=['3579.0,5934.0,0.8','5635.0,7731.0,0.8','7445.4,9824.0,0.8']
for expid in expid_arr:
    for i in range(len(camera_arr)):
        cmd='desi_process_exposure -i '+frame_dir+'/'+expid+'/frame-'+camera_arr[i]+'-'+expid+'.fits --fiberflat /exposures/nightwatch/redux/v0/exposures/20191028/merged-fiberflat-'+camera_arr[i][0]+'-3-autocal.fits -o '+data_dir+'/flatfielded-frame-'+camera_arr[i]+'-'+expid+'.fits'
        print(cmd)
        os.system(cmd)


