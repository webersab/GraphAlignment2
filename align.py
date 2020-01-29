# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 11:11:13 2020

@author: Sabine
"""
from component_dict import Component_dict
import parse_to_graph
import copy
import pickle
import networkx as nx
import os
import sys


def align(de_graph,en_graph,comp_dict):
    #de_en_alignment_dict=comp_dict.de_en_component_dict
    #en_de_alignment_dict=comp_dict.de_en_component_dict
    #step 1, node alignment
    multi_graph=copy.deepcopy(de_graph)
    list_of_added_english_nodes=[]
    
    for node in de_graph.nodes():
        if node in comp_dict.get_keys_de_en():
            for comp in comp_dict.get_node_de_en(node):
                aligned_node_of_en=comp
                list_of_added_english_nodes.append(aligned_node_of_en)
                #merge nodes in new graph
                try:
                    english_verbs=en_graph.node[aligned_node_of_en]["verb"]
                except KeyError:
                    #print("key error a")
                    english_verbs=""
                multi_graph.node[node]["verb"]+=" "+english_verbs
    #step 2, adding missing nodes and edges from english graph
    new_node_number=de_graph.number_of_nodes()+1
    for node in en_graph.nodes():
        if node not in list_of_added_english_nodes:
            new_component_number=new_node_number
            new_node_number+=1
            multi_graph.add_node(new_component_number)
            try:
                multi_graph.node[new_component_number]["verb"]=en_graph.node[node]["verb"]
            except KeyError:
                print("key error ",node)
            list_of_added_english_nodes.append(node)
        neighbors_nodes=en_graph.neighbors(node)
        for neighbour in neighbors_nodes:
            if node not in list_of_added_english_nodes and neighbour not in list_of_added_english_nodes:
                multi_graph.add_node(new_node_number)
                multi_graph.node[new_node_number]["verb"]=en_graph.node[neighbour]["verb"]
                multi_graph.add_edge(new_component_number, new_node_number)
                new_node_number+=1
                list_of_added_english_nodes.append(neighbour)
            elif node in list_of_added_english_nodes and neighbour not in list_of_added_english_nodes:
                corresponding_German_nodes=comp_dict.get_node_en_de(node)
                if corresponding_German_nodes!=None:
                    multi_graph.add_node(new_node_number)
                    multi_graph.node[new_node_number]["verb"]=en_graph.node[neighbour]["verb"]
                    new_node_number+=1
                    for nds in corresponding_German_nodes:
                        multi_graph.add_edge(nds, new_node_number)
                list_of_added_english_nodes.append(neighbour)
    return multi_graph

def find_english_graph_with_similar_density(german_graph,english_graph_directory):
    density=nx.density(german_graph)
    min_difference=100
    chosen_graph=None
    graph_name=""
    for filename in os.listdir(english_graph_directory):
        graph=pickle.load(open(english_graph_directory+filename,"rb"))
        english_density=nx.density(graph)
        if english_density==0:
            continue
        difference=abs(english_density-density)
        if difference<min_difference:
            min_difference=difference
            chosen_graph=graph
            graph_name=english_graph_directory+filename
                
    return chosen_graph, graph_name

def find_english_graph_with_highest_density(german_graph,english_graph_directory):
    max_density=0
    chosen_graph=None
    graph_name=""
    for filename in os.listdir(english_graph_directory):
        graph=pickle.load(open(english_graph_directory+filename,"rb"))
        english_density=nx.density(graph)
        if english_density==0:
            continue
        if english_density>max_density:
            max_density=english_density
            chosen_graph=graph
            graph_name=english_graph_directory+filename
    return chosen_graph, graph_name

def align_all_german_to_english(german_input_folder,english_input_folder,lam, output_folder, densityMatch="equal"):
    #list_of_missing=["LOCATION#EVENT","ORGANIZATION#EVENT","ORGANIZATION#ORGANIZATION","ORGANIZATION#PERSON","PERSON#LOCATION"]
    for filename in os.listdir(german_input_folder):
    #for filename in list_of_missing:
        print("processing " , filename,lam)
        G=parse_to_graph.constructGraphFromFile(german_input_folder+filename, lam)
        if G == None:
            print("g is none")
            continue
        if nx.density(G)==0:
            print(filename, lam)
            continue
        type_pair=filename.lower()
        if "thing" in type_pair:
            type_pair=type_pair.replace("thing","misc")
        if type_pair not in os.listdir(english_input_folder):
            pair=type_pair.split("#")
            type_pair=pair[1]+"#"+pair[0]
        if densityMatch=="equal":
            H, H_filename=find_english_graph_with_similar_density(G,english_input_folder+type_pair+"/")
        elif densityMatch=="highest":
            H, H_filename=find_english_graph_with_highest_density(G,english_input_folder+type_pair+"/")
        print("pairing with ",H_filename)
        #This is where we need do create a new comp dict!!
        comp_dict=Component_dict(german_input_folder+filename, H_filename, "vectors-de.txt", "vectors-en.txt", 5)
        print("done building comp dict")
        multi_graph=align(G,H,comp_dict)
        print("done aligning")
        pickle.dump(multi_graph, open(output_folder+filename+str(lam)+".pickle", "wb" ) ) 
        print("de density: ",nx.density(G),"en density: ",nx.density(H),"mul density: ",nx.density(multi_graph))
        print("Pickled ",filename+str(lam))
    return None

def translate_english_graph_to_german(english_graph, verctors_de, vectors_en, number_of_nearest_neighbors):

    return None
   
if __name__ == '__main__':
    #graph=pickle.load(open("/disk/scratch_big/sweber/GraphAlignment2/mergedGraphPickles/event#misc/merged_graphEvent#Misc0.059.pickle", "rb" ))
    #for n in graph.nodes():
        #print("-------------")
        #print(n)
        #print(graph.nodes[n])                       
    #comp_dict=pickle.load(open("comp_dict.pickle", "rb" ))
    #print(comp_dict.component_to_string_list_dict_de)
    #create the alignment dictionaries
    #comp_dict=Component_dict("persLoc0150de.txt", "persLoc0150.txt", "vectors-de.txt", "vectors-en.txt", 5)
    #pickle.dump(comp_dict, open("comp_dict.pickle", "wb" ) )
    #print("tutut")
    german_lambda_list=[0.15,0.25,0.34,0.44,0.55,0.64,0.75,0.85,0.12,0.22,0.32,0.42,0.52,0.62,0.72,0.82,0.17,
                        0.27,0.37,0.47,0.57,0.67,0.77,0.87,0.99]
    german_lambda=sys.argv[1]
    #german_lambda_list=[0.015, 0.025, 0.035, 0.045, 0.055, 0.065, 0.075, 0.085, 0.0125, 0.0225, 0.0325, 0.0425, 0.0525, 0.0625, 0.0725, 0.0825, 0.0175, 0.0275, 0.0375, 0.0475, 0.0575, 0.0675, 0.0775, 0.0875, 0.0999]
    align_all_german_to_english("/disk/scratch_big/sweber/GraphAlignment2/justGraphsHighL/","/disk/scratch_big/sweber/GraphAlignment2/mergedGraphPickles/",german_lambda, "/disk/scratch_big/sweber/GraphAlignment2/multilingual_graphs/")