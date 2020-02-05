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
    
    for filename in os.listdir(graphs_file_path):
        graph=parse_to_graph.constructGraphFromFile(graphs_file_path+filename,lambda_value)
        graph_dict[filename.lower()]=graph
        parts=filename.lower().split("#")
        graph_dict[parts[1]+"#"+parts[0]]=graph
        if (parts[1]+"#"+parts[0])=="thing#thing":
            graph_dict["noType"]=graph
    return graph_dict

def get_graphs_for_lambda_translated(lambda_value,graphs_file_path):
    graph_dict={}
    for filename in os.listdir(graphs_file_path):
        if str(lambda_value) in filename:
            graph=pickle.load( open( graphs_file_path+filename, "rb" ) )
            filename=filename[12:]
            if len(str(lambda_value))==6:
                type_pair=filename.lower()[:-13]
            elif len(str(lambda_value))==5:
                type_pair=filename.lower()[:-12]
            elif len(str(lambda_value))==4:
                type_pair=filename.lower()[:-11]
            elif len(str(lambda_value))==3:
                type_pair=filename.lower()[:-10]
            if "misc" in type_pair:
                type_pair=type_pair.replace("misc","thing")
            graph_dict[type_pair]=graph
            parts=type_pair.split("#")
            graph_dict[parts[1]+"#"+parts[0]]=graph
            if (parts[1]+"#"+parts[0])=="thing#thing":
                graph_dict["noType"]=graph
    return graph_dict

def get_graphs_for_lambda_multi(lambda_value,graphs_file_path):
    graph_dict={}
    for filename in os.listdir(graphs_file_path):
        if str(lambda_value) in filename:
            graph=pickle.load( open( graphs_file_path+filename, "rb" ) )
            if len(str(lambda_value))==6:
                type_pair=filename.lower()[:-13]
            elif len(str(lambda_value))==5:
                type_pair=filename.lower()[:-12]
            elif len(str(lambda_value))==4:
                type_pair=filename.lower()[:-11]
            graph_dict[type_pair]=graph
            parts=type_pair.split("#")
            graph_dict[parts[1]+"#"+parts[0]]=graph
            if (parts[1]+"#"+parts[0])=="thing#thing":
                graph_dict["noType"]=graph
    return graph_dict

def get_graphs_for_lambda_trans_comb(lambda_value,graphs_file_path):
    graph_dict={}
    for filename in os.listdir(graphs_file_path):
        if str(lambda_value) in filename:
            graph=pickle.load( open( graphs_file_path+filename, "rb" ) )
            if len(str(lambda_value))==6:
                type_pair=filename.lower()[:-13]
            elif len(str(lambda_value))==5:
                type_pair=filename.lower()[:-12]
            elif len(str(lambda_value))==4:
                type_pair=filename.lower()[:-11]
            if "misc" in type_pair:
                type_pair=type_pair.replace("misc","thing")
            graph_dict[type_pair]=graph
            parts=type_pair.split("#")
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

def analyze_errors(graph, relation_tuple):
    both_in_graph=False
    rel1=relation_tuple[0]
    rel2=relation_tuple[1]
    rel1_nodes=[]
    rel2_nodes=[]
    for n in graph.nodes:
        try:
            if rel1 in graph.nodes[n]["verb"] and not verb_negated(rel1,graph.nodes[n]["verb"]):
                rel1_nodes.append(n)
            if rel2 in graph.nodes[n]["verb"] and not verb_negated(rel2,graph.nodes[n]["verb"]):
                rel2_nodes.append(n)
        except KeyError:
            continue
    #check: are relations in same graph?
    if len(rel1_nodes)>0 and len(rel2_nodes)>0:
        both_in_graph=True
    else: 
        return both_in_graph,"n"
    #are they in same cluster? 
    overlap = [value for value in rel1_nodes if value in rel2_nodes] 
    if len(overlap)>0:
        print("in same node")
        for m in overlap:
            print(graph.nodes[m])
        return both_in_graph,"y"
    #is rel2 ancestor of rel1?
    for node in rel2_nodes:
        ancestors=nx.ancestors(graph,node)
        descendants=nx.descendants(graph,node)
        for n in rel1_nodes:
            if n in ancestors:
                print("in ancestors")
                print(graph.nodes[n])
                return both_in_graph,"y"
            elif n in descendants:
                print("in descendants")
                print(graph.nodes[n])
    if both_in_graph:
        print("in graph, but no overlap or ancestors")
        print(rel1)
        for k in rel1_nodes:
            connected_component=nx.node_connected_component(graph.to_undirected(), k)
            for j in rel2_nodes:
                if j in connected_component:
                    print("in conn comp")
                    print(len(connected_component))
                    print("shortest path",nx.shortest_path_length(graph.to_undirected(),source=k,target=j))
                    return both_in_graph, "n"
    return both_in_graph,"n"    
    

