import argparse
import os
import fitsio
import astropy.io.fits as pyfits
os.environ["MKL_INTERFACE_LAYER"]="GNU"
os.environ["MKL_THREADING_LAYER"]="GNU"
os.environ["OMP_NUM_THREADS"]="24"
os.environ["SPECEXDATA"]="/global/common/software/desi/cori/desiconda/20180709-1.2.6-spec/code/specex/0.6.1/data"
import pandas as pd
from desispec.util import runcmd
import errno
class DESI_PROCESS(object):
    """ Code to reduce any DESI single exposure 
    Example:
    python3 desi_process.py -i /global/project/projectdirs/desi/users/zhangkai/teststand/20180403/data/WINLIGHT_00007850.fits -p psf-r1.fits -c r1 -f fibermap.fits -e 00007850

python3 desi_process.py -i /global/project/projectdirs/desi/users/zhangkai/teststand/20180403/data/WINLIGHT_00007832.fits -p psf-r1.fits -c r1 -f fibermap.fits -e 00007850 -w 5622,7735,0.7

python3 desi_process.py -i /global/project/projectdirs/desi/users/zhangkai/teststand/20180403/data/WINLIGHT_00007805.fits -p psf-r1.fits -c r1 -f fibermap.fits -e 00007805 -ff fiberflat-r1-4s.fits -w 5622,7735,0.7
    Should not present in formal version: 
        add_keyword.py in extract_frame
        declare_sky.py  in fit_sky. Should only be used when dealing with all sky plates. 
    """

    def __init__(self):
        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser = self._init_parser(parser)
        args = parser.parse_args()
        self.args=args
        hdulist = pyfits.open(args.infile)
        try:
            flavor=hdulist[1].header['FLAVOR']
        except:
            #flavor='flat'
            flavor='science'
        #import pdb;pdb.set_trace()
        if flavor=='arc':
            self.process_arc()
        elif flavor=='flat':
            self.process_flat()
        elif flavor=='science':
            self.process_science()

    def _init_parser(self,parser):
        parser.add_argument('-i','--infile', type=str, default = None, required = True, help="input preprocessed image")
        #parser.add_argument('-o','--outfile', type=str, default = None, required = True, help="output preprocessed image")
        parser.add_argument('-p','--psf', type=str, default = None, required = True, help="psf file for traces")
        parser.add_argument('-ff','--fiberflat', type=str, default = None, required = False, help="fiberflat file for extraction")
        parser.add_argument('-c','--camera', type=str, default = None, required = True, help="which camera to process")
        parser.add_argument('-f','--fibermap', type=str, default = None, required = False, help="fibermap to use")
        parser.add_argument('-e','--expnum', type=str, default = None, required = True, help="exposure number")
        parser.add_argument('-w','--wrange', type=str, default = None, required = False, help="wavelength range for fiberflat extraction")
        return parser


    def process_arc(self):
        """
        To reduce an arc exposure
        Input:
            infile: raw arc file
            expnum: exposure number
            cam: camera to process
            psf: psf file
        Output:
            newpsf: psf file
        By product:
            preprocess: preprocced exposure
        """

        preprocess=self.preprocess(self.args.infile, self.args.expnum,self.args.camera)
        newpsf=self.psf_fit(preprocess, self.args.expnum, self.args.camera, self.args.psf)


    def process_flat(self):
        """
        To reduce a flat exposure
        Input:
            infile: raw flat file
            expnum: exposure number
            cam: camera to process
            psf: psf file
            fibermap: fibermap to use
            wrange: wavelength range for extraction
        Output:
            fiberflat: individual fiberflat file generated using flat
        By product:
            shifted_psf: shifted psf
            frame: uncalibrated frame extracted
        """
        expnum=self.args.expnum
        cam=self.args.camera
        preproc=self.preprocess(self.args.infile,self.args.expnum,cam)
        ### Traceshift ###
        shifted_psf=self.shift_trace(preproc,expnum,cam,self.args.psf)
        ### Extrac frame ###
        frame=self.extract_frame(preproc,expnum,cam,shifted_psf,self.args.fibermap,self.args.wrange)
        ### Extract fiberflat ###
        fiberflat=self.make_fiberflat(frame,expnum,cam,shifted_psf)

    def process_science(self):
        """
        To reduce a science exposure
        Input:
            infile: raw science file 
            expnum: exposure number
            cam: camera to process
            psf: psf file
            fibermap: fibermap to use
            wrange: wavelength range for extraction
            fiberflat: stacked or individual fiberflat file generated using flats
        Output:
            cframe: calibrated frame
        By product:
            shifted_psf: shifted psf
            frame: uncalibrated frame extracted
            sky: sky frame
        """
        expnum=self.args.expnum
        cam=self.args.camera
        preproc=self.preprocess(self.args.infile,self.args.expnum,cam)
        ### Traceshift ###
        shifted_psf=self.shift_trace(preproc,expnum,cam,self.args.psf)
        ### Extrac frame ###
        frame=self.extract_frame(preproc,expnum,cam,shifted_psf,self.args.fibermap,self.args.wrange)
        ### Fit Sky ###
        sky=self.fit_sky(frame,expnum,cam,self.args.fiberflat)
        ### Calibration ###
        cframe=self.calibrate(frame,expnum,cam,self.args.fiberflat,sky)


    def preprocess(self,ifile,expnum,cam):    
        ofile='preproc-'+cam+'-'+expnum+'.fits'
        if not (os.path.exists(ifile)):
            raise FileNotFoundError(ifile+' not exists!')
        if not os.path.exists(ofile):
            cmd='desi_preproc --infile '+ifile+' --cam '+cam+' --outfile '+ofile+' --bkgsub'
            print(cmd)
            runcmd(cmd)#+' >>preproc_'+expnum+'.log')
        else:
            print(ofile+' exists\n')
        self._print_blank()
        return ofile

    def psf_fit(self,ifile,expnum,cam,psf):
        ofile='psf-'+cam+'-'+expnum+'.fits'
        if not (os.path.exists(ifile)):
            raise FileNotFoundError(ifile+' not exists!')
        if not os.path.exists(ofile):
            cmd='desi_psf_fit  --half-size-x 4 --half-size-y 4 --gauss-hermite-deg 6 --legendre-deg-wave 4 --legendre-deg-x 4 --trace-deg-wave 6  --in-psf '+psf+' --arc '+ifile+' --out-psf '+ofile
            print(cmd)
            runcmd(cmd)
        else:
            print(ofile+' exists\n')
        self._print_blank()
        return ofile

    def shift_trace(self,ifile,expnum,cam,psf):
        ofile='psf-'+cam+'-shifted-'+expnum+'.fits'
        if not (os.path.exists(ifile)):
            raise FileNotFoundError(ifile+' not exists!')
        if not os.path.exists(ofile):
            cmd='desi_compute_trace_shifts --continuum --image '+ifile+' --psf '+psf+' --outpsf '+ofile+' --max-error 0.5' 
            print(cmd)
            runcmd(cmd)
        else:
            print(ofile+' exists\n')
        self._print_blank()
        return ofile

    def extract_frame(self,ifile,expnum,cam,psf,fibermap,wrange):
        ofile='frame-'+cam+'-'+expnum+'.fits'
        if not (os.path.exists(ifile)):
            raise FileNotFoundError(ifile+' not exists!')
        if not os.path.exists(ofile):
            import subprocess
            use=subprocess.check_output(['which','add_keywords.py'])[0:-1]
            cmd='python3 '+use.decode("utf-8")+' -i '+ifile
            print(cmd)
            runcmd(cmd)
            use=subprocess.check_output(['which', 'desi_extract_spectra'])[0:-1]
            cmd=use.decode("utf-8")+' -i '+ifile+' -o '+ofile+' -p '+psf+' --bundlesize 1 --fibermap '+fibermap+' --wavelength '+wrange
            print(cmd)
            runcmd(cmd)
        else:
            print(ofile+' exists\n')
        self._print_blank()
        return ofile

    def make_fiberflat(self,ifile,expnum,cam):
        ofile='fiberflat-'+cam+'-'+expnum+'.fits'
        if not (os.path.exists(ifile)):
            raise FileNotFoundError(ifile+' not exists!')
        if not os.path.exists(ofile):
            cmd='desi_compute_fiberflat --infile '+ifile+' --outfile '+ofile
            print(cmd)
            runcmd(cmd)
        else:
            print(ofile+' exists\n')
        self._print_blank()
        return ofile

    def fit_sky(self,ifile,expnum,cam,fiberflat):
        ofile='sky-'+cam+'-'+expnum+'.fits'
        if not (os.path.exists(ifile)):
            print(ifile+' not exists!')
            raise FileNotFoundError(ifile+' not exists!')
        if not os.path.exists(ofile):
            cmd='python3 declare_sky_fibers.py -i '+ifile+' --skyfibers=20,22,24,26,28,30,32,34,36,38 >> /dev/null'
            print(cmd)
            runcmd(cmd)
            cmd='desi_compute_sky --infile '+ifile+' --outfile '+ofile+' --fiberflat '+fiberflat+' --cosmics-nsig 10 --no-extra-variance' 
            print(cmd)
            runcmd(cmd)
        else:
            print(ofile+' exists\n')
        self._print_blank()
        return ofile

    def calibrate(self,ifile,expnum,cam,fiberflat,sky):
        ofile='cframe'+cam+'-'+expnum+'.fits'
        if not (os.path.exists(ifile)):
            print(ifile+' not exists!')
            raise FileNotFoundError(ifile+' not exists!')
        if not os.path.exists(ofile):
            cmd='desi_process_exposure --infile '+ifile+' --outfile '+ofile+' --fiberflat '+fiberflat+' --sky '+sky+' --cosmics-nsig 4'
            print(cmd)
            runcmd(cmd)
        else:
            print(ofile+' exists\n')
        self._print_blank()
        return ofile

    def _print_blank(self):
        print('\n\n\n\n\n')

if __name__=="__main__":
    process=DESI_PROCESS()

## desi_bootcalib --fiberflat preproc-b2-00010354.fits --arcfile preproc-b2-00010318.fits --lamps HgI,NeI,ArI,CdI,KrI --outfile psfboot-b2.fits
#desi_bootcalib --fiberflat preproc-r2-00010354.fits --arcfile preproc-r2-00010327.fits --lamps NeI --outfile psfboot-r2.fits
#desi_bootcalib --fiberflat preproc-z2-00010354.fits --arcfile preproc-z2-00010372.fits --lamps HgI,NeI,ArI,CdI,KrI --outfile psfboot-z2.fits



