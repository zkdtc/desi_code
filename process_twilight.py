import os
#expid='00033801' 20191219
expid_arr=['00044457']
night='20200127'
expid_arr=['00055556','00055557','00055558','00055559','00055560','00055561','00055562','00055563','00055564','00055565']
expid_arr=['00055589']
night='20200315'
camera_arr=['b0','b1','b2','b3','b4','b5','b6','b7','b8','b9','r0','r1','r2','r3','r4','r5','r6','r7','r8','r9','z0','z1','z2','z3','z4','z5','z6','z7','z8','z9']
sm_arr=['4','10','5','6','1','9','7','8','2','3','4','10','5','6','1','9','7','8','2','3','4','10','5','6','1','9','7','8','2','3']
product='extendwavelength'

for expid in expid_arr:
    raw_dir='/global/project/projectdirs/desi/spectro/data/'+night+'/'
    in_dir='/project/projectdirs/desi/spectro/redux/'+product+'/exposures_backup/'+night+'/'+expid
    #out_dir='/global/project/projectdirs/desi/users/zhangkai/twilight/'+night+'/'+expid
    out_dir=in_dir

    cmd='mkdir '+out_dir
    print(cmd)
    os.system(cmd)

    #cmd='desi_proc -n 20191219 -e '+expid+' --batch'
    #print(cmd)
    #os.system(cmd)

    for i in range(len(camera_arr)):

        #cmd='desi_process_exposure -i '+out_dir+'/frame-'+camera_arr[i]+'-'+expid+'.fits --fiberflat /project/projectdirs/desi/spectro/redux/daily/exposures/20191217/fiberflatnight-'+camera_arr[i]+'-20191217.fits -o '+out_dir+'/flatfielded-frame-'+camera_arr[i]+'-'+expid+'.fits'
        #cmd='desi_process_exposure -i '+out_dir+'/frame-'+camera_arr[i]+'-'+expid+'.fits --fiberflat /project/projectdirs/desi/spectro/desi_spectro_calib/trunk/spec/sm'+sm_arr[i]+'/fiberflatnight-'+camera_arr[i]+'-20200125.fits -o '+out_dir+'/flatfielded-frame-'+camera_arr[i]+'-'+expid+'.fits'
        #cmd='desi_process_exposure -i '+in_dir+'/frame-'+camera_arr[i]+'-'+expid+'.fits --fiberflat /project/projectdirs/desi/spectro/desi_spectro_calib/trunk/spec/sm'+sm_arr[i]+'/fiberflatnight-'+camera_arr[i]+'-20200307-20200315.fits -o '+out_dir+'/flatfielded-frame-'+camera_arr[i]+'-'+expid+'.fits'
        #print(cmd)
        #os.system(cmd)
        #cmd='desi_process_exposure -i '+in_dir+'/frame-'+camera_arr[i]+'-'+expid+'.fits --fiberflat /global/cfs/cdirs/desi/spectro/redux/daily/calibnight/20200313/fiberflatnight-'+camera_arr[i]+'-20200313.fits -o '+out_dir+'/flatfielded-frame-'+camera_arr[i]+'-'+expid+'.fits'
        #print(cmd)
        #os.system(cmd)

        cmd='desi_process_exposure -i '+in_dir+'/frame-'+camera_arr[i]+'-'+expid+'.fits --fiberflat /global/cfs/cdirs/desi/spectro/redux/extendwavelength/calibnight/fiberflat-'+camera_arr[i]+'-00055714.fits -o '+out_dir+'/flatfielded-frame-'+camera_arr[i]+'-'+expid+'.fits'
        print(cmd)
        os.system(cmd)