def find_entailment(graph, relation_tuple):
    both_in_graph=False
    rel1=relation_tuple[0]
    rel2=relation_tuple[1]
    rel1_nodes=[]
    rel2_nodes=[]
    for n in graph.nodes:
        try:
            if rel1 in graph.nodes[n]["verb"] and not verb_negated(rel1,graph.nodes[n]["verb"]):
                rel1_nodes.append(n)
            if rel2 in graph.nodes[n]["verb"] and not verb_negated(rel2,graph.nodes[n]["verb"]):
                rel2_nodes.append(n)
        except KeyError:
            continue
    #check: are relations in same graph?
    if len(rel1_nodes)>0 and len(rel2_nodes)>0:
        both_in_graph=True
    #else: 
        #return both_in_graph,"n"
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
    #stupid hack to see if my overlapping is too strict. I know this is terrible
    for n in graph.nodes:
        if "_" in rel1:
            rel1=rel1.split("_")
            rel1=rel1[0]
        else:
            rel1=rel1.split(".")
            rel1=rel1[0]
        if "_" in rel2:
            rel2=rel2.split("_")
            rel2=rel2[0]
        else:
            rel2=rel2.split(".")
            rel2=rel2[0]
        try:
            if rel1 in graph.nodes[n]["verb"] and not verb_negated(rel1,graph.nodes[n]["verb"]):
                rel1_nodes.append(n)
            if rel2 in graph.nodes[n]["verb"] and not verb_negated(rel2,graph.nodes[n]["verb"]):
                rel2_nodes.append(n)
        except KeyError:
            continue
    #check: are relations in same graph?
    if len(rel1_nodes)>0 and len(rel2_nodes)>0:
        both_in_graph=True
    else: 
        return both_in_graph,"n"
    
    #hacky solutiion for too many things with "be"
    #if "sein" in rel1 or "sein" in rel2:
        #return both_in_graph, "n"
    
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

