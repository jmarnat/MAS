#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 16:36:28 2018

@author: jmarnat
"""



# test for 100 agts with AFB and SynchBB
# test for  10 agts with all
from extract import create_tree, save_tree
from logparser import parse
from os import path, makedirs, chdir, system
import pandas as pd

agt_name = {}
agt_name['ADOPT'] = 'ADOPTagentJaCoP.xml'
agt_name['AFB'] = 'AFBagentJaCoP.xml'
agt_name['DPOP'] = 'DPOPagentJaCoP.xml'
agt_name['DSA'] = 'DSAagentJaCoP.xml'
agt_name['MaxSum'] = 'MaxSumAgentJaCoP.xml'
#agt_name['MaxSumPtd'] = 'MaxSumAgentPerturbedJaCoP.xml'
#agt_name['MGM2'] = 'MGM2agentJaCoP.xml'
agt_name['MGM'] = 'MGMagentJaCoP.xml'
#agt_name['MPC'] = 'MPC-DisCSP4_JaCoP.xml'
#agt_name['MPCW'] = 'MPC-DisWCSP4_JaCoP.xml'
agt_name['SynchBB'] = 'SynchBBagentJaCoP.xml'


DEBUG = False

def tree_path(path_tmp, scene, subset):
#    return path_tmp+'/scen'+str(scene).zfill(2)+'-'+str(subset)+'.xml'
    return path_tmp+'run-tmp.xml'

def log_path(path_tmp, scene, subset, agent):
#    return path_tmp+'/scen'+str(scene).zfill(2)+'-'+str(subset)+'-'+str(agent)+'.log'
    return path_tmp+'run-tmp.log'

def cmd(path_tmp, scene, agent, subset):
    path_frodo = 'frodo2/frodo2.jar'
    agt_fty = 'frodo2.algorithms.AgentFactory'
    path_pb = tree_path(path_tmp, scene, subset)
    path_agent = 'frodo2/agents/'+agent+'/'+agt_name[agent]
    path_log = log_path(path_tmp, scene, subset, agent)
    
    command = 'java -cp '+path_frodo+' '+agt_fty+' '+path_pb+' '+path_agent+' > '+path_log
    if (DEBUG): print(command)
    system(command)
    # java -cp frodo2/frodo2.jar frodo2.algorithms.AgentFactory tmp_mas/scen01-100-AFB.xmlrodo2/agents/AFB/AFBagentJaCoP.xml

    
    
chdir('/home/jmarnat/Documents/MAS/MAS')
path_tmp = './tmp_mas/'

if not path.exists(path_tmp):
    makedirs(path_tmp)

big_df_cols = ['sub','agent','time','agts','mes','mean_mes','bytes','mean_bytes']
big_df = pd.DataFrame(columns=big_df_cols)

#sub = 10
#agt_start = 0
for sub in [3,5,7,9,11,13,15]:
    print('sub = '+str(sub))
    for scene in range(1,2):
        ''' generating the xml tree of the problem '''
        print('- scene '+str(scene))
        tree = create_tree(scen = scene, domain_union=False, subset=sub, optimize_agents=True)
        save_tree(tree, tree_path(path_tmp, scene, sub))
        
        # for agent in ['AFB','SynchBB']:
#        iagt = 0
        for agent in agt_name.keys():
#            iagt += 1
#            if iagt >= agt_start :
            print('\t- agent : '+agent)
            
    
            ''' running the problem '''
            # print('\t\t- running DCOP')
            cmd(path_tmp, scene, agent, sub)
            
            ''' parsing the result '''
            # print('\t\t- parsing the result')
            df = parse(log_path(path_tmp, scene, sub, agent), debug = False)
            time = df['time'][0]
            nagts = df['agts'][0]
            nmes = df['mes'][0]
            nbytes = df['bytes'][0]
            nrow = [sub, agent, time, nagts, nmes, int(nmes/nagts), nbytes, int(nbytes/nagts)]
            big_df.loc[big_df.shape[0]] = nrow
   

''' writing the overall results '''
print('\n- writing all the results...')
big_df.to_csv('all-sub-incremental-3-15.csv')

print('\nall done.')