import os
import numpy as np
from desispec.io import read_frame
from astropy.table import Table
import matplotlib.pyplot as plt
from astropy.stats import sigma_clip

table=Table.read(os.environ["DESIMODEL"]+"/data/focalplane/desi-focalplane_2019-09-16T00:00:00.ecsv", format='ascii.ecsv')
ii=np.where((table["PETAL"]==0)&(table["FIBER"]>=0))[0]
xk="OFFSET_X"
yk="OFFSET_Y"
fiberid="FIBER"
dico={}
for i in ii :
   dico[table[fiberid][i]]=i



frame_file_b3='/project/projectdirs/desi/spectro/redux/v0/exposures/20191028/00022301/frame-b3-00022301.fits'
frame_file_r3='/project/projectdirs/desi/spectro/redux/v0/exposures/20191028/00022301/frame-r3-00022301.fits'
frame_file_z3='/project/projectdirs/desi/spectro/redux/v0/exposures/20191028/00022301/frame-z3-00022301.fits'

sframe_file_b3='/project/projectdirs/desi/spectro/redux/v0/exposures/20191028/00022301/sframe-b3-00022301.fits'
sframe_file_r3='/project/projectdirs/desi/spectro/redux/v0/exposures/20191028/00022301/sframe-r3-00022301.fits'
sframe_file_z3='/project/projectdirs/desi/spectro/redux/v0/exposures/20191028/00022301/sframe-z3-00022301.fits'


frame_b3=read_frame(frame_file_b3)
frame_r3=read_frame(frame_file_r3)
frame_z3=read_frame(frame_file_z3)
sframe_b3=read_frame(sframe_file_b3)
sframe_r3=read_frame(sframe_file_r3)
sframe_z3=read_frame(sframe_file_z3)


flux_b3=frame_b3.flux
flux_r3=frame_r3.flux
flux_z3=frame_z3.flux
sflux_b3=sframe_b3.flux
sflux_r3=sframe_r3.flux
sflux_z3=sframe_z3.flux

fiber=frame_b3.fibermap["FIBER"]-1500
x=np.zeros(fiber.size)
y=np.zeros(fiber.size)

for j,fib in enumerate(fiber) :
   x[j]=table[xk][dico[fib]]
   y[j]=table[yk][dico[fib]]


sky_line1_z3=np.zeros(fiber.size)
sky_cont1_z3=np.zeros(fiber.size)
ssky_line1_z3=np.zeros(fiber.size)
ssky_cont1_z3=np.zeros(fiber.size)

sky_line2_z3=np.zeros(fiber.size)
ssky_line2_z3=np.zeros(fiber.size)

sky_line3_z3=np.zeros(fiber.size)
ssky_line3_z3=np.zeros(fiber.size)

for i in range(fiber.size):
    plt.plot(flux_z3[i])
    plt.plot(sflux_z3[i],color='red')
plt.show()

plt.subplot(331)
for i in range(fiber.size):
    plt.plot(flux_z3[i][1122:1130])
    plt.plot(sflux_z3[i][1122:1130],color='red')

plt.subplot(332)
for i in range(fiber.size):
    plt.plot(flux_z3[i][1724:1734])
    plt.plot(sflux_z3[i][1724:1734],color='red')

plt.subplot(333)
for i in range(fiber.size):
    plt.plot(flux_z3[i][2346:2354])
    plt.plot(sflux_z3[i][2346:2354],color='red')

plt.show()


for i in range(fiber.size):
    plt.figure(0,figsize=(13,13))
    plt.subplot(331)
    plt.plot(flux_z3[i][1122:1130])
    plt.plot(sflux_z3[i][1122:1130],color='red')
    plt.subplot(332)
    plt.plot(flux_z3[i][1724:1734])
    plt.plot(sflux_z3[i][1724:1734],color='red')
    plt.subplot(333)
    plt.plot(flux_z3[i][2346:2354])
    plt.plot(sflux_z3[i][2346:2354],color='red')

    plt.subplot(334)
    plt.plot(sflux_z3[i][1122:1130])
    plt.subplot(335)
    plt.plot(sflux_z3[i][1724:1734])
    plt.subplot(336)
    plt.plot(sflux_z3[i][2346:2354])

    plt.show()

