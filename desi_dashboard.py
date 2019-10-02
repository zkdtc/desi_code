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
        self.conn=self.get_db_conn(host="nerscdb03.nersc.gov",database="desidev",user="desidev_admin")
        self.cur=self.conn.cursor()
        self.schema=self._compute_schema('/global/cscratch1/sd/zhangkai/desi/realtime8/spectro/redux/daily')
        self.tasktype_arr=['preproc','psf','psfnight','traceshift','extract','fiberflat','fiberflatnight','sky','starfit','fluxcalib','cframe','spectra','redshift']
        # Load data 
        for tasktype in self.tasktype_arr:
            cmd="self.get_table(tasktype='"+tasktype+"')"
            exec(cmd)
        nights=np.unique(self.df_preproc['night'])
        strTable="<html><style> table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}"
        strTable=strTable+"td, th {border: 1px solid #dddddd;text-align: left;padding: 8px;}"
        strTable=strTable+"tr:nth-child(even) {background-color: #dddddd;}</style>"
        #### Overall Table ######
        table=self._compute_night_statistic("all")
        strTable=strTable+self._add_html_table(table,"Overall")
        #### Table for individual night ####
        for night in nights:
            # Create Statistic table for each night 
            table=self._compute_night_statistic(night)
            strTable=strTable+self._add_html_table(table,"Night "+str(night))
            
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        print(timestamp)
        strTable=strTable+"<div style='color:#00FF00'>"+timestamp+"</div></html>"
        hs=open("/global/project/projectdirs/desi/www/users/zhangkai/desi_dashboard/desi_pipe_dashboard.html",'w')
        hs.write(strTable)

    def _add_html_table(self,table,heading):
        strTable="<h1>"+heading+"</h1>"
        strTable = strTable+"<table><tr><th>Tasktype</th><th>waiting</th><th>ready</th><th>running</th><th>done</th><th>failed</th><th>submit</th>"
        for i in range(len(table)):
            str_row="<tr><td>"+self.tasktype_arr[i]+"</td><td>"+str(table[i][0])+"</td><td>"+str(table[i][1])+"</td><td>"+str(table[i][2])+"</td><td>"+str(table[i][3])+"</td><td>"+str(table[i][4])+"</td><td>"+str(table[i][5])+"</td></tr>"
            strTable=strTable+str_row
        strTable=strTable+"</table>"
        return strTable


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
        for i in range(n_tasktype):
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
                df_this=df.loc[ind]

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
