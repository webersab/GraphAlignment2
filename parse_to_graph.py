# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 14:37:24 2020

@author: Sabine
"""
import networkx as nx
import collections
import re

def get_type_pair_from_relation(relation):
    result = re.search('\#(.*)::.*::', relation)
    if result!= None:
        return result.group(1)
    else:
        return "noType"

def parse_rel_ex_output_to_sentence_relation_dict(filename, levi_text):
    sentence_set=set()
    with open(levi_text, 'r') as inF:
        for line in inF:
            line=line.strip().split(". ")
            for l in line:
                sentence_set.add(l.lower())
    print(len(sentence_set))
    #print(sentence_set)
    
    sent_to_rels_dict={}
    sentence=""
    relation={}
    sentence_counter=0
    with open(filename, 'r') as inF:
        for line in inF:
            if "line: " in line:
                sentence=line[6:].lower().rstrip()
                sentence=sentence[:-2]
                sentence_counter+=1
                #print(sentence)
                if sentence in sentence_set:
                    sentence_set.remove(sentence)
            elif line[0]=="(":
                type_pair=get_type_pair_from_relation(line)
                relation=line
                relation_dict={relation:type_pair}
            elif not line.strip():
                if sentence in sent_to_rels_dict.keys():
                    rel=sent_to_rels_dict[sentence]
                    if relation not in rel.keys():
                        rel[relation]=type_pair
                    sent_to_rels_dict[sentence]=rel
                else:
                    sent_to_rels_dict[sentence]= relation_dict         
    print(len(sentence_set))
    print(sentence_set)
    return sent_to_rels_dict

def constructGraphFromFile(filename):
    G = nx.DiGraph()
    counter=0
    passedComponent=False
    passedRightLambda=False

    with open(filename, 'r') as inF:
            number=-100
            for line in inF:
                if "lambda" in line:
                    G = nx.DiGraph()
                    passedComponent=False
                    passedRightLambda=True
                    continue
                elif "writing Done" in line and passedRightLambda:
                    #E=nx.connected_components(G)
                    return G
                elif "component" in line and passedRightLambda:
                    passedComponent=True
                    line=line.rstrip()
                    lineSplit=line.split()
                    try:
                        number=int(lineSplit[1])
                    except IndexError:
                        print("format error in graph file")
                        continue
                    G.add_node(number)
                elif "component" not in line and passedComponent and line!="" and "=>" not in line and passedRightLambda:
                    counter+=1
                    if line!="\n" and number!=-100:
                        try:
                            old_line=G.node[number]["verb"]
                            G.node[number]["verb"]=line+" "+old_line
                        except KeyError:
                           G.node[number]["verb"]=line
                elif "component" not in line and passedComponent and line!="" and "=>" in line and passedRightLambda:
                    line=line.rstrip()
                    lineSplit=line.split()
                    component=int(lineSplit[1])
                    #G.add_edge(number, component)
                    #print("added edge between ", component, number)
                    G.add_edge(component, number)
                elif line=="":
                    passedComponent=False
                    
def get_the_stats(G): 
    print("Total number of nodes: ", int(G.number_of_nodes())) 
    print("Total number of edges: ", int(G.number_of_edges())) 
    #print("List of all nodes: ", list(G.nodes())) 
    #print("List of all edges: ", list(G.edges(data = True))) 
    degree_dict={}
    for node in G.nodes():
        degree=G.degree[node]
        if degree in degree_dict.keys():
            degree_dict[degree]+=1
        else:
            degree_dict[degree]=1
    od = collections.OrderedDict(sorted(degree_dict.items()))
    print("Degree for all nodes: ", od) 
    nuG=G.to_undirected()
    print("Number of connected components: ", nx.number_connected_components(nuG))

    #print("Total number of self-loops: ", int(G.number_of_selfloops())) 
    print("List of all nodes with self-loops: ", 
                 list(G.nodes_with_selfloops())) 

    #print("List of all nodes we can go to in a single step from node 2: ", 
                                                     #list(G.neigh
#if __name__ == '__main__':
    #sent_to_rels_dict=parse_rel_ex_output_to_sentence_relation_dict("Levy_relations.txt")
    #print(sent_to_rels_dict)