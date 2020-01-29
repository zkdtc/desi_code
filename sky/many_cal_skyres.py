import os
cam_arr=['b','r','z']
num_arr=['0','1','2','3','4','5','6','7']

date='20191029'
expnum='00022586'

cam_arr=['b','r','z']
num_arr=['3']
tail=''
date_arr=  ['20191029','20191029','20191029','20191029','20191029','20191029','20191029','20191029']
expnum_arr=['00022536'] #,'00022549','00022543','00022546','00022577','00022580','00022583','00022586']
"""
cam_arr=['b','r','z']
num_arr=['0','1','2','3','4','5','6','7']
tail=''
date_arr=  ['20191111','20191111','20191111','20191111','20191111','20191111']
expnum_arr=['00027278','00027281','00027282','00027297','00027299','00027301']
tail='.traceshift'
date_arr=  ['20191112','20191112','20191112','20191112','20191112','20191112','20191112','20191112']
expnum_arr=['00027399','00027401','00027403','00027405','00027410','00027412','00027413','00027415']
"""


n_exp=len(expnum_arr)
for i in range(n_exp):
    date=date_arr[i]
    expnum=expnum_arr[i]    
    for cam in cam_arr:
        for num in num_arr:
            #cmd='nohup python3 cal_skyres.py -i /project/projectdirs/desi/spectro/redux/daily/exposures/'+date+'/'+expnum+'/frame-'+cam+num+'-'+expnum+'.fits --fiberflat /project/projectdirs/desi/spectro/desi_spectro_calib/trunk/spec/sp'+num+'/fiberflat-sm'+str(int(num)+1)+'-'+cam+'-20191108.fits -o '+'frame-'+cam+num+'-'+expnum+'.fits.dat -m rough >'+'frame-'+cam+num+'-'+expnum+'.fits.log &'
            cmd='nohup python3 cal_skyres.py -i /project/projectdirs/desi/spectro/redux/v0/exposures/'+date+'/'+expnum+'/frame-'+cam+num+'-'+expnum+'.fits --fiberflat /project/projectdirs/desi/spectro/desi_spectro_calib/trunk/spec/sp'+num+'/fiberflat-sm'+str(int(num)+1)+'-'+cam+'-20191028.fits -o '+'frame-'+cam+num+'-'+expnum+'.fits'+tail+'.dat  -m rough >'+'frame-'+cam+num+'-'+expnum+'.fits'+tail+'.log &'
            print(cmd)
            os.system(cmd)