for i in range(fiber.size):
    sky_line1_z3[i]=np.sum(flux_z3[i][1724:1734])
    ssky_line1_z3[i]=np.sum(sflux_z3[i][1724:1734])
    sky_cont1_z3[i]=np.sum(flux_z3[i][850:1000])
    ssky_cont1_z3[i]=np.sum(sflux_z3[i][850:1000])
    sky_line2_z3[i]=np.sum(flux_z3[i][1122:1130])
    ssky_line2_z3[i]=np.sum(sflux_z3[i][1122:1130])
    sky_line3_z3[i]=np.sum(flux_z3[i][2346:2354])
    ssky_line3_z3[i]=np.sum(sflux_z3[i][2346:2354])


sky_line1_z3_norm=sky_line1_z3/np.median(sky_line1_z3)
ssky_line1_z3_norm=ssky_line1_z3/np.median(ssky_line1_z3)
sky_cont1_z3_norm=sky_cont1_z3/np.median(sky_cont1_z3)
ssky_cont1_z3_norm=ssky_cont1_z3/np.median(ssky_cont1_z3)
sky_line2_z3_norm=sky_line2_z3/np.median(sky_line2_z3)
ssky_line2_z3_norm=ssky_line2_z3/np.median(ssky_line2_z3)


s1=30
contrast=2
plt.figure(0,figsize=(12,10))
plt.subplot(331)
d_plot=sky_line1_z3
d_median=np.median(d_plot)
d_std=np.std(d_plot)
plt.scatter(x,y,c=d_plot,cmap="plasma",vmin=d_median-contrast*d_std,vmax=d_median+contrast*d_std,s=s1)
plt.colorbar()
plt.title('frame Z3 Sky Line1')

plt.subplot(332)
d_plot=ssky_line1_z3
d_median=np.median(d_plot)
d_std=np.std(d_plot)
plt.scatter(x,y,c=d_plot,cmap="plasma",vmin=d_median-contrast*d_std,vmax=d_median+contrast*d_std,s=s1)
plt.colorbar()
plt.title('sframe Z3 Sky Line1')

plt.subplot(334)
d_plot=sky_line2_z3
d_median=np.median(d_plot)
d_std=np.std(d_plot)
plt.scatter(x,y,c=d_plot,cmap="plasma",vmin=d_median-contrast*d_std,vmax=d_median+contrast*d_std,s=s1)
plt.colorbar()
plt.title('frame Z3 Sky Line2')

plt.subplot(335)
d_plot=ssky_line2_z3
d_median=np.median(d_plot)
d_std=np.std(d_plot)
plt.scatter(x,y,c=d_plot,cmap="plasma",vmin=d_median-contrast*d_std,vmax=d_median+contrast*d_std,s=s1)
plt.colorbar()
plt.title('sframe Z3 Sky Line2')

plt.subplot(337)
d_plot=sky_line3_z3
d_median=np.median(d_plot)
d_std=np.std(d_plot)
plt.scatter(x,y,c=d_plot,cmap="plasma",vmin=d_median-contrast*d_std,vmax=d_median+contrast*d_std,s=s1)
plt.colorbar()
plt.title('frame Z3 Sky Line3')

plt.subplot(338)
d_plot=ssky_line3_z3
d_median=np.median(d_plot)
d_std=np.std(d_plot)
plt.scatter(x,y,c=d_plot,cmap="plasma",vmin=d_median-contrast*d_std,vmax=d_median+contrast*d_std,s=s1)
plt.colorbar()
plt.title('sframe Z3 Sky Line3')


plt.tight_layout()
plt.show()
import pdb;pdb.set_trace()

