# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 13:00:49 2020

@author: Sabine
"""

import matplotlib as pl
import os
 
precision_values=[]
recall_values=[]

for filename in os.listdir("/disk/scratch_big/sweber/GraphAlignment2/combinedTestResults/"):
    with open(filename, 'r') as inF:
        for line in inF:
            if "precision" in line:
                parts=line.split(" ")
                value=parts[1]
                precision_values.append(float(value))
            elif "recall" in line: 
                parts=line.split(" ")
                value=parts[1]
                recall_values.append(float(value))
                
pl.plot(precision_values, recall_values)
pl.show()
pl.savefig('prec_rec.png')