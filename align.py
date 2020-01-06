# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 11:11:13 2020

@author: Sabine
"""
from component_dict import Component_dict
import parse_to_graph

def align(de_graph,en_graph,de_en_alignment_dict,en_de_alignment_dict):
     multi_graph=[]
     return multi_graph
    
if __name__ == '__main__':
    print("huphup")
    G=parse_to_graph.constructGraphFromFile("persLoc0150de.txt")
    parse_to_graph.get_the_stats(G)
    print("noo")
    #create the alignment dictionaries
    #comp_dict=Component_dict("persLoc0150de.txt", "persLoc0150.txt", "vectors-de.txt", "vectors-en.txt", 5)
    #parse graphs from text files
    #feed them to the alignment