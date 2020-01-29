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

class DESI_CATCHUP(object):
    """ Code to catchup a few nights data 
    """

    def __init__(self):
        os.environ['BASEDIR']=os.environ['SCRATCH']+'/desi/realtime9'
        cmd="mkdir -p "+os.environ['BASEDIR']+"/spectro/redux/daily"
        print(cmd)
        os.system(cmd) #subprocess.run(cmd,shell=True,check=True)
        cmd="mkdir -p "+os.environ['BASEDIR']+"/spectro/redux/data"
        print(cmd)
        os.system(cmd) #subprocess.run(cmd,shell=True,check=True)
        #cmd="desi_pipe create --db-postgres --data $BASEDIR/spectro/data --redux $BASEDIR/spectro/redux --prod daily --force"
        #print(cmd)
        #os.system(cmd) #subprocess.run(cmd,shell=True,check=True)
        cmd="source $BASEDIR/spectro/redux/daily/setup.sh"
        print(cmd)
        os.system(cmd) #subprocess.run(cmd,shell=True,check=True)
        cmd="mkdir -p $BASEDIR/spectro/data/"
        print(cmd)
        os.system(cmd) #subprocess.run(cmd,shell=True,check=True)
        os.environ['SVDCDATA']="/global/cscratch1/sd/sjbailey/desi/svdc2019d/spectro/data/"
        night_arr=['20200103','20200107','20200108']
        nersc_queue_arr=['regular','realtime','regular']
        expid_arr=[['00001012','00001013','00001014','00001015','00001016','00001017','00001018','00001019','00001020','00001021','00001022','00001023','00001024','00001025','00001026','00001027','00001028'],
                ['00001087','00001088','00001089','00001090','00001091','00001092','00001093','00001094','00001095','00001096','00001097','00001098','00001099','00001100','00001101','00001102','00001103','00001104','00001105','00001106','00001107','00001108','00001109','00001110','00001111','00001112','00001113','00001114','00001115','00001116','00001117','00001118','00001119','00001120','00001121','00001122'],
                ['00001123','00001124','00001125','00001126','00001127','00001128','00001129','00001130','00001131','00001132','00001133','00001134','00001135','00001136','00001137','00001138','00001139','00001140','00001141','00001142','00001143','00001144','00001145','00001146','00001147','00001148','00001149']
                ]
        science_wait=20
        time_arr=[[20,20,20,  20,20,20,  20,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait],
                  [20,20,20,  20,20,20,  20,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait,science_wait],
                  [20,20,20,  20,20,20, 20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,science_wait]
                  ]
        for i in [1]: #range(len(night_arr)):
            night=night_arr[i]
            self.run_one_night(night,expid_arr[i],time_arr[i],nersc_queue_arr[i])


    def run_one_night(self,night,expid_arr,time_arr,nersc_queue):
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
            cmd="desi_night update --night "+night+" --expid "+expid_arr[i]+" --nersc cori-haswell --nersc_queue "+nersc_queue+" --nersc_maxnodes 10"
            print(cmd)
            import shlex
            args=shlex.split(cmd)
            #print(args)
            #p=subprocess.run(cmd,shell=True,check=True)
            os.system(cmd) #p=subprocess.check_call(cmd,shell=True) 
            #p=subprocess.Popen(args)
            if i == 2:
                cmd="desi_night arcs --night $NIGHT --nersc cori-haswell --nersc_queue "+nersc_queue+" --nersc_maxnodes 10"
                print(cmd)
                try:
                    os.system(cmd) #subprocess.run(cmd,shell=True,check=True)
                except:
                    pass
            elif i== 5:
                cmd="desi_night flats --night $NIGHT --nersc cori-haswell --nersc_queue "+nersc_queue+" --nersc_maxnodes 10"
                try:
                    os.system(cmd) #subprocess.run(cmd,shell=True,check=True)
                except:
                    pass
            elif i==n_exp-1:
                cmd="desi_night redshifts --night $NIGHT --nersc cori-haswell --nersc_queue "+nersc_queue+" --nersc_maxnodes 10"
                try:
                    os.system(cmd) #subprocess.run(cmd,shell=True,check=True)
                except:
                    pass

            time.sleep(time_arr[i])

        
if __name__=="__main__":
    process=DESI_CATCHUP()
