#!/usr/bin/env python

"""
./cal_skyres_skyonly.py -i /project/projectdirs/desi/spectro/redux/daily/exposures/20191111/00027278/frame-r6-00027278.fits --fiberflat /project/projectdirs/desi/spectro/desi_spectro_calib/trunk/spec/sp6/fiberflat-sm7-r-20191108.fits -o test.dat -m rough

./cal_skyres_skyonly.py -i /project/projectdirs/desi/spectro/redux/daily/exposures/20191112/00027405/frame-r6-00027405.fits --fiberflat /project/projectdirs/desi/spectro/desi_spectro_calib/trunk/spec/sp6/fiberflat-sm7-r-20191108.fits -o test.dat -m rough
"""

import os,sys,glob
import argparse
import numpy as np
import astropy.io.fits as pyfits
import matplotlib.pyplot as plt
from teststand.graph_tools import parse_fibers
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
import json
import copy
def reshape(itmp) :
    tmp=np.array(itmp)
    tmp=tmp.reshape((tmp.shape[0]*tmp.shape[1],tmp.shape[2]))
    return tmp

def gaus(x,a,x0,sigma):
    return a*exp(-(x-x0)**2/(2*sigma**2))


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-i','--infile', type = str, default = None, required = True, nargs="*",
                    help = 'path to frame')
parser.add_argument('-t','--title', type = str, default = "skyres", required = False)
parser.add_argument('--fiberflat', type = str, required = True)
parser.add_argument('--satur', type = float, default=None, required = False ,help="mask lines above that level")
parser.add_argument('-o','--outfile', type = str, default = None, required = True,help = 'output file')
parser.add_argument('-m','--std_method', type = str, default = None, required = False,help = 'Method to calculate STD, rough uses 84 percentile minus 16 percentile and divided by 2. Otherwise, fit the distribution.')
args = parser.parse_args()


flux=[]
fflux_arr=[]
ivar=[]
sky=[]

std_method=args.std_method

for filename in args.infile :
    print(filename)
    h=pyfits.open(filename)
    wave=h["WAVELENGTH"].data
    fibers=np.where(h["FIBERMAP"].data["OBJTYPE"]=="SKY")[0] # sky fibers   
    #fibers=np.arange(h["FIBERMAP"].data["OBJTYPE"].size)
    #print("ONLY SOME FIBERS") ; fibers=fibers[fibers<10] 
    fibers_sky=np.where(h["FIBERMAP"].data["OBJTYPE"]=="SKY")[0]
    print("fibers=",fibers,len(fibers))
    print("sky_fibers=",fibers_sky,len(fibers_sky))
    if fibers.size == 0 :
        print("no selected fibers among sky fibers of",filename)
        continue
    camera=h[0].header["camera"].strip()
    print(camera)
    # find corresponding sky
    sky_filename = filename.replace("frame-","sky-").replace("-modmask","")
    if not os.path.isfile(sky_filename) :
        print("no",sky_filename)
        continue
    print(sky_filename)
    h_sky=pyfits.open(sky_filename)
    
    # find corresponding fiberflat
    fiberflat_filename=args.fiberflat
    print(fiberflat_filename)
    h_fiberflat = pyfits.open(fiberflat_filename)
    for fiber in fibers :
        
        fflux=h[0].data[fiber]
        fivar=h["ivar"].data[fiber]*(h["mask"].data[fiber]==0)
        
        flat=h_fiberflat["FIBERFLAT"].data[fiber]
        flat_ivar=h_fiberflat["ivar"].data[fiber]*(h_fiberflat["mask"].data[fiber]==0)
        
        fflux /= flat
        fivar *= flat**2

        fsky=h_sky["SKY"].data[fiber]
        sky_ivar=h_sky["ivar"].data[fiber]*(h_sky["mask"].data[fiber]==0)
        
        fivar *= (sky_ivar>0)*(flat_ivar>0)
        
        # add flatfield error and sky error to inverse variance
        ok=fivar>0
        fivar[ok] = 1./ (  1./fivar[ok] + 1./sky_ivar[ok] )
                
        #fivar[ok] = 1./ (  1./fivar[ok] + 1./sky_ivar[ok]
        #                   + fsky[ok]**2/h_fiberflat["ivar"].data[fiber][ok] )
                           # + 1./sky_ivar[ok] ) # this is negligible, and the code changes sky_ivar
        
        flux.append(h[0].data[fiber])
        fflux_arr.append(fflux)
        ivar.append(fivar)
        sky.append(fsky)
        
    h.close()
    h_sky.close()
    h_fiberflat.close()

