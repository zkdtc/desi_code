import os
night_arr=['20200305','20200306','20200307','20200308','20200309','20200312','20200313','20200314','20200315']
for night in night_arr:
    cmd='nohup python3 reduce_zero.py '+night+' >>reduce_zero_'+night+'.log &'
    a=os.system(cmd)

