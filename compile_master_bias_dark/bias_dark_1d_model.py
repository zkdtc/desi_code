from astropy.io import fits
import pdb
import matplotlib.pyplot as plt
import numpy as np
import copy
import desispec.preproc

camera_arr=['b0','b1','b2','b3','b4','b5','b6','b7','b8','b9']
camera_arr=['b0','z0']
res=10
plot=False
def calculate_dark_fast(exp_arr,image_arr,res=res):
    n_exp=len(exp_arr)
    nx=len(image_arr[0])
    ny=len(image_arr[0][0])
    exp_arr=np.array(exp_arr)

    output=copy.deepcopy(0.*image_arr[0])
    for i in range(int(nx/res)):
        print(i)
        for j in range(int(ny/res)):

            y_temp=[]
            end_x=min([res*i+res,nx-1])
            end_y=min([res*j+res,ny-1])
            for k in range(n_exp):
                y_temp.append(np.median(image_arr[k][res*i:end_x,res*j:end_y].ravel()))
            print(i,j,end_x,end_y,y_temp)
            z=np.polyfit(exp_arr,y_temp,1)
            output[res*i:end_x,res*j:end_y]=z[0]

            print(z[0])
    return output

prefix="master-bias-dark-20200607-20200728-"
for camera in camera_arr:
    filename=prefix+camera+".fits"
    try:
        hdu_this = fits.open(filename)
    except:
        continue
    nx=len(hdu_this[0].data) #4162
    ny=len(hdu_this[0].data[0]) #4232
    #header=hdu_this[exptime].header
    #jj = desispec.preproc.parse_sec_keyword(header['DATASEC'+amp])
    indA = desispec.preproc.parse_sec_keyword('[1:'+str(int(nx/2))+',1:'+str(int(ny/2))+']')
    indB = desispec.preproc.parse_sec_keyword('['+str(int(nx/2)+1)+':'+str(int(nx))+',1:'+str(int(ny/2))+']')
    indC = desispec.preproc.parse_sec_keyword('[1:'+str(int(nx/2))+','+str(int(ny/2)+1)+':'+str(int(ny))+']')
    indD = desispec.preproc.parse_sec_keyword('['+str(int(nx/2)+1)+':'+str(int(nx))+','+str(int(ny/2)+1)+':'+str(int(ny))+']')
    exp_arr=[300,450,700,900,1200]
    image_arr=[]
    for exp in exp_arr:
        image_arr.append(hdu_this[str(exp)].data)

    dark=calculate_dark_fast(exp_arr,image_arr)
    hdr_dark = fits.Header()
    hdr_dark['RES']=str(res)
    dataHDU = fits.ImageHDU(dark,header=hdr_dark, name='dark')
    hdu_this.append(dataHDU)
    #import pdb;pdb.set_trace()
    exptime_arr=[]
    for hdu in hdu_this:
        if hdu.name !='0' and hdu.name !='DARK':
            exptime_arr.append(hdu.name)
    for exptime in exptime_arr:

        ###### Pass1 subtract bias #######
        pass1=hdu_this[exptime].data-hdu_this['0'].data
        pass1_1d=pass1.ravel()
        std_pass1=np.std(pass1_1d[(pass1_1d<100) & (pass1_1d>-10)])
        print('std_pass1',std_pass1)
        correction=1.0
        for i in range(1):
            ###### Pass2 Subtract dark current #######
            print('dark ',np.median(dark))
            pass2=pass1-correction*dark*float(exptime)

            ###### Pass3 subtract 1D profile #######
            profileA=np.median(pass2[indA],axis=1)
            profileB=np.median(pass2[indB],axis=1)
            profileC=np.median(pass2[indC],axis=1)
            profileD=np.median(pass2[indD],axis=1)
            profileLeft=profileA.tolist()+profileD.tolist()
            profileRight=profileB.tolist()+profileC.tolist()
            #profile_1d=np.median(pass2,axis=1) # 4162
            profile_2d_Left=np.transpose(np.tile(profileLeft,(int(ny/2),1)))
            profile_2d_Right=np.transpose(np.tile(profileRight,(int(ny/2),1)))
            profile_2d=np.concatenate((profile_2d_Left,profile_2d_Right),axis=1)
            pass3=pass2-profile_2d
            correction=1.+np.median(pass3.ravel()/(float(exptime)*dark.ravel()))
            data1d=pass3.ravel()
            std=np.std(data1d[(data1d<10) & (data1d>-10)])
            print('correction ',correction,' std ',std)
        # Store pass3 stddev
        hdu_this[exptime].header['res_std']=std
        # Store 1D profile
        hdu_this[exptime].data=[profileLeft,profileRight] #profile_2d

        if plot:
            plt.figure(0,figsize=(20,16))
            font = {'family' : 'sans-serif',
                    'weight' : 'normal',
                    'size'   : 10}
            plt.rc('font', **font)
            plt.subplot(231)
            plt.imshow(pass1,vmin=-1,vmax=5)
            plt.title(camera+' '+exptime+'s After Bias Subtraction')
            plt.colorbar()

            plt.subplot(232)
            plt.imshow(dark,vmin=0,vmax=1.5/750.)
            plt.title('Dark')
            plt.colorbar()

            plt.subplot(233)
            plt.imshow(pass2,vmin=-1,vmax=1)
            plt.title('After removing dark current')
            plt.colorbar()

            plt.subplot(234)
            plt.imshow(profile_2d,vmin=-1,vmax=1)
            plt.title('2D Profile')
            plt.colorbar()

            plt.subplot(235)
            plt.imshow(pass3,vmin=-1,vmax=1)
            plt.title('After 2D Profile Subtraction')
            plt.colorbar()

            plt.subplot(236)
            plt.hist(pass3.ravel(),30,range=(-5,5),alpha=0.5)
            plt.xlabel('Residual')
            plt.title('Std='+str(std)[0:4])
            plt.show()
            print(hdu_this.info())
    hdu_this.writeto(prefix+camera+'-compressed.fits')

