#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 14:21:50 2020

@author: s1782911
"""
import parse_to_graph
import test1 
import matplotlib.pyplot as pl
import os
import pickle

def test(lambda_list, path, positives, negatives):
    return_list=[]
    for l in lambda_list:
        tp=0
        fp=0
        tn=0
        fn=0
        print(l)
        G=parse_to_graph.constructGraphFromFile(path,l)
        #print("pos")
        for tup in  positives:
            try:
                res=test1.find_entailment(G, tup)
                #print(res)
                if res[1]=='y':
                    #print(tup,res)
                    tp+=1
                else:
                    fn+=1
            except AttributeError:
                print("no ", l)
                break
        #print("neg")
        for tup in negatives:
            try:
                res=test1.find_entailment(G, tup)
                #print(res)
                if res[1]=='n':
                    tn+=1
                else:
                    fp+=1
            except  AttributeError:
                print("no ", l)
                break
        print("tp: ",tp," tn: ",tn," fp: ",fp," fn: ",fn)
        if tp!=0:
            prec=tp/(tp+fp)
            print("precision :", tp/(tp+fp))
            rec=tp/(tp+fn)
            print("recall :", tp/(tp+fn))
        else:
            prec=1
            rec=0
        return_list.append((prec,rec))
    return return_list

def parse(input_path):
    positives=[]
    negatives=[]
    f=open(input_path,"r")
    one=False
    two=False
    for line in f:
        print(line)
        if "positive" in line:
            one=True
            continue
        if one and line!="\n":
            line=line.split("),(")
            a=line[1].replace("(","").replace(")","")
            b=line[0].replace("(","").replace(")","")
            positives.append((a,b))
        if line=="\n":
            one=False
        if "negative" in line:
            two=True
            continue
        if two:
            line=line.split("),(")
            a=line[1].replace("(","").replace(")","")
            b=line[0].replace("(","").replace(")","")
            negatives.append((a,b))
    return positives, negatives

def test_multi(lambda_list,file_path, type_pair, positives, negatives):
    return_list=[]
    for l in lambda_list:
        print("----------------------"+str(l)+"------------------------------")
        tp=0
        fp=0
        tn=0
        fn=0
        for filename in os.listdir(file_path):
            if type_pair in filename and str(l)+".pickle" in filename:
                #print(file_path+filename)
                G=pickle.load(open(file_path+filename,"rb"))
                #print(G[0])
                print("number of edges", G.number_of_edges())
                for tup in  positives:
                    try:
                        res=test1.find_entailment(G, tup)
                        #print(tup,res)
                        if res[1]=='y':
                            print(tup,res)
                            tp+=1
                        else:
                            fn+=1
                    except AttributeError:
                        print("no ", l)
                        break
                for tup in negatives:
                    try:
                        res=test1.find_entailment(G, tup)
                        #print(tup,res)
                        if res[1]=='n':
                            tn+=1
                        else:
                            fp+=1
                    except  AttributeError:
                        #print("no ", l)
                        break
                print("tp: ",tp," tn: ",tn," fp: ",fp," fn: ",fn)
                if tp!=0:
                    prec=tp/(tp+fp)
                    print("precision :", tp/(tp+fp))
                    rec=tp/(tp+fn)
                    print("recall :", tp/(tp+fn))
                else:
                    prec=1
                    rec=0
                return_list.append((prec,rec))
    return return_list

if __name__ == '__main__':
    """
    lambda_list=[ 0.004, 0.008, 0.012, 0.016, 0.020, 0.024, 0.028, 0.032, 0.036,
             0.040, 0.044, 0.048, 0.052, 0.056, 0.060, 0.064, 0.068, 0.072, 
             0.076, 0.080, 0.084, 0.088, 0.092]
    for l in lambda_list:
        G=parse_to_graph.constructGraphFromFile_multi("person#person_gsim_HTLFRG",l,0)
        pickle.dump(G[0], open("/disk/scratch_big/sweber/GraphAlignment2/mergedGlobalGraphPickles/person#person"+str(l)+".pickle", "wb" ) )
        print("done ",l)
    
    
    G=pickle.load(open("mergedGraphPickles/person#person/merged_graphPerson#Person0.0099.pickle","rb"))
    for n in G.nodes():
        print(n)
        print(G.nodes[n]["verb"])
    
    #parse the test set
    positives,negatives=parse("/disk/scratch_big/sweber/manual_german_graph_test/person#person")       
    # for all the different graphs of that type
    lambda_list=[0.0149, 0.025, 0.035, 0.045, 0.054, 0.064, 0.075, 0.085, 0.0125, 0.0225, 
                 0.0324, 0.0425, 0.0524, 0.0625, 0.0724, 0.0825, 0.0175, 0.0274, 0.0375, 
                 0.0474, 0.0575, 0.0675, 0.0775, 0.0874]
    
    return_list_low=test(lambda_list,"justGraphsLowL/PERSON#PERSON", positives, negatives)
        
    lambda_list=[0.15,  0.25,  0.34, 0.44, 0.55, 0.64, 0.75,  0.85, 0.125,  0.224,
                 0.324, 0.425, 0.524, 0.625,  0.725, 0.824, 0.174, 0.275, 0.375, 
                 0.474, 0.574, 0.675, 0.774, 0.875
                 ]
    
    return_list_high=test(lambda_list,"justGraphsHighL/PERSON#PERSON", positives, negatives)
    return_list_low.extend(return_list_high)
    rec_list=[]
    prec_list=[]
    for t in return_list_low:
        prec_list.append(t[0])
        rec_list.append(t[1])
    pl.plot(rec_list, prec_list, "ro", label='German')
    """ 
    positives, negatives=parse("person#person_EN")
    lambda_list=[0.0125,  0.0375,  0.0675,  0.12,  0.27,  0.44,  0.62,  0.0175,  0.0425,  
                 0.075,   0.15,  0.32,  0.47,  0.64,  0.85, 0.0225,  0.045,   0.0775,  0.17,  
                 0.34,  0.52,  0.67,  0.87, 0.025,   0.0575,  0.0825,  0.22,  0.37,  0.55,  
                 0.75, 0.035,   0.0625,  0.085,   0.25,  0.42,  0.57,  0.77]
    
    return_list1=test_multi(lambda_list,"newAligned/", "PERSON#PERSON", positives, negatives)
    
    rec_list1=[]
    prec_list1=[]
    for t in return_list1:
        prec_list1.append(t[0])
        rec_list1.append(t[1])
    pl.plot(rec_list1, prec_list1, "bv", label='MultiAll') 
    
    lambda_list=[0.0125,  0.0375,  0.0675,  0.12,  0.27,  0.44,  0.62,  0.0175,  0.0425,  
                 0.075,   0.15,  0.32,  0.47,  0.64,  0.85, 0.0225,  0.045,   0.0775,  0.17,  
                 0.34,  0.52,  0.67,  0.87, 0.025,   0.0575,  0.0825,  0.22,  0.37,  0.55,  
                 0.75, 0.035,   0.0625,  0.085,   0.25,  0.42,  0.57,  0.77]
    
    return_list2=test_multi(lambda_list,"newAlignedHighest/", "PERSON#PERSON", positives, negatives)
    
    rec_list2=[]
    prec_list2=[]
    for t in return_list2:
        prec_list2.append(t[0])
        rec_list2.append(t[1])
    pl.plot(rec_list2, prec_list2, "ro", label='MultiHigh')

    
    lambda_list=[ 0.004, 0.008, 0.012, 0.016, 0.020, 0.024, 0.028, 0.032, 0.036,
                 0.040, 0.044, 0.048, 0.052, 0.056, 0.060, 0.064, 0.068, 0.072, 
                 0.076, 0.080, 0.084, 0.088, 0.092]
    
    return_list=test_multi(lambda_list,"mergedGlobalGraphPickles/", "person#person", positives, negatives)
    
    rec_list3=[]
    prec_list3=[]
    for t in return_list:
        prec_list3.append(t[0])
        rec_list3.append(t[1])
    pl.plot(rec_list3, prec_list3, "g*", label='English')
    
    pl.legend(loc='upper right')
    pl.xlabel('recall')
    pl.ylabel("precision")
    pl.savefig('prec_recMinimal.pdf')
    pl.show()
    #positives_en, negatives_en=parse("/disk/scratch_big/sweber/manual_german_graph_test/person#person_en")
                                 
                                 