flux=np.array(flux)
fflux_arr=np.array(fflux_arr)
ivar=np.array(ivar)
sky=np.array(sky)
res = flux - sky
res_stack=np.sum(res,axis=0)/len(res)
median_res=np.median(res,1)
good_fiber=np.where(np.abs(median_res-np.median(res))<5*np.std(median_res))
good_fiber=np.where(np.abs(median_res-np.median(res))<5*np.std(median_res[good_fiber]))
if args.satur is not None : # mask out saturated sky lines 
    mflux=np.median(flux,axis=0)
    bad=(mflux>args.satur)
    print(bad.shape)
    #enlarge mask
    for d in range(1,10) :
        bad[d:] |= bad[:-d]
        bad[:-d] |= bad[d:] 
    bad=np.where(bad)[0]
    for i in range(ivar.shape[0]) :
        ivar[i,bad]=0. 
##### Finish raw data handling #########
##### Loop over fibers, focus on the central 1000 pixels ########
ormask_f=np.zeros(res.shape[0]) # number of fibers
meansky_f=np.zeros(res.shape[0])
meanres_f=np.zeros(res.shape[0])
rms_f=np.zeros(res.shape[0])
stds_f=np.zeros(res.shape[0])
erms_f=np.zeros(res.shape[0])
erms05_f=np.zeros(res.shape[0])
erms1_f=np.zeros(res.shape[0])
erms2_f=np.zeros(res.shape[0])
erms5_f=np.zeros(res.shape[0])
erms10_f=np.zeros(res.shape[0])
std_sky_f=np.zeros(res.shape[0])


for j in range(res.shape[0]) :  # Loop over fibers
    print(j)
    ok=np.where(ivar[j,:]>0)
    ok=ok[0][800:1000]
    #ok=np.array(list(set(ok[0])&set(good_fiber[0])))
    if np.sum(ok)==0 :
        continue
    meansky_f[j]=np.median(flux[j,ok])
    meanres_f[j]=np.median(res[j,ok])
    rms_f[j]=np.sqrt(np.mean(res[j,ok]**2))
    mean_f = 0#sum(x*y)/n                   #note this correction
    sigma_f = rms_f[j] #sum(y*(x-mean)**2)/n        #note this correction
    if std_method=='rough':
        try:
            std_f=(np.percentile(res[j,ok],84)-np.percentile(res[j,ok],16))/2.
        except:
            std_f=999

    else:
        #### Accurate method to calculate std ####
        nbins=50
        n, bins, patches=plt.hist(res[j,ok],bins=nbins)
        bins2=[(bins[i+1]+bins[i])/2. for i in range(nbins)]
        try:
            popt,pcov = curve_fit(gaus,bins2,n,p0=[1,mean_f,sigma_f])
            std_f=popt[2]
        except:
            std_f=999


    plt.close()  # Release the memory
    stds_f[j]=std_f
    std_sky_f[j]=(std_f**2-np.mean(1./ivar[j,ok]))/(np.mean(flux[j,ok])**2)
    erms_f[j]=np.sqrt(np.mean(1./ivar[j,ok]))
    erms05_f[j]=np.sqrt(np.mean(1./ivar[j,ok]+(0.005*flux[j,ok])**2))
    erms1_f[j]=np.sqrt(np.mean(1./ivar[j,ok]+(0.01*flux[j,ok])**2))
    erms2_f[j]=np.sqrt(np.mean(1./ivar[j,ok]+(0.02*flux[j,ok])**2))
    erms5_f[j]=np.sqrt(np.mean(1./ivar[j,ok]+(0.05*flux[j,ok])**2))
    erms10_f[j]=np.sqrt(np.mean(1./ivar[j,ok]+(0.1*flux[j,ok])**2))
    ormask_f[j]=np.sum(ivar[j,:]==0)
    print(j,std_f,np.mean(1./ivar[j,ok]),std_sky_f[j])



