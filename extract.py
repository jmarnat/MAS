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


def save_nicely(node,filename):
    root = ET.ElementTree(node).getroot()
    md = minidom.parseString(ET.tostring(root))
    txt = md.toprettyxml(indent='\t')
    file_out = open(filename,'w')
    file_out.write(txt)
    file_out.close()

var = pd.read_csv("FullRLFAP/CELAR/scen01/var.txt", delim_whitespace=True, names=["id","domain"])
dom = pd.read_csv("FullRLFAP/CELAR/scen01/dom.txt", delim_whitespace=True, header=None)
ctr = pd.read_csv("FullRLFAP/CELAR/scen01/ctr.txt", delim_whitespace=True, header=None, names=["var1","var2","dc","op","cst"])

# removing dom[0] (the union of all the domains)
dom = dom[1:len(dom)]


instance = ET.Element("instance")
presentation = ET.SubElement(instance, "presentation", name="sampleProblem", maxConstraintArity="2", maximize="false", format="XCSP 2.1_FRODO")

#predicates = ET.SubElement(instance, "predicates", nbPredicates="1")
#predicate = ET.SubElement(predicates, "predicate", name="NEQ")
#parameters = ET.SubElement(predicate, "parameters").text = "int X1 int X2"
#expression = ET.SubElement(predicate, "expression")
#functional = ET.SubElement(expression, "functional").text = "ne(X1,X2)"


# =============================================================================
# AGENTS
# =============================================================================
# for now, 1 antenna = 1 agent = 1 variable

nbAgents = len(var)
agents = ET.SubElement(instance, "agents", nbAgents=str(nbAgents))
for row in var.values:
    num_antenna = row[0]
    ET.SubElement(agents, "agent", name='agt_'+str(num_antenna))

# =============================================================================
# DOMAINS
# =============================================================================
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


# =============================================================================
# VARIABLES
# =============================================================================
nbAgents = len(var)
variables = ET.SubElement(instance, "variables", nbVariables=str(nbAgents))
for row in var.values:
    num_antenna = row[0]
    num_domain = row[1]
    ET.SubElement(variables, "variable", name='ant_'+str(num_antenna), domain='dom_'+str(num_domain), agent='agt_'+str(num_antenna))

# =============================================================================
# PREDICATES
# =============================================================================
nbPredicates = 1
predicates = ET.SubElement(instance, "predicates", nbPredicates = str(nbPredicates))

# deviation : |ant_A - ant_B| < dev
pred_dev = ET.SubElement(predicates, "predicate", name="DEV")
params = ET.SubElement(pred_dev, "parameters")
params.text = "int A int B int C"
expression = ET.SubElement(pred_dev, "expression")
func = ET.SubElement(expression, "functional")
func.text = "lt(abs(sub(A,B)),C)"



# =============================================================================
# CONSTRAINTS
# =============================================================================
nbConstraints = len(ctr)
constraints = ET.SubElement(instance, "constraints", nbConstraints=str(nbConstraints))
for row in ctr.values:
    antA = str(row[0])
    antB = str(row[1])
    cst_type = row[3]
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
        parameters.text = 'ant_' + str(antA) + ' ant_' + str(antB)
    # elif cst_type == '=':
        # nothing for now





save_nicely(instance,'scen01.xml')























