#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 10:42:32 2020

@author: s1782911
"""

from test_dict import Test_dict
import parse_to_graph

def get_graphs_for_lambda(lambda_value,graphs_file_path):
    graph_dict={}
    graph=parse_to_graph.constructGraphFromFile("persLoc0150de.txt")
    graph_dict["person#location"]=graph
    return graph_dict

def test(sentence_to_relations_dict,data_set_file_path,lambda_value,graphs_file_path):
    test_dict=Test_dict(lambda_value)
    graph_dict=get_graphs_for_lambda(lambda_value,graphs_file_path)
    count=0
    #walk trough levy data set
    with open(data_set_file_path, 'r') as inF:
            for line in inF:
                line=line.rstrip()
                line=line.split(". ")
                if len(line)<3:
                    continue
                sent1=line[0].lower()
                #sent1=sent1[:-1]
                sent2=line[1].lower()
                sent2=sent2[:-1]
                judgement=line[2]
                #from relation dict get relation and type pairs for sent 1 and sent 2
                #print(sentence_to_relations_dict.keys())
                
                if sent1 not in sentence_to_relations_dict.keys():
                    count+=1
                    #print(sent1)
    #print(count)
                #relations_dict1=sentence_to_relations_dict[sent1]
                #relations_dict2=sentence_to_relations_dict[sent2]
                
                #print(relations_dict1, relations_dict2)
                
    #from graph_dict get graphs of type pairs
    #for all possible combinations of relations from the two sentences query the respective graphs
    return test_dict


if __name__ == '__main__':
    sentence_to_relation_dict=parse_to_graph.parse_rel_ex_output_to_sentence_relation_dict("Levy_relations.txt","deepLTranslationOfWholeDataset.txt")
    test_dict=test(sentence_to_relation_dict,"deepLTranslationOfWholeDataset.txt",0.015,"")