# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 14:37:24 2020

@author: Sabine
"""
import networkx as nx
import collections
import re
import pickle
import os
import sys

def get_string_from_relation(relation):
    if "NEG" in relation:
        result=re.search('NEG__\((.*)\.2\)', relation)
        if result!= None:
            return "NEG__"+result.group(1)
        else:
            return "noRelation"
    else:
        result = re.search('\((.*)\.2\)', relation)
        if result!= None:
            return result.group(1)
        else:
            return "noRelation"
    

def get_type_pair_from_relation(relation):
    result = re.search('\#(.*)::.*::', relation)
    if result!= None:
        return result.group(1)
    else:
        return "noType"
        
#taken from stackexchange
def edit_distance(s1, s2):
    m=len(s1)+1
    n=len(s2)+1

    tbl = {}
    for i in range(m): tbl[i,0]=i
    for j in range(n): tbl[0,j]=j
    for i in range(1, m):
        for j in range(1, n):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            tbl[i,j] = min(tbl[i, j-1]+1, tbl[i-1, j]+1, tbl[i-1, j-1]+cost)

    return tbl[i,j]

def find_right_sentence(sentence_to_relations_dict,sent):
    right_key=""
    for key in sentence_to_relations_dict.keys():
        ed_dist=edit_distance(key,sent)
        #print(ed_dist)
        if ed_dist<=4:
            right_key=key
            return right_key
        

def parse_rel_ex_output_to_sentence_relation_dict(filename_rel,filename_data):
    
    sent_to_rels_dict={}
    external_dict={}
    
    sentence=""
    relation={}
    relation_list=[]
    sentence_counter=0
    with open(filename_rel, 'r') as inF:
        for line in inF:
            if "line: " in line:
                relation_list=[]
                sentence=line[6:].lower().rstrip()
                sentence=sentence[:-2]
                sentence_counter+=1
            elif line[0]=="(":
                type_pair=get_type_pair_from_relation(line)
                relation=get_string_from_relation(line)
                relation_list.append((relation,type_pair))
            elif not line.strip():
                if sentence in sent_to_rels_dict.keys():
                    rel=sent_to_rels_dict[sentence]
                    for res in relation_list:
                        if res not in rel:
                            rel.append((relation,type_pair))
                    sent_to_rels_dict[sentence]=rel
                else:
                    sent_to_rels_dict[sentence]= relation_list
    print("done first bit")                
    with open(filename_data, 'r') as inF:
        for line in inF:
            line=line.rstrip()
            line=line.split(". ")
            if len(line)<3:
                continue
            sent1=line[0].lower()
            sent2=line[1].lower()
            #sent2=sent2[:-1]
            judgement=line[2]
            if sent1 not in sent_to_rels_dict.keys():
                try:
                    right_key1=find_right_sentence(sent_to_rels_dict,sent1)
                    relation_list1=sent_to_rels_dict[right_key1]
                except KeyError:
                    print(sent1)
                    relation_list1=[("NoRelation","NoType")]
            else:
                relation_list1=sent_to_rels_dict[sent1]
            if sent2 not in sent_to_rels_dict.keys():
                try:
                    right_key2=find_right_sentence(sent_to_rels_dict,sent2)
                    relation_list2=sent_to_rels_dict[right_key2]
                except KeyError:
                    print(sent2)
                    relation_list2=[("NoRelation","NoType")]
            else:
                relation_list2=sent_to_rels_dict[sent2]
            internal_dict={"rel1":relation_list1,
                            "rel2":relation_list2,
                            "judgement":judgement}
            external_dict[sent1+". "+sent2]=internal_dict
                         
    pickle.dump(external_dict, open("relation_dict2.pickle", "wb" ) )           
    return external_dict

def make_one_graph_from_all_in_folder(lambda_value,folder_path,name):
    home_path=folder_path+"/"
    graph_list=[]
    old_component_count=0
    for filename in os.listdir(folder_path):
        try:
            graph,new_component_count=constructGraphFromFile_multi(home_path+filename,lambda_value,old_component_count)
        except TypeError:
            print("type error in ",lambda_value,filename)
            continue
        graph_list.append(graph)
        old_component_count=new_component_count
        #print(filename,old_component_count)
    merged_graph=nx.DiGraph()
    for graph in graph_list:
        merged_graph_n=nx.compose(merged_graph,graph)
        merged_graph=merged_graph_n
        #get_the_stats(merged_graph)
    pickle.dump(merged_graph, open("/disk/scratch_big/sweber/GraphAlignment2/mergedGraphPickles/"+name+"/merged_graph"+name+str(lambda_value)+".pickle", "wb" ) ) 
    return merged_graph

def constructGraphFromFile_multi(filename,lambda_value,old_component_count):
    G = nx.DiGraph()
    passedComponent=False
    passedRightLambda=False

    with open(filename, 'r') as inF:
            number=-100
            for line in inF:
                if "lambda: "+str(lambda_value) in line:
                    G = nx.DiGraph()
                    passedComponent=False
                    passedRightLambda=True
                    splits=line.split(" ")
                    count=int(splits[3])
                    component_count=old_component_count+count
                    continue
                #elif ("lambda" in line and passedRightLambda) or ("writing Done"in line):
                elif ("lambda" in line and passedRightLambda):
                    return G, component_count
                elif "component" in line and passedRightLambda:
                    passedComponent=True
                    line=line.rstrip()
                    lineSplit=line.split()
                    try:
                        number=int(lineSplit[1])
                        number+=old_component_count
                    except IndexError:
                        print("format error in graph file")
                        continue
                    G.add_node(number)
                elif "component" not in line and passedComponent and line!="" and "=>" not in line and passedRightLambda:
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
    

def constructGraphFromFile(filename, lambda_value):
    G = nx.DiGraph()
    counter=0
    passedComponent=False
    passedRightLambda=False

    with open(filename, 'r') as inF:
            number=-100
            for line in inF:
                if "lambda: "+str(lambda_value) in line:
                    G = nx.DiGraph()
                    passedComponent=False
                    passedRightLambda=True
                    continue
                #elif ("lambda" in line and passedRightLambda) or ("writing Done"in line):
                elif ("lambda" in line and passedRightLambda):
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
if __name__ == '__main__':
    #german_lambda_list=[0.015, 0.025, 0.035, 0.045, 0.055, 0.065, 0.075, 0.085, 0.0125, 0.0225, 0.0325, 0.0425, 0.0525, 0.0625, 0.0725, 0.0825, 0.0175, 0.0275, 0.0375, 0.0475, 0.0575, 0.0675, 0.0775, 0.0875, 0.0999]
    #lam=sys.argv[1]
    #parallel -j72 python test.py ::: 0.0049 0.0099 0.015 0.025 0.03 0.035 0.04 0.045 0.59 0.5 0.1
    lam=0.025
    for filename in os.listdir("/disk/scratch_big/sweber/GraphAlignment2/justGraphsLowLPickles/"):
        for filenameEn in os.listdir("/disk/scratch_big/sweber/GraphAlignment2/translatedGraphsEnDe/"):
            if str(lam) in filename and str(lam) in filenameEn:
                deGraph=pickle.load(open("/disk/scratch_big/sweber/GraphAlignment2/justGraphsLowLPickles/"+filename,"rb"))
                enGraph=pickle.load(open("/disk/scratch_big/sweber/GraphAlignment2/translatedGraphsEnDe/"+filenameEn,"rb"))
                deLenght=len(deGraph)
                mapping={}
                for n in enGraph.nodes():
                    mapping[n]=n+deLenght
                newGraph=nx.relabel_nodes(enGraph,mapping)
                combinedGraph=nx.compose(deGraph,newGraph)
                pickle.dump(combinedGraph,open("/disk/scratch_big/sweber/GraphAlignment2/combinedDeEnTranslated/"+filename,"wb"))
