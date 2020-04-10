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
cam_arr=['b','r','z']
sp_num_arr=['0','3','6','7','9']
sm_num_arr=['4','6','7','8','3']
tail=''
date_arr=  ['20200219','20200219']
expnum_arr=['00050988','00050995']
date_arr=  ['20200304','20200304','20200304']
expnum_arr=['00053127','00053128','00053129']

sm_num_arr=['1','2','3','4','5','6','7','8','9','10']
sp_num_arr=['4','8','9','0','2','3','6','7','5','1']
tail=''
date_arr=['20200315','20200315','20200315','20200315','20200315','20200315','20200315','20200315','20200315','20200315','20200315','20200315','20200315','20200315','20200315','20200315','20200315']
expnum_arr=['00055589','00055590','00055591','00055592','00055593','00055594','00055611','00055612','00055613','00055626','00055627','00055628','00055639','00055640','00055641','00055642','00055643']


n_exp=len(expnum_arr)
print(cam_arr)
for i in range(n_exp):
    date=date_arr[i]
    expnum=expnum_arr[i]   
    in_dir='/project/projectdirs/desi/spectro/redux/daily/exposures/'+date+'/'+expnum
    for cam in cam_arr:
        print(cam)
        for j in range(len(sp_num_arr)):
            print(j)
            sp_num=sp_num_arr[j]
            sm_num=sm_num_arr[j]

            #cmd='nohup python3 cal_skyres.py -i /project/projectdirs/desi/spectro/redux/daily/exposures/'+date+'/'+expnum+'/frame-'+cam+num+'-'+expnum+'.fits --fiberflat /project/projectdirs/desi/spectro/desi_spectro_calib/trunk/spec/sp'+num+'/fiberflat-sm'+str(int(num)+1)+'-'+cam+'-20191108.fits -o '+'frame-'+cam+num+'-'+expnum+'.fits.dat -m rough >'+'frame-'+cam+num+'-'+expnum+'.fits.log &'
            #cmd='nohup python3 cal_skyres.py -i /project/projectdirs/desi/spectro/redux/v0/exposures/'+date+'/'+expnum+'/frame-'+cam+num+'-'+expnum+'.fits --fiberflat /project/projectdirs/desi/spectro/desi_spectro_calib/trunk/spec/sp'+num+'/fiberflat-sm'+str(int(num)+1)+'-'+cam+'-20191028.fits -o '+'frame-'+cam+num+'-'+expnum+'.fits'+tail+'.dat  -m rough >'+'frame-'+cam+num+'-'+expnum+'.fits'+tail+'.log &'
            #cmd='nohup python3 cal_skyres.py -i /global/cfs/cdirs/desi/spectro/redux/minisv2/exposures/'+date+'/'+expnum+'/frame-'+cam+sp_num+'-'+expnum+'.fits --fiberflat /project/projectdirs/desi/spectro/desi_spectro_calib/trunk/spec/sm'+sm_num+'/fiberflatnight-'+cam+str(int(sp_num))+'-20200125.fits -o '+'frame-'+cam+sp_num+'-'+expnum+'.fits'+tail+'.dat  -m rough >'+'frame-'+cam+sp_num+'-'+expnum+'.fits'+tail+'.log &'
            #print(cmd)
            #os.system(cmd)
            ###   Sky fiber only  ######
            #cmd='nohup python3 cal_skyres_skyonly.py -i /global/cfs/cdirs/desi/spectro/redux/minisv2/exposures/'+date+'/'+expnum+'/frame-'+cam+sp_num+'-'+expnum+'.fits --fiberflat /project/projectdirs/desi/spectro/desi_spectro_calib/trunk/spec/sm'+sm_num+'/fiberflatnight-'+cam+str(int(sp_num))+'-20200125.fits -o '+'frame-'+cam+sp_num+'-'+expnum+'.fits'+tail+'_skyonly.dat  -m rough >'+'frame-'+cam+sp_num+'-'+expnum+'.fits'+tail+'_skyonly.log &'
            #print(cmd)
            #os.system(cmd)
            ### March 15 good night ####
            cmd='nohup python3 cal_skyres_skyonly.py -i' +in_dir+'/frame-'+cam+str(int(sp_num))+'-'+expnum+'.fits --fiberflat /project/projectdirs/desi/spectro/desi_spectro_calib/trunk/spec/sm'+sm_num+'/fiberflatnight-'+cam+str(int(sp_num))+'-20200307-20200315.fits -o '+'frame-'+cam+str(int(sp_num))+'-'+expnum+'.fits'+tail+'_skyonly.dat  -m rough >'+'frame-'+cam+sp_num+'-'+expnum+'.fits'+tail+'_skyonly.log &'
            print(cmd)
            os.system(cmd)


