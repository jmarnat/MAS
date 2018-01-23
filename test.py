#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 19:40:16 2018

@author: jmarnat
"""
#import numpy as np




def get_agt(d, ant):
    for agt, ants in d.items():
        if ant in ants:
            return agt
    return -1

def dadd(d, i, value):
    if d.get(i):
        d[i].append(value)
    else:
        d[i] = [value]

def drem(d, i, value):
    d[i].remove(value)

###########
# TESTING #
###########
'''
d = {}

# [1,2]
dadd(d,1,1)
dadd(d,2,2)

# [1,3]
dadd(d,2,3)

# [1,4]
dadd(d,2,4)

# [2,3]
drem(d,2,3)
dadd(d,3,3)

# [2,4]
drem(d,2,4)
dadd(d,3,4)

# [3,4]
drem(d,3,4)
dadd(d,4,4)


# [5,6]
dadd(d,1,5)
dadd(d,2,6)

print(str(d))
print(str(len(d)))



# what we want is : d=[[1,5],[2,6],[3],[4]]
'''



####################
# NOW THE TRUE ONE #
####################
ctrs = [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4],[5,6]]

d = {}
for ctr in ctrs:
def update_d(d,ctr):
    antA = ctr[0]
    antB = ctr[1]
    
    agtA = get_agt(d, antA)
    agtB = get_agt(d, antB)
    
    if agtA < 0 and agtB < 0:
        dadd(d,1,antA)
        dadd(d,2,antB)
    elif agtA > 0:
        if (agtA == agtB):
            drem(d,agtA,antB)
            dadd(d,agtA+1,antB)
        else:
            for i in range(1,len(d)+1):
                if (i != agtA):
                    dadd(d,i,antB)
#    return d

                
        