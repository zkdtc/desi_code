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
from desispec.io import read_spectra,write_spectra, read_frame_as_spectra
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


class DESI_STACK(object):
    """ Code to stack DESI spectra
    refer to /global/project/projectdirs/desi/users/zhangkai/desi/code/desispec/py/desispec/scripts/coadd_spectra.py
    Example:
    """

    def __init__(self):
        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser = self._init_parser(parser)
        args = parser.parse_args()
        self.args=args
        df_list=pd.read_csv(args.listfile)
        n_obj=len(df_list)
        ind=np.arange(n_obj) # Do not use directly! It is splitted into groups! Use ind_this 
        if use_mpi:
            comm = MPI.COMM_WORLD                                                  
            rank = comm.Get_rank()                                                 
            size = comm.Get_size() 
        
            if rank ==0:
                # Split the input list into N tasks, run separately and combine them together afterward
                ind=np.arange(n_obj)
                ind_chunks=np.array_split(ind,size,axis=0)
            else:
                ind_chunks=None
            ind_this=comm.scatter(ind_chunks,root=0)
            #print("process {} recv ind {} ".format(rank,ind_this))
        else:
            ind_this=ind
        n_this=len(ind_this)
        #wavelength_stack=
        #flux_stack=
        #ivar_stack=

        for i in range(n_this):
            night_this=df_list['night'][ind_this[i]]
            expid_this=df_list['expid'][ind_this[i]]
            expid_this=str(expid_this).zfill(8)
            sp_this=df_list['sp'][ind_this[i]]
            fiber_this=df_list['fiber'][ind_this[i]]
            wavelength,flux,ivar=self.retrive_spectrum(night_this,expid_this,sp_this,fiber_this)
            if i ==0:
                wavelength_stack=wavelength
                flux_stack=flux
                ivar_stack=ivar
                N=1
            else:
                flux_stack=(flux_stack*N+flux)/(N+1)
                N=N+1
            output=[wavelength_stack,flux_stack,ivar_stack,N]

        if use_mpi:
            all_stack= comm.gather(output,root=0)
            if rank==0:
                # Stack again
                for i in range(len(all_stack)):
                    
                    if i==0:
                        wave_out=all_stack[0][0]
                        flux_out=all_stack[0][1]
                        ivar_out=all_stack[0][2]
                        N=all_stack[0][3]
                    else:
                        N_this=all_stack[i][3]
                        flux_out=(flux_out*N+all_stack[i][1]*N_this)/(N+N_this)
                        N=N+N_this
                output=[wave_out,flux_out,ivar_out,N]
        """
        if use_mpi:
            if rank==0:
                plt.plot(output[0],output[1])
                plt.show()
        else:
            plt.plot(output[0],output[1])
            plt.show()
        """




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
    t0=time.time()
    process=DESI_STACK()
    t1=time.time()
    print('Use '+str(t1-t0)+'s to stack')




