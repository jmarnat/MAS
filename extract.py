#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 16:01:13 2017

@author: koolok
"""

import pandas as pd
from lxml import etree

var = pd.read_csv("FullRLFAP/CELAR/scen01/var.txt", delim_whitespace=True, names=["id","domain"])

dom = pd.read_csv("FullRLFAP/CELAR/scen01/dom.txt", delim_whitespace=True, header=None)

ctr = pd.read_csv("FullRLFAP/CELAR/scen01/ctr.txt", delim_whitespace=True, header=None, names=["var1","var2","dc","op","cst"])


for row in csv.values :
    print(type(row[0]),type(row[1]))