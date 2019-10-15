import argparse
import os
import fitsio
import astropy.io.fits as pyfits
import subprocess
#os.environ["MKL_INTERFACE_LAYER"]="GNU"
#os.environ["MKL_THREADING_LAYER"]="GNU"
#os.environ["OMP_NUM_THREADS"]="24"
#os.environ["SPECEXDATA"]="/global/common/software/desi/cori/desiconda/20180709-1.2.6-spec/code/specex/0.6.1/data"
import pandas as pd
from desispec.util import runcmd
import errno
import time
import numpy as np
speed_up_factor=1
class DESI_SIM_NIGHT(object):
    """ Code to simulate night to night operations  
    """

    def __init__(self):
        os.environ['BASEDIR']=os.environ['SCRATCH']+'/desi/realtime10'
        cmd="mkdir -p "+os.environ['BASEDIR']+"/spectro/redux/daily"
        print(cmd)
        os.system(cmd) #subprocess.run(cmd,shell=True,check=True)
        cmd="mkdir -p "+os.environ['BASEDIR']+"/spectro/redux/data"
        print(cmd)
        os.system(cmd) #subprocess.run(cmd,shell=True,check=True)
        a=input('Are you sure you want to create this prod?')
        if a=='Y' or a=='y':
            cmd="desi_pipe create --db-postgres --data $BASEDIR/spectro/data --redux $BASEDIR/spectro/redux --prod daily --force"
            print(cmd)
            os.system(cmd) #subprocess.run(cmd,shell=True,check=True)
        cmd="source "+os.environ['BASEDIR']+"/spectro/redux/daily/setup.sh"
        print(cmd)
        os.system(cmd) #subprocess.run(cmd,shell=True,check=True)
        cmd="mkdir -p $BASEDIR/spectro/data/"
        print(cmd)
        os.system(cmd) #subprocess.run(cmd,shell=True,check=True)
        os.environ['SVDCDATA']="/global/cscratch1/sd/sjbailey/desi/svdc2019d/spectro/data/"
        night_arr=['20200103','20200104','20200105','20200106','20200107','20200108','20200109']
        t0=1570059490
        trigger_time_arr=[t0,t0+1*24*3600, t0+2*24*3600, t0+3*24*3600, t0+4*24*3600,t0+5*24*3600,t0+6*24*3600] # 2019-09-24 16:20 
        expid_arr=[['00001012','00001013','00001014','00001015','00001016','00001017','00001018','00001019','00001020','00001021','00001022','00001023','00001024','00001025','00001026','00001027','00001028'],
                ['00001029','00001030','00001031','00001032','00001033','00001034','00001035','00001036','00001037','00001038','00001039','00001040','00001041'],
                ['00001042','00001043','00001044','00001045','00001046','00001047','00001048','00001049','00001050','00001051','00001052','00001053','00001054','00001055','00001056','00001057','00001058','00001059','00001060','00001061','00001062','00001063','00001064','00001065','00001066','00001067','00001068','00001069','00001070','00001071','00001072','00001073','00001074','00001075','00001076','00001077','00001078','00001079','00001080'],
                ['00001081','00001082','00001083','00001084','00001085','00001086'],
                ['00001087','00001088','00001089','00001090','00001091','00001092','00001093','00001094','00001095','00001096','00001097','00001098','00001099','00001100','00001101','00001102','00001103','00001104','00001105','00001106','00001107','00001108','00001109','00001110','00001111','00001112','00001113','00001114','00001115','00001116','00001117','00001118','00001119','00001120','00001121','00001122'],
                ['00001123','00001124','00001125','00001126','00001127','00001128','00001129','00001130','00001131','00001132','00001133','00001134','00001135','00001136','00001137','00001138','00001139','00001140','00001141','00001142','00001143','00001144','00001145','00001146','00001147','00001148','00001149'],
                ['00001150','00001151','00001152','00001153','00001154','00001155','00001156','00001157','00001158','00001159','00001160','00001161','00001162','00001163','00001164','00001165','00001166','00001167','00001168','00001169','00001170','00001171','00001172','00001173','00001174','00001175','00001176','00001177','00001178','00001179','00001180','00001181','00001182']
                ]

        time_arr=np.array([np.array([180,180,180,  180,180,180,  1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200]),
                  np.array([180,180,180,  180,180,180,  1200,1200,1200,1200,1200,1200,1200]),
                  np.array([180,180,180,  180,180,180,  1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200]),
                  np.array([180,180,180,  180,180,180 ]),
                  np.array([180,180,180,  180,180,180,  1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200]),
                  np.array([180,180,180,  180,180,180, 1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200]),
                  np.array([180,180,180,  180,180,180,  1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200,1200])])
        time_arr=time_arr/speed_up_factor
         
        while True:
            time_now=time.time()
            t=np.array(trigger_time_arr)-time_now
            print('Waiting for new exposures.\n')
            print(t)
            t2=[k for k in t if abs(k)<3000]
            if t2:
                index=t.tolist().index(t2[0]) 
                self.run_one_night(night_arr[index],expid_arr[index],time_arr[index])
            time.sleep(60)


    def run_one_night(self,night,expid_arr,time_arr):
        os.environ['NIGHT']=night
        n_exp=len(expid_arr)
        if (n_exp != len(time_arr)):
            raise Exception("expid_arr and time_arr have different length!")
        for i in range(n_exp):
            os.environ['EXPID']=expid_arr[i]
            cmd="mkdir -p $BASEDIR/spectro/data/$NIGHT/"
            print(cmd)
            os.system(cmd) #subprocess.run(cmd,shell=True,check=True)
            cmd="ln -s $SVDCDATA/$NIGHT/$EXPID $BASEDIR/spectro/data/$NIGHT/$EXPID"
            print(cmd)
            try:
                os.system(cmd) #t=subprocess.run(cmd,shell=True,check=True)
            except:
                pass
            print(os.environ['NIGHT'],'  ',os.environ['EXPID'])
            cmd="desi_night update --night "+night+" --expid "+expid_arr[i]+" --nersc cori-haswell --nersc_queue realtime --nersc_maxnodes 10"
            print(cmd)
            import shlex
            args=shlex.split(cmd)
            #print(args)
            #p=subprocess.run(cmd,shell=True,check=True)
            os.system(cmd) #p=subprocess.check_call(cmd,shell=True) 
            #p=subprocess.Popen(args)
            if i == 2:
                cmd="desi_night arcs --night $NIGHT --nersc cori-haswell --nersc_queue realtime --nersc_maxnodes 10"
                print(cmd)
                try:
                    os.system(cmd) #subprocess.run(cmd,shell=True,check=True)
                except:
                    pass
            elif i== 5:
                cmd="desi_night flats --night $NIGHT --nersc cori-haswell --nersc_queue realtime --nersc_maxnodes 10"
                try:
                    os.system(cmd) #subprocess.run(cmd,shell=True,check=True)
                except:
                    pass
            elif i==n_exp-1:
                cmd="desi_night redshifts --night $NIGHT --nersc cori-haswell --nersc_queue realtime --nersc_maxnodes 10"
                try:
                    os.system(cmd) #subprocess.run(cmd,shell=True,check=True)
                except:
                    pass

            time.sleep(time_arr[i])

        
if __name__=="__main__":
    process=DESI_SIM_NIGHT()
