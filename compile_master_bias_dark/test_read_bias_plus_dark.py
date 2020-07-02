import os
import desispec.preproc as preproc
import numpy as np
import matplotlib.pyplot as plt
############################
## Test1 read_bias_plus_dark
#############################
img=preproc.read_bias_plus_dark(filename='master-bias-dark-20200607-z9.fits',exptime=830)

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
#os.system(cmd)

night="20200609"
expid="00056908" # 400s for interpolation test
camera="b2"
cmd="desi_preproc -i $DESI_SPECTRO_DATA/"+night+"/"+expid+"/desi-"+expid+".fits.fz -o /global/project/projectdirs/desi/users/zhangkai/redux_test/"+night+"/"+expid+"/preproc-"+camera+"-"+expid+".fits --cameras "+camera
print(cmd)
os.system(cmd)


