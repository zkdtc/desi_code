import argparse
import os
import fitsio
import astropy.io.fits as pyfits
import subprocess
import pandas as pd
from desispec.util import runcmd
import errno
import time
import numpy as np
import psycopg2
import hashlib
import pdb
class DESI_DASHBOARD(object):
    """ Code to generate the statistic of desi_pipe production status   
    """

    def __init__(self):
        self.output_dir="/global/project/projectdirs/desi/www/users/zhangkai/desi_dashboard/"
        self.output_url="https://portal.nersc.gov/project/desi/users/zhangkai/desi_dashboard/"
        self.conn=self.get_db_conn(host="nerscdb03.nersc.gov",database="desidev",user="desidev_admin")
        self.cur=self.conn.cursor()
        self.redux_dir="/global/cscratch1/sd/zhangkai/desi/realtime9/spectro/redux/daily"
        self.schema=self._compute_schema(self.redux_dir)
        self.tasktype_arr=['preproc','psf','psfnight','traceshift','extract','fiberflat','fiberflatnight','sky','starfit','fluxcalib','cframe','spectra','redshift']
        self.tasktype_arr_nonight=['spectra','redshift']# Load data 
        for tasktype in self.tasktype_arr:
            cmd="self.get_table(tasktype='"+tasktype+"')"
            exec(cmd)
        nights=np.unique(self.df_preproc['night'])

        strTable=self._initialize_page()
        strTable=strTable+"<button class='regular' id='b1'>Display All Nights</button><button class='regular' id='b2'>Hide All Nights</button>"
        strTable=strTable+"<h2>Data Dir: "+self.redux_dir+"</h2>"
        #### Overall Table ######
        table=self._compute_night_statistic("all")
        strTable=strTable+self._add_html_table_with_link(table,"Overall")
        #### Table for individual night ####
        for night in nights:
            # Create Statistic table for each night 
            table=self._compute_night_statistic(night)
            strTable=strTable+self._add_html_table(table,"Night "+str(night))
            
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        print(timestamp)
        strTable=strTable+"<div style='color:#00FF00'>"+timestamp+"</div>"
        strTable=strTable+self._add_js_script()
        strTable=strTable+"</html>"
        hs=open(self.output_dir+"desi_pipe_dashboard.html",'w')
        hs.write(strTable)
        hs.close()


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
        .content {padding: 0 18px;display: table;overflow: hidden;background-color: #f1f1f1;maxHeight:0px;}</style>
        <h1>DESI PIPELINE STATUS MONITOR</h1>"""

        return strTable

    def _add_html_table(self,table,heading):
        strTable="<button class='collapsible'>"+heading+"</button><div class='content' style='display:inline-block;min-height:0%;'>"
        strTable = strTable+"<table id='c'><tr><th>Tasktype</th><th>waiting</th><th>ready</th><th>running</th><th>done</th><th>failed</th><th>submit</th></tr>"
        for i in range(len(table)):
            try:
                str_row="<tr><td>"+self.tasktype_arr[i]+"</td><td>"+str(table[i][0])+"</td><td>"+str(table[i][1])+"</td><td>"+str(table[i][2])+"</td><td>"+str(table[i][3])+"</td><td>"+str(table[i][4])+"</td><td>"+str(table[i][5])+"</td></tr>"
                strTable=strTable+str_row
            except:
                pass
        strTable=strTable+"</table></div>"
        return strTable

    def _add_html_table_with_link(self,table,heading):
        strTable="<h2>"+heading+"</h2>"
        strTable = strTable+"<table id='c'><tr><th>Tasktype</th><th>waiting</th><th>ready</th><th>running</th><th>done</th><th>failed</th><th>submit</th></tr>"
        for i in range(len(table)):
            tasktype=self.tasktype_arr[i]
            if table[i][4]==0:
                str_row="<tr><td>"+self.tasktype_arr[i]+"</td><td>"+str(table[i][0])+"</td><td>"+str(table[i][1])+"</td><td>"+str(table[i][2])+"</td><td>"+str(table[i][3])+"</td><td>"+str(table[i][4])+"</td><td>"+str(table[i][5])+"</td></tr>"
            else:
                str_row="<tr><td>"+self.tasktype_arr[i]+"</td><td>"+str(table[i][0])+"</td><td>"+str(table[i][1])+"</td><td>"+str(table[i][2])+"</td><td>"+str(table[i][3])+"</td><td><a href='"+self.output_url+"failed_"+tasktype+"_list.html'><font color='red'>"+str(table[i][4])+"</font></a></td><td>"+str(table[i][5])+"</td></tr>"
                loc=locals()
                cmd='df = self.df_'+tasktype
                exec(cmd)
                df=loc['df']
                ind=np.where(df['state'] ==4)[0]
                print(ind)
                strFailed=self._initialize_page()
                strFailed=strFailed+"<h2>Failed "+tasktype+"</h2><table id='c'><tr><th>Name</th></tr>"
                for j in range(len(ind)):
                    strFailed=strFailed+"<tr><td>"+str(df['name'][ind[j]])+"</td></tr>"
                strFailed=strFailed+"</table>"
                hs=open(self.output_dir+"failed_"+tasktype+"_list.html",'w')
                hs.write(strFailed)
                hs.close()
            strTable=strTable+str_row
        strTable=strTable+"</table>"
        return strTable

    def _add_js_script(self):
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


    def get_table(self,tasktype=None):
        if tasktype=='preproc':
            columns=['name','night','band','spec','expid','flavor','state','submitted']
        elif tasktype=='psf' or tasktype=='traceshift' or tasktype=='extract' or tasktype=='fiberflat' or tasktype=='sky' or tasktype=='fluxcalib' or tasktype=='cframe':
            columns=['name','night','band','spec','expid','state','submitted']
        elif tasktype=='psfnight' or tasktype=='fiberflatnight' or tasktype=='starfit':
            columns=['name','night','band','spec','state','submitted']
        elif tasktype=='spectra' or tasktype=='redshift':
            columns=['name','nside','pixel','state','submitted']

        self.cur.execute("select * from "+self.schema+"."+tasktype+";")
        status=self.cur.fetchall()
        cmd="self.df_"+tasktype+"=pd.DataFrame(status,columns=columns)"
        exec(cmd)

    def _compute_night_statistic(self,night):
        n_tasktype=len(self.tasktype_arr)
        n_states=5 # waiting, ready, running, done, failed, submit 
        a=[0]*n_states
        output=[a]*n_tasktype
        if night=="all":
            n_loop=n_tasktype
        else:
            n_loop=n_tasktype-2
        for i in range(n_loop):
            df=0
            tasktype=self.tasktype_arr[i]
            loc=locals()
            cmd='df = self.df_'+tasktype
            exec(cmd)
            df=loc['df']

            temp=[]
            try:
                ind=np.where(df['night']==night)
            except:
                pass
            if night=="all":
                df_this=df
            else:
                try:
                    df_this=df.iloc[ind[0].tolist()]
                except:
                    print(night)
                    import pdb;pdb.set_trace()

            try:
                temp.append(len(np.where(df_this['state'] ==0)[0]))
            except:
                temp.append(0)
                pass
            try:
                temp.append(len(np.where(df_this['state'] ==1)[0]))
            except:
                temp.append(0)
                pass
            try:
                temp.append(len(np.where(df_this['state'] ==2)[0]))
            except:
                temp.append(0)
                pass
            try:
                temp.append(len(np.where(df_this['state'] ==3)[0]))
            except:
                temp.append(0)
                pass
            try:
                temp.append(len(np.where(df_this['state'] ==4)[0]))
            except:
                temp.append(0)
                pass
            try:
                temp.append(len(np.where(df_this['submitted'] ==1)[0]))
            except:
                temp.append(0)
                pass
            output[i]=temp
        return output

    def _compute_schema(self,s):
        import hashlib
        md=hashlib.md5()
        md.update(s.encode())
        return 'pipe_'+md.hexdigest()


    def get_db_conn(self,host=None,database=None,user=None):
        conn=psycopg2.connect(host=host,database=database,user=user)
        conn.autocommit=True
        return conn

        
if __name__=="__main__":
    process=DESI_DASHBOARD()
