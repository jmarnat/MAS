#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 16:01:13 2017

@author: koolok
"""

import pandas as pd
import xml.etree.cElementTree as ET
# https://stackoverflow.com/questions/3605680/creating-a-simple-xml-file-using-python
# https://docs.python.org/3.4/library/xml.etree.elementtree.html



var = pd.read_csv("FullRLFAP/CELAR/scen01/var.txt", delim_whitespace=True, names=["id","domain"])

dom = pd.read_csv("FullRLFAP/CELAR/scen01/dom.txt", delim_whitespace=True, header=None)

ctr = pd.read_csv("FullRLFAP/CELAR/scen01/ctr.txt", delim_whitespace=True, header=None, names=["var1","var2","dc","op","cst"])


instance = ET.Element("instance")
presentation = ET.SubElement(instance, "presentation", name="sampleProblem", maxConstraintArity="2", maximize="false", format="XCSP 2.1_FRODO")

predicates = ET.SubElement(instance, "predicates", nbPredicates="1")
predicate = ET.SubElement(predicates, "predicate", name="NEQ")
parameters = ET.SubElement(predicate, "parameters").text = "int X1 int X2"
expression = ET.SubElement(predicate, "expression")
functional = ET.SubElement(expression, "functional").text = "ne(X1,X2)"


tree = ET.ElementTree(instance)
tree.write("test.xml")

for row in csv.values :
    print(type(row[0]),type(row[1]))