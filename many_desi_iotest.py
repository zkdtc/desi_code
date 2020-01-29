import os
import time
import argparse
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-l','--log_dir', type=str, default = 'log', required = True, help="Output directory")
args = parser.parse_args()

log_dir=args.log_dir
os.system('mkdir '+log_dir
for i in range(200):
    print(i)
    cmd="strace srun -N 1 -n 30 -q realtime -C haswell python3 desi_iotest.py >>"+log_dir+"/desi_iotest_"+str(i).zfill(3)+".log 2>"+log_dir+"/desi_iotest_"+str(i).zfill(3)+".err &"
    print(cmd)
    os.system(cmd)
    time.sleep(600)


