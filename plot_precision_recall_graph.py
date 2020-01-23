# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 13:00:49 2020

@author: Sabine
"""

import matplotlib.pyplot as pl
import os
 
precision_values=[]
recall_values=[]

for filename in os.listdir("/disk/scratch_big/sweber/GraphAlignment2/combinedTestResults/"):
    with open("/disk/scratch_big/sweber/GraphAlignment2/combinedTestResults/"+filename, 'r') as inF:
        for line in inF:
            if "precision" in line:
                parts=line.split(" ")
                value=parts[2]
                precision_values.append(float(value))
            elif "recall" in line: 
                parts=line.split(" ")
                value=parts[2]
                recall_values.append(float(value))
                
pl.plot(recall_values, precision_values, "ro")
pl.show()
pl.savefig('prec_recDE.png')
