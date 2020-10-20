* Pipeline for gnerating new bias+dark files

** Steps
1) Run "python3 generate_darks_list.py". It will give you a list of dark exposures ordered by exptime. Use this list as a reference for the exptime grid you want to compile: exptime_set_arr in step 2. 

2) Revise the "night_arr=['20200607','20200608','20200609'] exptime_set_arr=[1200,900,...,0] in create_new_master_bias_dark.py. "python compile_master_bias_dark.py". It will generates master bias+dark grid file for each camera. Make sure the filenmae contains 'bias' and 'dark', they are used to judge if the new bias+dark subtraction code in desispec/preproc.py will be used. 

3) python3 bias_dark_1d_model.py to compress the images into 1D profile + 2D darks

4) Copy all the master bias+dark files to $DESI_SPECTRO_CALIB/ccd/ . Update the yaml files under $DESI_SPECTRO_CALIB/spec/sm?/sm?-?.yaml to use the new bias+dark images as bias. Dark will be suppressed by codes in preproc.py when reading bias. 

5) Run reduce_darks_to_verify.py to use the new master bias+dark, yaml files and preproc.py code to preprocess a series of darks. 

6) Run check_many_darks_to_verify.py to plot the residuals of the preproccessed images. 
