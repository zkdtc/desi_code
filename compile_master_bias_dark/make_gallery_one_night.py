from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from os import listdir
import pdb
from matplotlib.backends.backend_pdf import PdfPages
from scipy.signal import butter, lfilter, freqz
from scipy.signal import savgol_filter


night="20200609"
camera_arr=["b0","b1","b2","r0","r1","r2","z0","z1","z2","b3","b4","b5","r3","r4","r5","z3","z4","z5","b6","b7","b8","b9","r6","r7","r8","r9","z6","z7","z8","z9"]
exptime_arr=[1,          2,         3,          4,         5,       6,          7,         8,         9,         10,       15,          20,      30,        40,         50,        60,        70,        80,       90,        100,       120,       140,        160,      180,     220,     240,       260,     280,      300,        350,    400,       450,      700,    1000,      1200]
expid_arr=["00056872","00056880","00056881","00056882","00056848","00056884","00056885","00056886","00056887","00056888","00056878","00056889","00056874","00056932","00056892","00056947","00056950","00056895","00056962","00056963","00056898","00056980","00056900","00056988","00056902","00056903","00056904","00056905","00056906","00056907","00056908","00056909","00056910","00056911","00056861"] # darks

night='20200607'
expid_arr=['00056569','00056570','00056571','00056572','00056573','00056574','00056575','00056576','00056577','00056578','00056579','00056580','00056583','00056584','00056585','00056586','00056587','00056588','00056589','00056590','00056591','00056592','00056593','00056594','00056595','00056597','00056598','00056599','00056600','00056601','00056602','00056603','00056604','00056610','00056611']
exptime_arr=[0]*len(expid_arr)

night='20200608'
expid_arr=['00056619','00056620','00056621','00056622','00056623','00056629','00056630','00056631','00056632','00056633','00056639','00056640','00056641','00056642','00056643','00056649','00056650','00056651','00056652','00056653','00056659','00056660','00056661','00056662','00056663','00056776','00056777','00056779','00056780','00056782','00056791','00056792','00056793','00056794','00056795','00056796','00056797','00056798','00056799','00056800','00056801','00056802','00056803','00056804','00056805','00056806','00056807','00056808','00056809','00056810','00056811','00056812','00056813','00056814','00056815','00056816','00056817','00056823','00056824','00056825','00056826','00056827','00056833','00056834','00056835','00056836','00056837']
exptime_arr=[0]*len(expid_arr)


night='20200609'
expid_arr=['00056843','00056844','00056845','00056846','00056847','00056853','00056854','00056855','00056856','00056857','00056863','00056864','00056865','00056866','00056867','00056933','00056934','00056935','00056936','00056937','00056968','00056969','00056970','00056971','00056972'] # zeros on 20200609
exptime_arr=[0]*len(expid_arr)

#night='20200728'
#expid_arr=['00060463','00060464','00060465','00060466','00060467','00060468','00060469','00060470','00060471','00060472','00060473','00060474','00060475','00060476','00060477','00060478','00060479','00060480','00060481','00060482','00060483','00060484','00060485','00060486','00060487','00060488','00060489','00060490','00060491','00060492','00060493','00060494','00060495','00060496','00060497','00060498','00060499','00060500','00060501','00060502','00060503','00060504','00060505','00060506','00060507','00060508','00060509','00060510','00060511','00060512','00060513','00060514','00060515','00060516','00060517','00060518','00060523','00060528','00060533','00060539','00060540','00060541','00060542','00060543','00060548'] # zeros on 20200728
#exptime_arr=[0]*len(expid_arr)

#night='20200729'
#expid_arr=['00060553','00060558','00060564','00060565','00060566','00060567','00060568','00060571','00060574','00060577','00060580','00060582','00060583','00060584','00060585','00060586','00060587','00060592','00060597','00060602','00060608','00060609','00060610','00060611','00060612','00060617','00060622','00060627','00060633','00060634','00060635','00060636','00060637','00060638','00060639','00060640','00060641','00060642','00060643','00060644','00060645','00060646','00060647','00060648','00060649','00060650','00060651','00060652','00060653','00060654','00060655','00060656','00060657','00060658','00060659','00060660','00060661','00060662','00060663','00060664','00060665','00060666','00060667','00060668','00060669','00060670','00060671','00060672','00060673','00060674','00060675','00060676','00060677','00060678','00060679','00060680','00060681','00060682','00060687','00060692','00060697','00060703','00060704','00060705','00060706','00060707','00060712']
#exptime_arr=[0]*len(expid_arr)


#night='20200730'
#expid_arr=['00060717','00060722','00060728','00060729','00060730','00060731','00060732','00060735','00060738','00060741','00060744','00060746','00060747','00060748','00060749','00060750','00060751','00060756','00060761','00060766','00060772','00060773','00060774','00060775','00060776','00060779','00060782','00060785','00060788','00060790']
#exptime_arr=[0]*len(expid_arr)

appendix='new'
preproc_dir1="/global/project/projectdirs/desi/users/zhangkai/redux_"+appendix+"bias/"
zmax=0.5
zmin=-0.5
sp_arr=['0', '1','2','3','4','5','6','7','8','9']
sm_arr=['4','10','5','6','1','9','7','8','2','3']
cam_arr=['b','r','z']

outdir='/global/project/projectdirs/desi/users/zhangkai/desi_code/compile_master_bias_dark/gallery/img/'+night+'/'
cmd='mkdir '+outdir
os.system(cmd)