def debug_test(sentence_to_relations_dict,lambda_value,graphs_file_path_de, graphs_file_path_multi, language_flag):
    #test_dict=Test_dict(lambda_value)

    graph_dict_de=get_graphs_for_lambda(lambda_value,graphs_file_path_de)
    graph_dict_multi=get_graphs_for_lambda_multi(lambda_value,graphs_file_path_multi)
    if graph_dict_de=={} or graph_dict_multi=={}:
        print("something is wrong dict building")
        
    total=0
    tp=0
    tn=0
    fp=0
    fn=0

    for sentence in sentence_to_relations_dict:
        relation_dict=sentence_to_relations_dict[sentence]
        judgement=relation_dict["judgement"]
        #print(judgement)
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
        candidate_graphs_de=set()
        candidate_graphs_multi=set()
        for type_pair in types_set:
            try:
                candidate_graphs_de.add(graph_dict_de[type_pair])
                candidate_graphs_multi.add(graph_dict_multi[type_pair])
            except KeyError:
                candidate_graphs_de.add(graph_dict_de["thing#thing"])
                candidate_graphs_multi.add(graph_dict_multi["thing#thing"])
                continue
    
        #get all combinations of relations
        our_judgement_set=set()
        both_in_graph_set=set()
        if "noRelation" in relations_list1:
            relations_list1.remove("noRelation")
        if "noRelation" in relations_list2:
            relations_list2.remove("noRelation")
        all_possible_combinations_of_relations= [(x,y) for x in relations_list1 for y in relations_list2]
        for graph in candidate_graphs_de:
            for relation_tuple in all_possible_combinations_of_relations:
                both_in_graph,our_judgement=find_entailment(graph, relation_tuple)
                our_judgement_set.add(our_judgement)
                both_in_graph_set.add(both_in_graph)
        #if none of the candidates in same graph, check all the other graphs too
        if True not in both_in_graph_set:
            for type_pair,graph in graph_dict_de.items():
                for relation_tuple in all_possible_combinations_of_relations:
                    both_in_graph,our_judgement=find_entailment(graph, relation_tuple)
        #compare our judgement with annotation
           
        total+=1
        if judgement=="y":
            if "y" in our_judgement_set:
                tp+=1
                #print("-----------------True positive-----------------")
                #print(sentence, relations_list1, relations_list2)
            else:
                print("------False negative, DE---------------")
                print(sentence, judgement, our_judgement_set)
                print(relations_list1, relations_list2)
                for graph in candidate_graphs_de:
                    print(nx.density(graph))
                    print(analyze_errors(graph, relation_tuple))
                fn+=1
        else:
            if "y" in our_judgement_set:
                fp+=1
            else:
                tn+=1
    
        for graph in candidate_graphs_multi:
            for relation_tuple in all_possible_combinations_of_relations:
                both_in_graph,our_judgement=find_entailment(graph, relation_tuple)
                our_judgement_set.add(our_judgement)
                both_in_graph_set.add(both_in_graph)
        #if none of the candidates in same graph, check all the other graphs too
        if True not in both_in_graph_set:
            for type_pair,graph in graph_dict_multi.items():
                for relation_tuple in all_possible_combinations_of_relations:
                    both_in_graph,our_judgement=find_entailment(graph, relation_tuple)
        #compare our judgement with annotation
           
        total+=1
        if judgement=="y":
            if "y" in our_judgement_set:
                tp+=1
                #print("-----------------True positive-----------------")
                #print(sentence, relations_list1, relations_list2)
            else:
                print("------False negative, MULTI---------------")
                print(sentence, judgement, our_judgement_set)
                print(relations_list1, relations_list2)
                for graph in candidate_graphs_multi:
                    print(nx.density(graph))
                    print(analyze_errors(graph, relation_tuple))
                fn+=1
        else:
            if "y" in our_judgement_set:
                fp+=1
            else:
                tn+=1
    
    #fill test_dict object with stats
    #print("tp ",tp, " tn ",tn," fn ",fn," fp ", fp)
    #print("\n precision: "+str(tp/(tp+fp)))
    #print("\n recall: "+str(tp/(tp+fn)))
    #if tp+tn+fn+fp!=total:
        #print("somehting went wrong with the counting")
    #with open("/disk/scratch_big/sweber/GraphAlignment2/testResultsMulti2/"+str(lambda_value)+'.txt', 'w') as f:
        #f.write("\n"+str(lambda_value))
        ##f.write("\n tp "+str(tp)+" tn "+str(tn)+" fn "+str(fn)+" fp "+str(fp))
        #f.write("\n precision: "+str(tp/(tp+fp)))
        #f.write("\n recall: "+str(tp/(tp+fn)))
    #f.close()
    #return test_dict
