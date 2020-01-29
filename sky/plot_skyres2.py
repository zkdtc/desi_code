#!/usr/bin/env python

"""
./plot_skyres2.py -i /project/projectdirs/desi/spectro/redux/daily/exposures/20191111/00027278/frame-r6-00027278.fits --fiberflat /project/projectdirs/desi/spectro/desi_spectro_calib/trunk/spec/sp6/fiberflat-sm7-r-20191108.fits -o test.dat

./plot_skyres2.py -i /project/projectdirs/desi/spectro/redux/daily/exposures/20191112/00027405/frame-r6-00027405.fits --fiberflat /project/projectdirs/desi/spectro/desi_spectro_calib/trunk/spec/sp6/fiberflat-sm7-r-20191108.fits -o test.dat

./plot_skyres2.py -i /project/projectdirs/desi/spectro/redux/v0/exposures/20191029/00022536/frame-r3-00022536.fits --fiberflat /project/projectdirs/desi/spectro/desi_spectro_calib/trunk/spec/sp3/fiberflat-sm4-r-20191028.fits -o test.dat
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

args = parser.parse_args()


flux=[]
ivar=[]
sky=[]

for filename in args.infile :
    print(filename)
    h=pyfits.open(filename)
    wave=h["WAVELENGTH"].data
    fibers=np.where(h["FIBERMAP"].data["OBJTYPE"]!="SKY")[0] # non sky fibers   
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
        ivar.append(fivar)
        sky.append(fsky)
        
    h.close()
    h_sky.close()
    h_fiberflat.close()

flux=np.array(flux)
ivar=np.array(ivar)
sky=np.array(sky)
res = flux - sky
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

for j in range(res.shape[1]) :  # Loop over individual pixels
    print(j)
    ok=np.where(ivar[:,j]>0)
    ok=np.array(list(set(ok[0])&set(good_fiber[0])))    
    if np.sum(ok)==0 :
        continue
    meansky[j]=np.median(flux[ok,j])
    meanres[j]=np.median(res[ok,j])
    rms[j]=np.sqrt(np.mean(res[ok,j]**2))
    mean = 0#sum(x*y)/n                   #note this correction
    sigma = rms[j] #sum(y*(x-mean)**2)/n        #note this correction
    nbins=50
    plot=0
    """
    if plot==1:
        fig, ax = plt.subplots()
        n, bins, patches=ax.hist(res[ok,j],bins=nbins)
    else:
        n, bins, patches=plt.hist(res[ok,j],bins=nbins)
    bins2=[(bins[i+1]+bins[i])/2. for i in range(nbins)]
    try:
        popt,pcov = curve_fit(gaus,bins2,n,p0=[1,mean,sigma])
        if plot==1:
            ax.plot(bins2,gaus(bins2,*popt),'ro:',label='fit')
        std=abs(popt[2])
    except:
        std=999

    """
    std=0.
    if plot==1:
        ax.text(0.7, 0.8, 'rms='+str(rms[j]), horizontalalignment='center',verticalalignment='center', transform=ax.transAxes)
        ax.text(0.7, 0.7, 'fit='+str(std), horizontalalignment='center',verticalalignment='center', transform=ax.transAxes)
        plt.show()
    plt.close()  # Release the memory
    stds[j]=std
    
    std_sky[j]=100.*np.sqrt(std**2-np.mean(1./ivar[ok,j]))/np.mean(flux[ok,j])
    erms[j]=np.sqrt(np.mean(1./ivar[ok,j]))
    erms05[j]=np.sqrt(np.mean(1./ivar[ok,j]+(0.005*flux[ok,j])**2))
    erms1[j]=np.sqrt(np.mean(1./ivar[ok,j]+(0.01*flux[ok,j])**2))
    erms2[j]=np.sqrt(np.mean(1./ivar[ok,j]+(0.02*flux[ok,j])**2))
    erms5[j]=np.sqrt(np.mean(1./ivar[ok,j]+(0.05*flux[ok,j])**2))
    erms10[j]=np.sqrt(np.mean(1./ivar[ok,j]+(0.1*flux[ok,j])**2))
    ormask[j]=np.sum(ivar[:,j]==0)
    print(rms[j],std,np.sqrt(np.mean(1./ivar[ok,j])),std_sky[j])


if 0 :
    plt.figure("skyflux")
    plt.plot(wave,meansky,c="red",label="measured mean flux from arc lines (electrons/A)")
    if 1 :
        h=pyfits.open("/global/projecta/projectdirs/desi/spectro/redux/month4/exposures/20191001/00003577/sky-r0-00003577.fits")
        plt.plot(h["WAVELENGTH"].data,h["SKY"].data[12],"-",color="blue",label="DESI dark sky spectrum (electrons/A)")
    plt.legend(loc="upper left",fontsize="small")

# increase ormask ...
for d in range(1,5) :
    ormask[d:-d]+=ormask[0:-2*d]+ormask[2*d:]

ok=np.where((ormask==0)&(rms>0))[0]
ok=np.where((rms>0))[0]
wave=wave[ok]
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


fig=plt.figure("residuals")
if 1 :
    for i in range(res.shape[0]) :
        label=None
        if i==0 : label="individual fiber/exposure residual"
        plt.plot(wave,res[i][ok],alpha=0.2,color="gray",label=label)
lw=2

ax1 = fig.add_subplot(111)
ax2 = ax1.twiny()


new_tick_locations = np.arange(52)*50


#plt.plot(wave,erms10,"--",c="brown",label="readout+poisson noise + 10% sky")
#plt.plot(wave,erms5,"--",c="red",label="readout+poisson noise + 5% sky")
ax1.plot(wave,erms2,"--",c="red",lw=lw,label="expected rms from readout+poisson noise + 2% sky")
ax1.plot(wave,erms1,"--",c="orange",lw=lw,label="expected rms from readout+poisson noise + 1% sky")
#plt.plot(wave,erms05,"--",c="g",lw=lw,label="expected rms from readout+poisson noise + 0.5% sky")
ax1.plot(wave,erms,"--",c="green",lw=lw,label="expected rms from readout+poisson noise")
ax1.plot(wave,rms,c="k",lw=lw,label="measured rms of 'sky' residual")
ax1.plot(wave,meanres,c="blue",lw=lw,alpha=0.6,label="median residual")
ax2.set_xlim(ax1.get_xlim())
ax2.set_xticks(new_tick_locations+ax1.get_xlim()[0])
ax2.set_xticklabels(new_tick_locations.tolist())
ax2.set_xlabel(r"Pixel Number")


ax1.legend(loc="lower left",fontsize="medium")
ax1.set_xlabel(r"wavelength (A)")
ax1.set_ylabel(r"electrons/A")
ax1.grid()

plt.show()

#plt.plot(wave,std_sky,c="k")
#plt.show()

output={'wave':wave.tolist(),'erms2':erms2.tolist(),'erms1':erms1.tolist(),'erms':erms.tolist(),'rms':rms.tolist(),'meanres':meanres.tolist(),'stds':stds.tolist(),'std_sky':std_sky.tolist()}
with open(args.outfile, 'w') as outfile:
    json.dump(output, outfile)


import pdb;pdb.set_trace()
