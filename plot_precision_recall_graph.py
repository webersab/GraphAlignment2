# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 13:00:49 2020

@author: Sabine
"""

import matplotlib.pyplot as pl
import os
 
fig, ax = pl.subplots()

precision_values1=[]
recall_values1=[]

for filename in os.listdir("/disk/scratch_big/sweber/GraphAlignment2/testResults/deMinimal/"):
    with open("/disk/scratch_big/sweber/GraphAlignment2/testResults/deMinimal/"+filename, 'r') as inF:
        for line in inF:
            if "precision" in line:
                parts=line.split(" ")
                value=parts[2]
                precision_values1.append(float(value))
            elif "recall" in line: 
                parts=line.split(" ")
                value=parts[2]
                recall_values1.append(float(value))
f1_1=[]
for prec,rec in zip(precision_values1,recall_values1):
    f1=(2*prec*rec)/(prec+rec)
    f1_1.append(f1)
    
print("de ",max(f1_1))

precision_values2=[]
recall_values2=[]

for filename in os.listdir("/disk/scratch_big/sweber/GraphAlignment2/testResults/multiMinimal/"):
    with open("/disk/scratch_big/sweber/GraphAlignment2/testResults/multiMinimal/"+filename, 'r') as inF:
        for line in inF:
            if "precision" in line:
                parts=line.split(" ")
                value=parts[2]
                precision_values2.append(float(value))
            elif "recall" in line: 
                parts=line.split(" ")
                value=parts[2]
                recall_values2.append(float(value))
                
f1_1=[]
for prec,rec in zip(precision_values2,recall_values2):
    f1=(2*prec*rec)/(prec+rec)
    f1_1.append(f1)
    
print("mult ",max(f1_1))

precision_values3=[]
recall_values3=[]

for filename in os.listdir("/disk/scratch_big/sweber/GraphAlignment2/testResults/transMinimal"):
    with open("/disk/scratch_big/sweber/GraphAlignment2/testResults/transMinimal/"+filename, 'r') as inF:
        for line in inF:
            if "precision" in line:
                parts=line.split(" ")
                value=parts[2]
                precision_values3.append(float(value))
            elif "recall" in line: 
                parts=line.split(" ")
                value=parts[2]
                recall_values3.append(float(value))
                
f1_1=[]
for prec,rec in zip(precision_values3,recall_values3):
    f1=(2*prec*rec)/(prec+rec)
    f1_1.append(f1)
    
print("tr ",max(f1_1))

pl.figure(figsize=(7,4))         
pl.plot(recall_values1, precision_values1, "ro", label='German')
pl.plot(recall_values3, precision_values3, "gs", label='Translated English')
pl.plot(recall_values2, precision_values2, "b*", label='Aligned')

pl.legend(loc='upper right')
pl.xlabel('recall')
pl.ylabel("precision")
pl.savefig('prec_recMinimal.pdf')
pl.show()