def initialize_html(night):
    strTable="""<html><style>
    h1 {font-family: 'sans-serif';font-size:50px;color:#4CAF50}
    #c {font-family: 'Trebuchet MS', Arial, Helvetica, sans-serif;border-collapse: collapse;width: 100%;}
    #c td, #c th {border: 1px solid #ddd;padding: 8px;}
    #c tr:nth-child(even){background-color: #f2f2f2;}
    #c tr:hover {background-color: #ddd;}
    #c th {padding-top: 12px;  padding-bottom: 12px;  text-align: left;  background-color: #4CAF50;  color: white;}
    .collapsible {background-color: #eee;color: #444;cursor: pointer;padding: 18px;width: 100%;border: none;text-align: left;outline: none;font-size: 25px;}
    .regular {background-color: #eee;color: #444;  cursor: pointer;  padding: 18px;  width: 25%;  border: 18px;  text-align: left;  outline: none;  font-size: 25px;}
    .active, .collapsible:hover {  background-color: #ccc;}
    .content {padding: 0 18px;display: table;overflow: hidden;background-color: #f1f1f1;maxHeight:0px;}
    /* The Modal (background) */
    .modal {
    display: none; /* Hidden by default */
    position: fixed; /* Stay in place */
    z-index: 1; /* Sit on top */
    padding-top: 100px; /* Location of the box */
    left: 0;
    top: 0;
    width: 100%; /* Full width */
    height: 90%; /* Full height */
    overflow: auto; /* Enable scroll if needed */
    background-color: rgb(0,0,0); /* Fallback color */
    background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
    }

    /* Modal Content */
    .modal-content {
    background-color: #fefefe;
    margin: auto;
    padding: 20px;
    border: 1px solid #888;
    width: 80%;
    }

    /* The Close Button */
    .close {
    color: #aaaaaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
    }
    .close:hover,
    .close:focus {
         color: #000;
         text-decoration: none;
         cursor: pointer;
     }
    </style>
    <h1>NIGHT """+night+"""</h1>"""

    return strTable

def add_img(filename):
    return "<img src='"+filename+"' width='60%'>"


for camera in camera_arr:
    #file_html='/global/cfs/cdirs/desi/users/zhangkai/preproc/'+night+'-'+camera+'.html'
    file_html=outdir+'/'+night+'-'+camera+'.html'
    ## Initialize html
    html_str=initialize_html(night)

    if True: #with PdfPages('check_many_darks_to_verify_'+camera+'_'+appendix+'_'+night+'_zeros.pdf') as pdf:
        for expid,exptime in zip(expid_arr,exptime_arr):
            print(camera,expid,exptime)
            outfile_naked='img-'+camera+'-'+expid+'.png'
            outfile=outdir+'/'+outfile_naked
            plt.figure(figsize=(18,18))
            font = {'family' : 'normal',
                 'size'   : 16}
            plt.rc('font', **font)

            file_preproc1=preproc_dir1+'/'+night+'/'+expid+'/preproc-'+camera+'-'+expid+'.fits'
            try:
                hdul1=fits.open(file_preproc1)
                html_str=html_str+add_img(outfile_naked)
            except:
                continue
            nx=len(hdul1[0].data)
            x=np.arange(nx)
            y_hat1 = np.mean(hdul1[0].data[:,1000:1500],axis=1)
            y_hat2 = np.mean(hdul1[0].data[:,2500:3000],axis=1)
            y_hat3=np.mean(hdul1[0].data[1000:1500,:],axis=0)
            y_hat4=np.mean(hdul1[0].data[2500:3000,:],axis=0)


            # Filter the data, and plot both the original and filtered signals.
            #y_filter = butter_lowpass_filter(y_hat1, cutoff, fs, order)
            y_filter= savgol_filter(y_hat1, 101, 2)

            plt.subplot(2,2,1)
            plt.plot(x,y_hat1,label='[1000:1500] column median')
            plt.plot(x,y_hat2+1,label='[2500:3000] column median+1')
            plt.plot([-100,10000],[0,0],'b--')
            plt.plot([-100,10000],[1,1],'b--')
            plt.title('EXPID:'+expid+' EXPTIME='+str(hdul1[0].header['EXPTIME']))
            plt.axis([0,4200,zmin,zmax])
            plt.yscale('linear')
            #plt.yscale('log')
            plt.xlabel('CCD row')
            plt.ylabel('electron/pix')
            plt.title(expid+' '+camera+' EXPTIME='+str(hdul1[0].header['EXPTIME']))
            plt.legend(loc=0)

            plt.subplot(2,2,2)
            plt.plot(y_hat3,label='[1000:1500] row median')
            plt.plot(y_hat4+1,label='[2500:3000] row median+1')
            plt.plot([-100,10000],[0,0],'b--')
            plt.plot([-100,10000],[1,1],'b--')
            plt.axis([0,4200,zmin,zmax])
            plt.yscale('linear')
            #plt.yscale('log')
            plt.xlabel('CCD column')
            plt.ylabel('electron/pix')
            plt.title(expid+' '+camera)
            plt.legend(loc=0)

            plt.subplot(2,2,3)
            plt.imshow(hdul1[0].data,vmin=zmin,vmax=zmax)
            plt.title(expid+' '+camera)
            plt.colorbar()
            
            data1d=hdul1[0].data.ravel()
            std=np.std(data1d[(data1d<10) & (data1d>-10)])

            plt.subplot(2,2,4)
            plt.hist(hdul1[0].data.ravel(),30,range=(-10,10),alpha=0.5)
            plt.title('Std='+str(std)[0:4])
            plt.colorbar()

            plt.tight_layout()
            #pdf.savefig()
            plt.savefig(outfile)
            plt.close()

    html_str=html_str+"</html>"
    hs=open(file_html,'w')
    hs.write(html_str)
    hs.close()


