import os
import desispec.preproc as preproc
import numpy as np
import matplotlib.pyplot as plt
#########################
### Test3 desi_preproc to reduce darks ###
##########################
night="20200609"
expid="00056626" # 900s dark
camera_arr=["b0"]
exptime_arr=[1,          2,         3,          4,         5,       6,          7,         8,         9,         10,       15,          20,      30,        40,         50,        60,        70,        80,       90,        100,       120,       140,        160,      180,     220,     240,       260,     280,      300,        350,    400,       450,      700,    1000,      1200]
expid_arr=["00056872","00056880","00056881","00056882","00056848""00056884","00056885","00056886","00056887","00056888","00056878","00056889","00056874","00056932","00056892","00056947","00056950","00056895","00056962","00056963","00056898","00056980","00056900","00056988","00056902","00056903","00056904","00056905","00056906","00056907","00056908","00056909","00056910","00056911","00056861"]

outdir="/n/home/datasystems/users/zhangkai/redux/newbias/"
for camera in camera_arr:
    for expid,exptime in zip(expid_arr,exptime_arr):
        cmd="desi_preproc -i $DESI_SPECTRO_DATA/"+night+"/"+expid+"/desi-"+expid+".fits.fz -o "+outdir+"/"+night+"/"+expid+"/preproc-"+camera+"-"+expid+".fits --cameras "+camera
        print(cmd)
        os.system(cmd)


"""
desi_proc --batch --nosubmit --cameras b0 b1 b2 -n 20200315 -e 55589
"""

