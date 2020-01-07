# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 14:37:24 2020

@author: Sabine
"""
import networkx as nx
import collections

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
                                                     #list(G.neighbors(2))) 