#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 10:42:32 2020

@author: s1782911
"""

from test_dict import Test_dict
import parse_to_graph
import pickle
import networkx as nx
import re
import os
import sys


def get_graphs_for_lambda(lambda_value,graphs_file_path):
    graph_dict={}
    home_path="/disk/scratch_big/sweber/GraphAlignment2/justGraphs/"
    
    for filename in os.listdir(graphs_file_path):
        graph=parse_to_graph.constructGraphFromFile(home_path+filename,lambda_value)
        parse_to_graph.get_the_stats(graph)
        graph_dict[filename.lower()]=graph
        parts=filename.lower().split("#")
        graph_dict[parts[1]+"#"+parts[0]]=graph
        if (parts[1]+"#"+parts[0])=="thing#thing":
            graph_dict["noType"]=graph
    return graph_dict

def verb_negated(relation,candidate_verb):
    result = re.search('(.*)'+relation, candidate_verb)
    if result!=None:
        string_before=result.group(1)
        try:
            if "NEG" in string_before[-5:]:
                return True
        except:
            print(relation,candidate_verb)
            return False
    return False

def find_entailment(graph, relation_tuple):
    both_in_graph=False
    rel1=relation_tuple[0]
    rel2=relation_tuple[1]
    rel1_nodes=[]
    rel2_nodes=[]
    for n in graph.nodes:
        if rel1 in graph.nodes[n]["verb"] and not verb_negated(rel1,graph.nodes[n]["verb"]):
            rel1_nodes.append(n)
        if rel2 in graph.nodes[n]["verb"] and not verb_negated(rel2,graph.nodes[n]["verb"]):
            rel2_nodes.append(n)
    #check: are relations in same graph?
    if len(rel1_nodes)>0 and len(rel2_nodes)>0:
        both_in_graph=True
    else: 
        return both_in_graph,"n"
    #are they in same cluster? 
    overlap = [value for value in rel1_nodes if value in rel2_nodes] 
    if len(overlap)>0:
        return both_in_graph,"y"
    #is rel2 ancestor of rel1?
    for node in rel2_nodes:
        ancestors=nx.ancestors(graph,node)
        for n in rel1_nodes:
            if n in ancestors:
                return both_in_graph,"y"
    return both_in_graph,"n"    

def test(sentence_to_relations_dict,lambda_value,graphs_file_path):
    #test_dict=Test_dict(lambda_value)
    graph_dict=get_graphs_for_lambda(lambda_value,graphs_file_path)
    total=0
    tp=0
    tn=0
    fp=0
    fn=0

    for sentence in sentence_to_relations_dict:
        #print(sentence)
        relation_dict=sentence_to_relations_dict[sentence]
        judgement=relation_dict["judgement"]
        #get set of type pairs, list of relations
        types_set=set()
        relations_list1=[]
        relations_list2=[]
        for relation in relation_dict["rel1"]:
            types_set.add(relation[1])
            relations_list1.append(relation[0])
        for relation in relation_dict["rel2"]:
            types_set.add(relation[1])
            relations_list2.append(relation[0])
            
        #for each of the type pairs get a graph
        candidate_graphs=set()
        for type_pair in types_set:
            try:
                candidate_graphs.add(graph_dict[type_pair])
            except KeyError:
                candidate_graphs.add(graph_dict["thing#thing"])
                continue
    
        #get all combinations of relations
        our_judgement_set=set()
        both_in_graph_set=set()
        if "noRelation" in relations_list1:
            relations_list1.remove("noRelation")
        if "noRelation" in relations_list2:
            relations_list2.remove("noRelation")
        all_possible_combinations_of_relations= [(x,y) for x in relations_list1 for y in relations_list2]
        for graph in candidate_graphs:
            for relation_tuple in all_possible_combinations_of_relations:
                both_in_graph,our_judgement=find_entailment(graph, relation_tuple)
                our_judgement_set.add(our_judgement)
                both_in_graph_set.add(both_in_graph)
        #if none of the candidates in same graph, check all the other graphs too
        if True not in both_in_graph_set:
            for type_pair,graph in graph_dict.items():
                for relation_tuple in all_possible_combinations_of_relations:
                    both_in_graph,our_judgement=find_entailment(graph, relation_tuple)
        #compare our judgement with annotation
        total+=1
        if judgement=="y":
            if "y" in our_judgement_set:
                tp+=1
            else:
                fn+=1
        else:
            if "y" in our_judgement_set:
                fp+=1
            else:
                tn+=1
        
    #fill test_dict object with stats
    #print("tp ",tp, " tn ",tn," fn ",fn," fp ", fp)
    if tp+tn+fn+fp!=total:
        print("somehting went wrong with the counting")
    with open(str(lambda_value)+'.txt', 'w') as f:
        f.write(str(lambda_value))
        f.write("\n tp "+str(tp)+" tn "+str(tn)+" fn "+str(fn)+" fp "+str(fp))
        f.write("\n precision: "+str(tp/(tp+fp)))
        f.write("\n recall: "+str(tp/(tp+fn)))
    f.close()
    #return test_dict


if __name__ == '__main__':
    #parallel -j35 python test.py ::: 0.15 0.25 0.34 0.44 0.55 0.64 0.75 0.85 0.12 0.22 0.32 0.42 0.52 0.62 0.72 0.82 0.17 0.27 0.37 0.47 0.57 0.67 0.77 0.87 0.99
    #lam=sys.argv[1]
    sentence_to_relation_dict = pickle.load( open( "relation_dict2.pickle", "rb" ) )
    test_dict=test(sentence_to_relation_dict,0.34,"/disk/scratch_big/sweber/GraphAlignment2/justGraphs")