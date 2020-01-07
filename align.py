# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 11:11:13 2020

@author: Sabine
"""
from component_dict import Component_dict
import parse_to_graph
import copy


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
                    print("key error")
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
    #%%    
if __name__ == '__main__':

    print("huphup")
    G=parse_to_graph.constructGraphFromFile("persLoc0150de.txt")
    #parse_to_graph.get_the_stats(G)
    H=parse_to_graph.constructGraphFromFile("persLoc0150.txt")
    #parse_to_graph.get_the_stats(H)
    print("noo")
    #%%
    #create the alignment dictionaries
    comp_dict=Component_dict("persLoc0150de.txt", "persLoc0150.txt", "vectors-de.txt", "vectors-en.txt", 5)
    print("tutut")
    #%%
    #feed them to the alignment
    multi_graph=align(G,H,comp_dict)
    #parse_to_graph.get_the_stats(multi_graph)
    #%%
    import parse_to_graph
    #for node in multi_graph.nodes():
        #print("AA" , node, multi_graph.node[node]["verb"])
    print("---------------------DE--------------")
    parse_to_graph.get_the_stats(G)
    print("---------------------EN------------------------")
    parse_to_graph.get_the_stats(H)
    print("-------------------------multi-----------------")
    parse_to_graph.get_the_stats(multi_graph)