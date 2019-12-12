import json
import matplotlib.pyplot as plt
import numpy as np

with open('frame-r1-00027405.fits.dat') as json_file:
    data=json.load(json_file)

wave=data['wave']
std_sky=np.nan_to_num(data['std_sky'])
stds=np.nan_to_num(data['stds'])
erms1=data['erms1']
print(np.median(std_sky))
import pdb;pdb.set_trace()
plt.plot(wave,erms1,color='green')
plt.plot(wave,stds,color='k')
plt.show()
