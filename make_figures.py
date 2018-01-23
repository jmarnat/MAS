#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
#import numpy as np
from os import chdir
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


chdir('/home/jmarnat/Documents/MAS/MAS/')
d = pd.read_csv('./all-sub-incremental-3-15.csv')


#plt.plot(d['sub'],d['time'])
#plt.scatter(x=d['sub'],y=d['time'])

#d['agent'=='AFB',]

#for ag in ['AFB',']

legend = {}
legend['ADOPT']   = 'rD-'
legend['AFB']     = 'bs-'
legend['DPOP']    = 'g^-'
legend['DSA']     = 'cv-'
legend['MGM']     = 'mo-'
legend['MaxSum']  = 'kx-'
legend['SynchBB'] = 'yd-'

#one of {'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'};



###################################
# PLOT OF TIME MESSAGES AND BYTES #
###################################
subs = ['time','mes','mean_mes','bytes','mean_bytes']
ysc = ['log','linear','linear','log','log']
fig = plt.figure(dpi=100, figsize=[12,8])

for i in range(0,5):
    ax = fig.add_subplot(2,3,i+1)
    for ag in legend.keys():
        da = d.query('agent == "'+str(ag)+'"')
        ax.plot(da['sub'],da[subs[i]],legend[ag])
        ax.set_yscale(ysc[i])
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax.set_xlabel('#variables')
        ax.set_ylabel(subs[i]+' ('+ysc[i]+')')

ax.legend(legend.keys(), bbox_to_anchor=(1.5,0.5),loc="center left")
#fig.suptitle('Evolution of time, #messages and #bytes in function of #variables', fontsize=20)
fig.tight_layout()
fig.savefig('all-subs.png')
plt.show()


