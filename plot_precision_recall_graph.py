# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 13:00:49 2020

@author: Sabine
"""

import matplotlib.pyplot as pl
import os
 
precision_values1=[]
recall_values1=[]

for filename in os.listdir("/disk/scratch_big/sweber/GraphAlignment2/testResults/DeMitSein/"):
    with open("/disk/scratch_big/sweber/GraphAlignment2/testResults/DeMitSein/"+filename, 'r') as inF:
        for line in inF:
            if "precision" in line:
                parts=line.split(" ")
                value=parts[2]
                precision_values1.append(float(value))
            elif "recall" in line: 
                parts=line.split(" ")
                value=parts[2]
                recall_values1.append(float(value))

precision_values2=[]
recall_values2=[]

for filename in os.listdir("/disk/scratch_big/sweber/GraphAlignment2/testResults/MultiMitSein/"):
    with open("/disk/scratch_big/sweber/GraphAlignment2/testResults/MultiMitSein/"+filename, 'r') as inF:
        for line in inF:
            if "precision" in line:
                parts=line.split(" ")
                value=parts[2]
                precision_values2.append(float(value))
            elif "recall" in line: 
                parts=line.split(" ")
                value=parts[2]
                recall_values2.append(float(value))

precision_values3=[]
recall_values3=[]

for filename in os.listdir("/disk/scratch_big/sweber/GraphAlignment2/testResults/translatedEnDe/"):
    with open("/disk/scratch_big/sweber/GraphAlignment2/testResults/translatedEnDe/"+filename, 'r') as inF:
        for line in inF:
            if "precision" in line:
                parts=line.split(" ")
                value=parts[2]
                precision_values3.append(float(value))
            elif "recall" in line: 
                parts=line.split(" ")
                value=parts[2]
                recall_values3.append(float(value))


               
pl.plot(recall_values1, precision_values1, "ro")
pl.plot(recall_values2, precision_values2, "bv")
pl.plot(recall_values3, precision_values3, "gs")
pl.savefig('prec_recDeMul.png')
#pl.show()


