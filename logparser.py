#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import pandas as pd

def get_int(line):
    return int(re.sub(r'\D','',line))

def log_path(path_tmp, scene, subset, agent):
    return path_tmp+'/scen'+str(scene).zfill(2)+'-'+str(subset)+'-'+str(agent)+'.log'


def parse(filename, debug=False):
    match = ''
    
    # list of variables:
    algotime = 0
    num_agts = 0
    num_bytes = 0
    num_mes = 0

    
    
    lines = open(filename).readlines()
    for fullline in lines:
        line = fullline.rstrip('\n')
        # print(line)
        
        '''----------------'''
        ''' regex matching '''
        '''----------------'''
        if re.match(r'Algorithm finished in',line):
            match = 'algotime'
        
        elif re.match(r'Number of messages sent .* type',line):
            match = 'num_sent_type'
        elif (match == 'num_sent_type') and re.match(r'.*Total.*',line):
            match = 'num_sent_type_total'
        
        elif re.match(r'Number of messages sent .* agent',line):
            match = 'num_sent_agt'
        elif (match == 'num_sent_agt') and re.match(r'.*agt_.*',line):
            match = 'agt_sent'
        elif re.match(r'Number of messages received.*',line):
            match = ''
        elif re.match(r'Amount of information sent .* type',line):
            match = 'info_sent_type'
        elif (match == 'info_sent_type') and re.match(r'.*Total.*',line):
            match = 'info_sent_type_tot'
        
        '''------------------'''
        ''' infos extracting '''
        '''------------------'''
        if match == 'algotime':
            algotime = get_int(line)
            match = ''
        elif match == 'num_sent_type_total':
            num_mes = get_int(line)
            match = ''
        elif match == 'info_sent_type_tot':
            num_bytes = get_int(line)
            match = ''
        elif match == 'agt_sent':
            tmp = re.sub(r'.*:','',line)
            num_agts += 1
            num_bytes += get_int(tmp)
            match = 'num_sent_agt'

    if (debug):
        print()
        print('algo time:<'+str(algotime)+'> ms')
        print('number of agents:             <'+str(num_agts)+'>')
        print('number of messages sent:      <'+str(num_mes)+'>')
        print('avg num of messages / agent:  <'+str(num_mes/num_agts)+'>')
        print('number of bytes transmitted:  <'+str(num_bytes)+'>')
        print('avg num of bytes / agent:     <'+str(num_bytes/num_agts)+'>')
        #print('byte_rec_agts:<'+str(byte_rec_agts)+'>')
        #print('avg_rec_agts:<'+str(byte_rec_agts/num_agts)+'>')

#    d = {'time':[algotime], 'num_agts':[num_agts], 'num_mes':[num_mes], 'num_bytes':[num_bytes]}
    d = [algotime, num_agts, num_mes, num_bytes]
    df = pd.DataFrame(data = d,)#, columns = ['time','agts','mes','bytes'])
    df = df.T
    df.columns = ['time','agts','mes','bytes']
    if (debug): print(df)
    return df
  
#big_df = pd.DataFrame(columns=['scene','agent','time','agts','mes','mean_mes','bytes','mean_bytes'])          
#df1 = parse('/home/jmarnat/Documents/MAS/MAS/tmp_mas/scen01-100-AFB.log')
#df2 = parse('/home/jmarnat/Documents/MAS/MAS/tmp_mas/scen01-100-SynchBB.log')
#
#for df in [df1,df2]:
#    time = df1['time'][0]
#    time = df1['agts'][0]
#    time = df1['mes'][0]
#    time = df1['bytes'][0]











