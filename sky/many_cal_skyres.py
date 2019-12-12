import os
date='20191112'
expnum='00027405'
cam_arr=['b','r','z']
num_arr=['0','1','2','3','4','5','6','7']

for cam in cam_arr:
    for num in num_arr:
        cmd='nohup python3 cal_skyres.py -i /project/projectdirs/desi/spectro/redux/daily/exposures/'+date+'/'+expnum+'/frame-'+cam+num+'-'+expnum+'.fits --fiberflat /project/projectdirs/desi/spectro/desi_spectro_calib/trunk/spec/sp'+num+'/fiberflat-sm'+str(int(num)+1)+'-'+cam+'-20191108.fits -o '+'frame-'+cam+num+'-'+expnum+'.fits.dat  >'+'frame-'+cam+num+'-'+expnum+'.fits.log &'
        print(cmd)
        os.system(cmd)



