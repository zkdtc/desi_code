import argparse
import os,glob
import fitsio
import astropy.io.fits as pyfits
from astropy.io import fits
import subprocess
import pandas as pd
import time,datetime
import numpy as np
import psycopg2
import hashlib
import pdb
import psutil
from os import listdir

class DESI_PROC_CALIBNIGHT_DASHBOARD(object):
    """ Code to generate the statistic of desi_pipe calibnight status   
    Usage:
    python3 desi_proc_calibnight_dashboard.py --nights 2020125,20200127 --n_nights 100 --prod_dir /global/cscratch1/sd/zhangkai/desi/ --output_dir /global/project/projectdirs/desi/www/users/zhangkai/desi_proc_calibnight_dashboard/
    """

    def __init__(self):
        ############
        ## Input ###
        ############
        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser = self._init_parser(parser)
        args = parser.parse_args()
        if not os.getenv('DESI_SPECTRO_REDUX'):
            os.environ['DESI_SPECTRO_REDUX']='/global/project/projectdirs/desi/spectro/redux/'
            os.environ['DESI_SPECTRO_DATA']='/global/project/projectdirs/desi/spectro/data/'
            os.environ['SPECPROD']='daily'
        if args.nights=='all':
            nights=listdir(os.getenv('DESI_SPECTRO_REDUX')+'/'+os.getenv('SPECPROD')+'/calibnight/')
            nights=[int(x) for x in nights]
        else:
            try:
                print(args.nights)
                if len(args.nights)==1: # list separted by , or a single night
                    nights=[int(night) for night in args.nights[0].split(',')]
                else:
                    nights=[int(night) for night in args.nights]
                print('Get nights',nights)
            except:
                nights=[]

        tonight=self.what_night_is_it()
        if not tonight in nights:
            nights.append(tonight)
        nights.sort(reverse=True)
        if int(args.n_nights)<=len(nights):
            nights=nights[0:int(args.n_nights)-1]
        print('Find ',nights)
        prod_dir=args.prod_dir # base directory of product
        self.output_dir=args.output_dir # Portal directory for output html files

        strTable=self._initialize_page()

        for night in nights:
            #print(night)
            stat_night=self.calculate_one_night(night)
            ####################################
            #### Table for individual night ####
            ####################################
            strTable=strTable+self._add_html_table(stat_night,str(night))
            
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        #print(timestamp)
        running=self.check_running()
        strTable=strTable+"<div style='color:#00FF00'>"+timestamp+" "+"desi_dailyproc running: "+running+"</div>"
        strTable=strTable+self._add_js_script1()
        strTable=strTable+"</html>"
        hs=open(self.output_dir+"desi_proc_calibnight_dashboard.html",'w')
        hs.write(strTable)
        hs.close()

        ##########################
        #### Fix Permission ######
        ##########################
        cmd="chmod -R a+xr "+self.output_dir
        os.system(cmd)

    def _init_parser(self,parser):
        parser.add_argument('-n','--nights', type=str, default = None, required = False, help="nights to monitor")
        parser.add_argument('-nn','--n_nights', type=str, default = None, required = False, help="all:all nights. ifdigit: the last n nights.")
        parser.add_argument('-pd','--prod_dir', type=str, default = None, required = True, help="product base directory")
        parser.add_argument('-od','--output_dir', type=str, default = None, required = True, help="output portal directory for the html pages ")
        return parser

    def calculate_one_night(self,night):
        #print(expid,flavor,obstype)
        fileglob_psf='/project/projectdirs/desi/spectro/redux/daily/calibnight/'+str(night)+'/psf*.fits'
        fileglob_fiberflat='/project/projectdirs/desi/spectro/redux/daily/calibnight/'+str(night)+'/fiberflat*.fits'
        file_psf=sorted(glob.glob(fileglob_psf))
        file_fiberflat=sorted(glob.glob(fileglob_fiberflat))
        psf_mask_arr=[]
        fflat_mask_arr=[]
        #for file_p in file_psf:
        #    print(file_p)
        #    d=fitsio.FITS(file_p)
        #    psf_mask_arr.append(len(ind[0])/500.)
        for file_f in file_fiberflat:
            cam=file_f.split('-')[-2]
            d=fitsio.FITS(file_f)
            ind=np.where(d[2][:,:]!=0)
            fflat_mask_arr.append(cam)
            fflat_mask_arr.append(str(int(len(ind[0])/500.)))
        output={'n_psf':len(file_psf),'n_fflat':len(file_fiberflat),'fflat_mask_arr':fflat_mask_arr}
        return(output)

    def _initialize_page(self):
        #strTable="<html><style> table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}"
        #strTable=strTable+"td, th {border: 1px solid #dddddd;text-align: left;padding: 8px;}"
        #strTable=strTable+"tr:nth-child(even) {background-color: #dddddd;}</style>"
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
        <h1>DESI PROC STATUS MONITOR</h1>"""

        return strTable

    def _add_html_table(self,table,night):
        heading="Night "+night
        strTable="<button class='collapsible'>"+heading+"</button><div class='content' style='display:inline-block;min-height:0%;'>"
        strTable = strTable+"<table id='c'><tr><th>N psfnight</th><th>N fiberflatnight</th><th>average fiberflat mask (per fiber)</th></tr>"
        n_spectrographs=len(table['fflat_mask_arr'])

        n_ref=[str(n_spectrographs),str(n_spectrographs),'2']

        color="green"
        str_row="<tr><td>"+str(table['n_psf'])+'/'+n_ref[0]+"</td><td>"+str(table['n_fflat'])+'/'+n_ref[1]+"</td><td>"+str(table['fflat_mask_arr'])+'/'+n_ref[2]+"</td></tr>"

        strTable=strTable+str_row
        strTable=strTable+"</table></div>"
        return strTable


    def _add_js_script1(self):
        s="""<script>
            var coll = document.getElementsByClassName('collapsible');
            var i;
            for (i = 0; i < coll.length; i++) {
                coll[i].nextElementSibling.style.maxHeight='0px';
                coll[i].addEventListener('click', function() {
                    this.classList.toggle('active');
                    var content = this.nextElementSibling;
                    if (content.style.maxHeight){
                       content.style.maxHeight = null;
                    } else {
                      content.style.maxHeight = '0px';
                            } 
                    });
             };
             var b1 = document.getElementById('b1');
             b1.addEventListener('click',function() {
                 for (i = 0; i < coll.length; i++) {
                     coll[i].nextElementSibling.style.maxHeight=null;
                                                   }});
             var b2 = document.getElementById('b2');
             b2.addEventListener('click',function() {
                 for (i = 0; i < coll.length; i++) {
                     coll[i].nextElementSibling.style.maxHeight='0px'
                             }});
            </script>"""
        return s

    def _add_js_script2(self,n_modal):
        s="""<script>"""
        for i in range(n_modal):
            s=s+"""
                var modal"""+str(i)+""" = document.getElementById('modal"""+str(i)+"""');
                var l"""+str(i)+""" = document.getElementById('Btn"""+str(i)+"""');

                l"""+str(i)+""".addEventListener('click',function() {
                  modal"""+str(i)+""".style.display = "block";
                })

                span"""+str(i)+""".addEventListener('click',function() {
                  modal"""+str(i)+""".style.display = "none";
                })"""

        s=s+"""</script>"""
        return s



    def what_night_is_it(self):
        d = datetime.datetime.utcnow() - datetime.timedelta(7/24+0.5)
        tonight = int(d.strftime('%Y%m%d'))
        return tonight

    def find_newexp(self,night, fileglob, known_exposures):
        datafiles = sorted(glob.glob(fileglob))
        newexp = list()
        for filepath in datafiles:
            expid = int(os.path.basename(os.path.dirname(filepath)))
            if (night, expid) not in known_exposures:
                newexp.append( (night, expid) )
        return set(newexp)
    def check_running(self):
        a=psutil.process_iter()
        running='No'
        for p in a:
            if 'desi_dailyproc' in ' '.join(p.cmdline()):
                running='Yes'
        return running

        
if __name__=="__main__":
    process=DESI_PROC_CALIBNIGHT_DASHBOARD()