def debug_test_2(lambda_list,sentence_to_relations_dict,graphs_file_path_de, graphs_file_path_multi):

    total=0
    tp=0
    tn=0
    fp=0
    fn=0
    
    for sentence in sentence_to_relations_dict:
        relation_dict=sentence_to_relations_dict[sentence]
        judgement=relation_dict["judgement"]
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
        candidate_graphs_de={}
        candidate_graphs_multi={}
        for lam in lambda_list:
            graph_dict_de=get_graphs_for_lambda(lam,graphs_file_path_de)
            graph_dict_multi=get_graphs_for_lambda_multi(lam,graphs_file_path_multi)
            for type_pair in types_set:
                try:
                    candidate_graphs_de[type_pair]=graph_dict_de[type_pair]
                    candidate_graphs_multi[type_pair]=graph_dict_multi[type_pair]
                except KeyError:
                    candidate_graphs_de[type_pair]=graph_dict_de["thing#thing"]
                    candidate_graphs_multi[type_pair]=graph_dict_multi["thing#thing"]                                    
                    continue
            #get all combinations of relations
            our_judgement_set=set()
            both_in_graph_set=set()
            if "noRelation" in relations_list1:
                relations_list1.remove("noRelation")
            if "noRelation" in relations_list2:
                relations_list2.remove("noRelation")
            all_possible_combinations_of_relations= [(x,y) for x in relations_list1 for y in relations_list2]
            for type_pair, graph in candidate_graphs_de.items():
                for relation_tuple in all_possible_combinations_of_relations:
                    both_in_graph,our_judgement=find_entailment(graph, relation_tuple)
                    our_judgement_set.add(our_judgement)
                    both_in_graph_set.add(both_in_graph)
            #if none of the candidates in same graph, check all the other graphs too
            if True not in both_in_graph_set:
                for type_pair,graph in graph_dict_de.items():
                    for relation_tuple in all_possible_combinations_of_relations:
                        both_in_graph,our_judgement=find_entailment(graph, relation_tuple)
            #compare our judgement with annotation
               
            if judgement=="y":
                if "y" in our_judgement_set:
                    tp+=1
                    #print("-----------------True positive-----------------")
                    #print(sentence, relations_list1, relations_list2)
                else:
                    if True in both_in_graph_set:
                        print("------False negative, DE"+str(lam)+"---------------")
                        print(sentence, judgement, our_judgement_set)
                        print(relations_list1, relations_list2)
                        for type_pair , graph in candidate_graphs_de.items():
                            both_in_graph, our_judgement=analyze_errors(graph, relation_tuple)
                            if both_in_graph:
                                print("both in ",lam,type_pair)
                                print(nx.density(graph))
                    fn+=1
            else:
                if "y" in our_judgement_set:
                    fp+=1
                else:
                    tn+=1
        
            for type_pair, graph in candidate_graphs_multi.items():
                for relation_tuple in all_possible_combinations_of_relations:
                    both_in_graph,our_judgement=find_entailment(graph, relation_tuple)
                    our_judgement_set.add(our_judgement)
                    both_in_graph_set.add(both_in_graph)
            #if none of the candidates in same graph, check all the other graphs too
            if True not in both_in_graph_set:
                for type_pair,graph in graph_dict_multi.items():
                    for relation_tuple in all_possible_combinations_of_relations:
                        both_in_graph,our_judgement=find_entailment(graph, relation_tuple)
            #compare our judgement with annotation
               
            if judgement=="y":
                if "y" in our_judgement_set:
                    tp+=1
                    #print("-----------------True positive-----------------")
                    #print(sentence, relations_list1, relations_list2)
                else:
                    if True in both_in_graph_set:
                        print("------False negative, MULTI"+str(lam)+"---------------")
                        print(sentence, judgement, our_judgement_set)
                        print(relations_list1, relations_list2)
                        for type_pair, graph in candidate_graphs_multi.items():
                            both_in_graph, our_judgement=analyze_errors(graph, relation_tuple)
                            if both_in_graph:
                                print("both in ",lam,type_pair)
                                print(nx.density(graph))
                    fn+=1
            else:
                if "y" in our_judgement_set:
                    fp+=1
                else:
                    tn+=1
                    
