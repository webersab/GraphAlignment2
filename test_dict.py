#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 14:35:47 2020

@author: s1782911
"""

#def get_graph_by_type_and_lambda(type_pair,lambda):
#return graph

class Test_dict:
    def __init__(self,lambda_value):
        self.lambda_value=lambda_value
        self.stats_dict={}
        self.true_pos_dict={}
        self.false_pos_dict={}
        self.false_neg_dict={}

# write getters and setters for this