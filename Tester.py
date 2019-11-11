# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 12:38:54 2019

@author: Tobias's PC
"""

from Simplex import Simplex
from Functions import Functions
import random

p=[]
for i in range(0, 3):
    p.append(random.randrange(-1,2,2)*random.randrange(10000, 100000)/1000)
    
simp=Simplex(Functions.sumSquares, 3, p, 3)
print(simp.randRun(100, 0, .01))