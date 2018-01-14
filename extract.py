#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 16:01:13 2017

@author: koolok
"""

import pandas as pd
import xml.etree.cElementTree as ET
from xml.dom import minidom
# https://stackoverflow.com/questions/3605680/creating-a-simple-xml-file-using-python
# https://docs.python.org/3.4/library/xml.etree.elementtree.html


def save_tree(node,filename):
    root = ET.ElementTree(node).getroot()
    md = minidom.parseString(ET.tostring(root))
    txt = md.toprettyxml(indent='\t')
    file_out = open(filename,'w')
    file_out.write(txt)
    file_out.close()


def create_tree(path, domain_union=False):
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
    for row in var.values:
        num_antenna = row[0]
        ET.SubElement(agents, "agent", name='agt_'+str(num_antenna))
    
    ###########
    # DOMAINS #
    ###########
    nbDomains = len(dom)
    domains = ET.SubElement(instance, "domains", nbDomains=str(nbDomains))
    for row in dom.values:
        num_domain = int(row[0])
        row = [x for x in row if str(x) != 'nan']
        nbValues = int(row[1])
        domain = ET.SubElement(domains, "domain", name="dom_"+str(num_domain), nbValues=str(nbValues))
        txt = ''
        for i in range(2,nbValues+2):
            txt += str(int(row[i]))
            if i <= (nbValues):
                txt += ' '
        domain.text = txt
    
    
    #############
    # VARIABLES #
    #############
    nbAgents = len(var)
    variables = ET.SubElement(instance, "variables", nbVariables=str(nbAgents))
    for row in var.values:
        num_antenna = row[0]
        num_domain = row[1]
        ET.SubElement(variables, "variable", name='ant_'+str(num_antenna), domain='dom_'+str(num_domain), agent='agt_'+str(num_antenna))
    
    ##############
    # PREDICATES #
    ##############
    nbPredicates = 1
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
    constraints = ET.SubElement(instance, "constraints", nbConstraints=str(nbConstraints))
#    print('ctr = ')
    for row in ctr.values:
#        print('yop')
        antA = str(int(row[0]))
        antB = str(int(row[1]))
        cst_type = row[3]
        dev = int(row[4])

        if cst_type == '>':
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
    
    ##############
    # FINALLY... #
    ##############
    return instance



tree = create_tree(path = './FullRLFAP/SUBCELAR6/CELAR6-SUB0', domain_union=False)
save_tree(tree, 'subcelar-6-0.xml')