ormask=np.zeros(res.shape[1]) # number of pixels
meansky=np.zeros(res.shape[1])
meanres=np.zeros(res.shape[1])
rms=np.zeros(res.shape[1])
stds=np.zeros(res.shape[1])
erms=np.zeros(res.shape[1])
erms05=np.zeros(res.shape[1])
erms1=np.zeros(res.shape[1])
erms2=np.zeros(res.shape[1])
erms5=np.zeros(res.shape[1])
erms10=np.zeros(res.shape[1])
std_sky=np.zeros(res.shape[1])
errors_mean=np.zeros(res.shape[1])

for j in range(res.shape[1]) :  # Loop over individual pixels
    ok=np.where(ivar[:,j]>0)
    ok=np.array(list(set(ok[0])&set(good_fiber[0])))    
    if np.sum(ok)==0 :
        continue
    meansky[j]=np.median(flux[ok,j])
    meanres[j]=np.median(res[ok,j])
    rms[j]=np.sqrt(np.mean(res[ok,j]**2))
    mean = 0#sum(x*y)/n                   #note this correction
    sigma = rms[j] #sum(y*(x-mean)**2)/n        #note this correction
    if std_method=='rough':
        try:
            std=(np.percentile(res[ok,j],84)-np.percentile(res[ok,j],16))/2.
        except:
            std=999

    else:
        #### Accurate method to calculate std ####
        nbins=50
        n, bins, patches=plt.hist(res[ok,j],bins=nbins)
        bins2=[(bins[i+1]+bins[i])/2. for i in range(nbins)]
        try:
            popt,pcov = curve_fit(gaus,bins2,n,p0=[1,mean,sigma])
            std=popt[2]
        except:
            std=999

    
    plt.close()  # Release the memory
    stds[j]=std
    errors_mean[j]=np.mean(1./ivar[ok,j])
    std_sky[j]=(std**2-errors_mean[j])/(np.mean(flux[ok,j])**2)
    erms[j]=np.sqrt(np.mean(1./ivar[ok,j]))
    erms05[j]=np.sqrt(np.mean(1./ivar[ok,j]+(0.005*flux[ok,j])**2))
    erms1[j]=np.sqrt(np.mean(1./ivar[ok,j]+(0.01*flux[ok,j])**2))
    erms2[j]=np.sqrt(np.mean(1./ivar[ok,j]+(0.02*flux[ok,j])**2))
    erms5[j]=np.sqrt(np.mean(1./ivar[ok,j]+(0.05*flux[ok,j])**2))
    erms10[j]=np.sqrt(np.mean(1./ivar[ok,j]+(0.1*flux[ok,j])**2))
    ormask[j]=np.sum(ivar[:,j]==0)
    print(j,std,np.mean(1./ivar[ok,j]),std_sky[j])

# increase ormask ...
for d in range(1,5) :
    ormask[d:-d]+=ormask[0:-2*d]+ormask[2*d:]
median_flux=np.median(flux,0)
median_fflux=np.median(fflux_arr,0)
median_sky=np.median(sky,0)

# Select only good pixels
ok=np.where((ormask==0)&(rms>0))[0]
ok=np.where((rms>0))[0]
wave0=copy.copy(wave)
res_stack0=copy.copy(res_stack)
wave=wave[ok]
#flux=flux[ok]
#ivar=ivar[ok]
#sky=sky[ok]
res_stack=res_stack[ok]
median_flux=median_flux[ok]
median_fflux=median_fflux[ok]
median_sky=median_sky[ok]
meanres=meanres[ok]
rms=rms[ok]
erms=erms[ok]
erms05=erms05[ok]
erms1=erms1[ok]
erms2=erms2[ok]
erms5=erms5[ok]
erms10=erms10[ok]
stds=stds[ok]
std_sky=std_sky[ok]



output={'wave':wave.tolist(),'median_flux':median_flux.tolist(),'median_fflux':median_fflux.tolist(),'res_stack':res_stack.tolist(),'erms2':erms2.tolist(),'erms1':erms1.tolist(),'erms':erms.tolist(),'rms':rms.tolist(),'meanres':meanres.tolist(),'stds':stds.tolist(),'errors_mean':errors_mean.tolist(),'std_sky':std_sky.tolist(),'wave0':wave0.tolist(),'res_stack0':res_stack0.tolist()}
with open(args.outfile, 'w') as outfile:
    json.dump(output, outfile)