def test(sentence_to_relations_dict,lambda_value,graphs_file_path, language_flag):
    #test_dict=Test_dict(lambda_value)
    if language_flag=="german":
        graph_dict=get_graphs_for_lambda(lambda_value,graphs_file_path)
    elif language_flag=="multi":
        graph_dict=get_graphs_for_lambda_multi(lambda_value,graphs_file_path)
        if graph_dict=={}:
            print("something is wrong dict building")
    elif language_flag=="translated":
        graph_dict=get_graphs_for_lambda_translated(lambda_value,graphs_file_path)
        if graph_dict=={}:
            print("something is wrong dict building")
    elif language_flag=="trans_comb":
        graph_dict=get_graphs_for_lambda_trans_comb(lambda_value,graphs_file_path)
        if graph_dict=={}:
            print("something is wrong dict building")
        
    total=0
    tp=0
    tn=0
    fp=0
    fn=0
    #not_in_graph_count=0
    print(len(sentence_to_relations_dict.keys()))
    for sentence in sentence_to_relations_dict:
        relation_dict=sentence_to_relations_dict[sentence]
        judgement=relation_dict["judgement"]
        #print(judgement)
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
        """
        if True not in both_in_graph_set:
            not_in_graph_count+=1
            print(not_in_graph_count)
        """    
        
        if True not in both_in_graph_set:
            continue
        else:
            if judgement=="y":
                if "y" in our_judgement_set:
                    tp+=1
                    #print("-----------------True positive-----------------")
                    #print(sentence, relations_list1, relations_list2)
                else:
                    #print("------False negative---------------")
                    #print(sentence, judgement, our_judgement_set)
                    #print(relations_list1, relations_list2)
                    #print(analyze_errors(graph, relation_tuple))
                    fn+=1
            else:
                if "y" in our_judgement_set:
                    fp+=1
                else:
                    tn+=1
            total+=1
        
    #fill test_dict object with stats
    print("tp ",tp, " tn ",tn," fn ",fn," fp ", fp)
    print("\n precision: "+str(tp/(tp+fp)))
    print("\n recall: "+str(tp/(tp+fn)))
    if tp+tn+fn+fp!=total:
        print("somehting went wrong with the counting")
    #print(not_in_graph_count)
    with open("/disk/scratch_big/sweber/GraphAlignment2/testResults/MultiHighDensity/"+str(lambda_value)+'.txt', 'w') as f:
        f.write("\n"+str(lambda_value))
        f.write("\n tp "+str(tp)+" tn "+str(tn)+" fn "+str(fn)+" fp "+str(fp))
        f.write("\n precision: "+str(tp/(tp+fp)))
        f.write("\n recall: "+str(tp/(tp+fn)))
        f.write("\n total: "+str(total))
    f.close()
    #return test_dict


if __name__ == '__main__':
    
    #parallel -j72 python test.py ::: 0.015 0.025 0.035 0.045 0.055 0.065 0.075 0.085 0.0125 0.0225 0.0325 0.0425 0.0525 0.0625 0.0725 0.0825 0.0175 0.0275 0.0375 0.0475 0.0575 0.0675 0.0775 0.0875 0.0999
    #parallel -j35 python test.py ::: 0.15 0.25 0.34 0.44 0.55 0.64 0.75 0.85 0.12 0.22 0.32 0.42 0.52 0.62 0.72 0.82 0.17 0.27 0.37 0.47 0.57 0.67 0.77 0.87 0.99
    #parallel -j72 python test.py ::: 0.0049 0.0099 0.015 0.025 0.03 0.035 0.04 0.045 0.59 0.5 0.1
    lam=sys.argv[1]
    #lambda_list=[ 0.15, 0.25, 0.34, 0.44]
    #lam=0.1
    sentence_to_relation_dict = pickle.load( open( "relation_dict2.pickle", "rb" ) )
    test_dict=test(sentence_to_relation_dict,lam,"/disk/scratch_big/sweber/GraphAlignment2/multilingual_graphs_highest/","multi")
