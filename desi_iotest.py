import argparse
import os
import time
import fitsio
import astropy.io.fits as pyfits
import numpy as np
os.environ["MKL_INTERFACE_LAYER"]="GNU"
os.environ["MKL_THREADING_LAYER"]="GNU"
os.environ["OMP_NUM_THREADS"]="24"
os.environ["SPECEXDATA"]="/global/common/software/desi/cori/desiconda/20180709-1.2.6-spec/code/specex/0.6.1/data"
import pandas as pd
from desispec.util import runcmd
import errno
from desispec.io import read_raw,write_raw,read_spectra,write_spectra, read_frame_as_spectra, write_image
from desispec.coaddition import coadd,coadd_cameras,resample_spectra_lin_or_log
import matplotlib.pyplot as plt
# Multiprocessing environment setup

default_nproc = None
"""Default number of multiprocessing processes. Set globally on first import."""

if "SLURM_CPUS_PER_TASK" in os.environ:
    default_nproc = int(os.environ["SLURM_CPUS_PER_TASK"])
else:
    import multiprocessing as _mp
    default_nproc = max(1, _mp.cpu_count() // 2)

# MPI environment availability

use_mpi = None
"""Whether we should use MPI.  Set globally on first import."""

if ("NERSC_HOST" in os.environ) and ("SLURM_JOB_NAME" not in os.environ):
    use_mpi = False
else:
    use_mpi = True
    try:
        import mpi4py.MPI as MPI
    except ImportError:
        use_mpi = False


class DESI_IOTEST(object):
    """ Code to do IO test
    srun -N 1 -n 30 -q realtime -C haswell python3 desi_iotest.py
    Example:
    """

    def __init__(self):
        pass
        #parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        #parser = self._init_parser(parser)
        #args = parser.parse_args()
        #self.args=args
    def run(self):
        file_dir='/global/cscratch1/sd/zhangkai/desi/test/'
        if use_mpi:
            comm = MPI.COMM_WORLD                                                  
            rank = comm.Get_rank()                                                 
            size = comm.Get_size() 
            test_file=file_dir+'test'+str(rank).zfill(2)+'.fits.fz'
            test_file_output=file_dir+'test'+str(rank).zfill(2)+'_out.fits.fz'
            ##### Read ######
            print('Read '+test_file)
            rawdata=read_raw(test_file ,camera='R1')
            h=fitsio.read_header(test_file,1)
            ##### Write ######
            print('Write '+test_file_output)
            write_image(test_file_output, rawdata) #write_raw(test_file_output,rawdata,None)

        else:
            pass
    def _init_parser(self,parser):
        parser.add_argument('-l','--listfile', type=str, default = None, required = True, help="input list file")
        parser.add_argument('-d','--dir', type=str, default = "/global/cscratch1/sd/zhangkai/desi/realtime8/spectro/redux/daily/exposures", required = False, help="reduced file directory")
        return parser


    def retrive_spectrum(self,night,expid,sp,fiber):
        filename=self.args.dir+'/'+str(night)+'/'+'/'+str(expid)+'/'+'cframe-'+str(sp)+'-'+str(expid)+'.fits'
        d= read_frame_as_spectra(filename)
        band=sp[0]
        return d.wave[band],d.flux[band][fiber],d.ivar[band]

if __name__=="__main__":
    process=DESI_IOTEST()
    process.run()





