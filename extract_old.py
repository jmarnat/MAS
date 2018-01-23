#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 16:01:13 2017

@author: koolok
"""

import pandas as pd
import numpy as np
import xml.etree.cElementTree as ET
from xml.dom import minidom
from os import chdir
# https://stackoverflow.com/questions/3605680/creating-a-simple-xml-file-using-python
# https://docs.python.org/3.4/library/xml.etree.elementtree.html




def save_tree(node,filename):
    root = ET.ElementTree(node).getroot()
    md = minidom.parseString(ET.tostring(root))
    txt = md.toprettyxml(indent='\t')
    file_out = open(filename,'w')
    file_out.write(txt)
    file_out.close()


def create_tree(path, domain_union=False, subset=10):
    var = pd.read_csv(path+"/var.txt", delim_whitespace=True, names=["id","domain"])
    dom = pd.read_csv(path+"/dom.txt", delim_whitespace=True, header=None)
    ctr = pd.read_csv(path+"/ctr.txt", delim_whitespace=True, names=["var1","var2","dc","op","dev","cst"])
    
    # removing dom[0] (the union of all the domains)
    if domain_union:
        dom = dom[1:len(dom)]
    
    
    instance = ET.Element("instance")
    
    ################
    # PRESENTATION #
    ################
    ET.SubElement(instance, "presentation", name="sampleProblem", maxConstraintArity="2", maximize="false", format="XCSP 2.1_FRODO")

    
    ##########
    # AGENTS #
    ##########
    # for now, 1 antenna = 1 agent = 1 variable
    
    nbAgents = len(var)
    agents = ET.SubElement(instance, "agents", nbAgents=str(nbAgents))
    num = 1
    nbAgents_real = 0
    for row in var.values:
        if (subset > 0) and (num > subset):
            print('agts break!')
            break
        num += 1
        nbAgents_real += 1
        num_antenna = row[0]
        ET.SubElement(agents, "agent", name='agt_'+str(num_antenna))
    if (subset > 0):
        agents.set('nbAgents',str(nbAgents_real))
    
    
    #############
    # VARIABLES #
    #############
    nbVariables = len(var)
    variables = ET.SubElement(instance, "variables", nbVariables=str(nbVariables))
    num = 1
    list_dom = np.zeros(len(dom))
    list_var = np.zeros(len(var))
    nbVariables_real = 0
    for row in var.values:
        if (subset > 0) and (num > subset):
            print('var break!')
            break
        num += 1
        num_antenna = row[0]
        num_domain = row[1]
        nbVariables_real += 1
        if (subset > 0): list_dom[num_domain] = 1
        if (subset > 0): list_var[num_antenna] = 1
        ET.SubElement(variables, "variable", name='ant_'+str(num_antenna), domain='dom_'+str(num_domain), agent='agt_'+str(num_antenna))
    if (subset > 0):
        variables.set('nbVariables',str(nbVariables_real))
        
    ###########
    # DOMAINS #
    ###########
    nbDomains = len(list_dom)
    domains = ET.SubElement(instance, "domains", nbDomains=str(nbDomains))
    nbDomains_real = 0
    for row in dom.values:
        num_domain = int(row[0])
        if (list_dom[num_domain] == 1):
            nbDomains_real += 1
            row = [x for x in row if str(x) != 'nan']
            nbValues = int(row[1])
            domain = ET.SubElement(domains, "domain", name="dom_"+str(num_domain), nbValues=str(nbValues))
            txt = ''
            for i in range(2,nbValues+2):
                txt += str(int(row[i]))
                if i <= (nbValues):
                    txt += ' '
            domain.text = txt
    if (subset > 0):
        domains.set('nbDomains',str(nbDomains_real))
        
        
    ##############
    # PREDICATES #
    ##############
    nbPredicates = 2
    predicates = ET.SubElement(instance, "predicates", nbPredicates = str(nbPredicates))
    
    # deviation : |ant_A - ant_B| > dev
    pred_dev = ET.SubElement(predicates, "predicate", name="DEV")
    params_dev = ET.SubElement(pred_dev, "parameters")
    params_dev.text = "int A int B int C"
    expr_dev = ET.SubElement(pred_dev, "expression")
    func_dev = ET.SubElement(expr_dev, "functional")
    func_dev.text = "gt(abs(sub(A,B)),C)"
    
    # or distance equal : |and_A - and_B| = 238
    pred_eq = ET.SubElement(predicates, "predicate", name="EQ")
    params_eq = ET.SubElement(pred_eq, "parameters")
    params_eq.text = "int A int B"
    expr_eq = ET.SubElement(pred_eq, "expression")
    func_eq = ET.SubElement(expr_eq, "functional")
    func_eq.text = "eq(abs(sub(A,B)),238)"
    
    
    
    ###############
    # CONSTRAINTS #
    ###############
    
    nbConstraints = len(ctr)
    nbConstraints_real = 0
    constraints = ET.SubElement(instance, "constraints", nbConstraints=str(nbConstraints))
    
    for row in ctr.values:
        antA = int(row[0])
        antB = int(row[1])
        
        if (subset < 1) or (list_var[antA] == 1 and list_var[antB] == 1):
            cst_type = row[3]
            dev = int(row[4])
            
            if cst_type == '>':
                nbConstraints_real += 1
                constraint = ET.SubElement(
                        constraints,
                        "constraint",
                        name = "cst_" + str(antA) + '_' + str(antB),
                        arity = "2",
                        scope = 'ant_' + str(antA) + ' ant_' + str(antB),
                        reference = "DEV"
                        )
                parameters = ET.SubElement(constraint, "parameters")
                parameters.text = 'ant_' + str(antA) + ' ant_' + str(antB) + ' ' + str(dev)
            elif cst_type == '=':
                nbConstraints_real += 1
                constraint = ET.SubElement(
                        constraints,
                        "constraint",
                        name = "cst_" + str(antA) + '_' + str(antB),
                        arity = "2",
                        scope = 'ant_' + str(antA) + ' ant_' + str(antB),
                        reference = "EQ"
                        )
                parameters = ET.SubElement(constraint, "parameters")
                parameters.text = 'ant_' + str(antA) + ' ant_' + str(antB)
    constraints.set('nbConstraints', str(nbConstraints_real))
    
    ##############
    # FINALLY... #
    ##############
    return instance



chdir('/home/jmarnat/Documents/MAS/MAS')


"""
##########################################
# run for extracting all the celar DCOPs #
##########################################
for i in range(1,12):
    pname = 'scen'+str(i).rjust(2,'0')
    tree = create_tree(path = './FullRLFAP/CELAR/'+pname, domain_union=False)
    save_tree(tree, 'frodo2/celar-'+pname+'.xml')
"""

#########################################
# extracting a sub-problem from a scene #
#########################################
# sub scen01
tree = create_tree(path = './FullRLFAP/CELAR/scen01/', domain_union=False, subset=20)
save_tree(tree, 'frodo2/celar-scen01-sub-20.xml')


