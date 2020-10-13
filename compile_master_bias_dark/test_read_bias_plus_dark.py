import os
import desispec.preproc as preproc
import numpy as np
import matplotlib.pyplot as plt
############################
## Test1 read_bias_plus_dark
#############################
zmax=5
exptime=0
camera='b0'
expid='test'

img=preproc.read_bias_plus_dark(filename='master-bias-dark-20200607-20200728-b0-compressed.fits',exptime=exptime)
nx=len(img)
x=np.arange(nx)
y_hat1 = np.median(img[:,1000:1500],axis=1)
y_hat2 = np.median(img[:,2500:3000],axis=1)
y_hat3=np.median(img[1000:1500,:],axis=0)
y_hat4=np.median(img[2500:3000,:],axis=0)
plt.figure(figsize=(18,18))
font = {'family' : 'normal',
        'size'   : 16}
plt.rc('font', **font)

plt.subplot(2,2,1)
plt.plot(x,y_hat1,label='[1000:1500] column median')
plt.plot(x,y_hat2+1,label='[2500:3000] column median+1')
plt.plot([-100,10000],[0,0],'b--')
plt.plot([-100,10000],[1,1],'b--')
plt.title('EXPID:'+expid+' EXPTIME='+str(exptime))
plt.axis([0,4200,-1,zmax])
plt.yscale('linear')
plt.xlabel('CCD row')
plt.ylabel('electron/pix')
plt.title(expid+' '+camera+' EXPTIME='+str(exptime))
plt.legend(loc=0)

plt.subplot(2,2,2)
plt.plot(y_hat3,label='[1000:1500] row median')
plt.plot(y_hat4+1,label='[2500:3000] row median+1')
plt.plot([-100,10000],[0,0],'b--')
plt.plot([-100,10000],[1,1],'b--')
plt.axis([0,4200,-1,zmax])
plt.yscale('linear')
plt.xlabel('CCD column')
plt.ylabel('electron/pix')
plt.title(expid+' '+camera)
plt.legend(loc=0)

plt.subplot(2,2,3)
plt.imshow(img,vmin=-1,vmax=zmax)
plt.colorbar()

plt.show()
import pdb;pdb.set_trace()
#################################
### Test2 image interpolation ###
#################################
"""
n = 8
img1 = np.zeros((n, n))
img2 = np.zeros((n, n))

img1[2:4, 2:4] = 1
img2[4:6, 4:6] = 1

plt.figure()
plt.imshow(img1)

plt.figure()
plt.imshow(img2)

img3=preproc.interp_two_images(img1, img2, 0.1)
plt.figure()
plt.imshow(img3)
plt.colorbar()

plt.show()
"""
#########################
### Test3 desi_preproc to reduce darks ###
##########################
night="20200608"
expid="00056626" # 900s dark
camera="b0"
cmd="desi_preproc -i $DESI_SPECTRO_DATA/"+night+"/"+expid+"/desi-"+expid+".fits.fz -o /global/project/projectdirs/desi/users/zhangkai/redux_test/"+night+"/"+expid+"/preproc-"+camera+"-"+expid+".fits --cameras "+camera
print(cmd)
os.system(cmd)

night="20200609"
expid="00056908" # 400s for interpolation test
camera="b2"
cmd="desi_preproc -i $DESI_SPECTRO_DATA/"+night+"/"+expid+"/desi-"+expid+".fits.fz -o /global/project/projectdirs/desi/users/zhangkai/redux_test/"+night+"/"+expid+"/preproc-"+camera+"-"+expid+".fits --cameras "+camera
print(cmd)
os.system(cmd)


