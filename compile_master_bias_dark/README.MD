* Pipeline for gnerating new bias+dark files

** Steps
1) Run "python3 generate_darks_list.py". It will give you a list of dark exposures ordered by exptime. Use this list as a reference for the exptime grid you want to compile: exptime_set_arr in step 2. 

2) Revise the "night_arr=['20200607','20200608','20200609'] exptime_set_arr=[1200,900,...,0] in generate_individual_darks.py. then "python3 generate_individual_darks.py". The code will search the raw images in the listed night folders for zeros and darks, group them by the exptime_set_arr. 

3) Revise exptime_set_arr in compile_master_bias_dark.py to the same as in step 2, in generate_individual_darks.py. "python compile_master_bias_dark.py". It will generates master bias+dark grid file for each camera. Make sure the filenmae contains 'bias' and 'dark', they are used to judge if the new bias+dark subtraction code in desispec/preproc.py will be used. 

4) Copy all the master bias+dark files to $DESI_SPECTRO_CALIB/ccd/ . Update the yaml files under $DESI_SPECTRO_CALIB/spec/sm?/sm?-?.yaml to use the new bias+dark images as bias. Dark will be suppressed by codes in preproc.py when reading bias. 

5) Run reduce_darks_to_verify.py to use the new master bias+dark, yaml files and preproc.py code to preprocess a series of darks. 

6) Run check_many_darks_to_verify.py to plot the residuals of the preproccessed images. 
