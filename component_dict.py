# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 12:18:27 2020

@author: Sabine
"""
import re
import io
import numpy as np

class Component_dict:
    
    def __init__(self, de_graph_txt, en_graph_txt, de_vectors_txt, en_vectors_txt, number_of_nearest_neighbors):
        component_to_string_list_dict_de, string_to_component_list_dict_de=self.parse_graph_from_txt(de_graph_txt)
        component_to_string_list_dict_en, string_to_component_list_dict_en=self.parse_graph_from_txt(en_graph_txt)
        self.component_to_string_list_dict_de=component_to_string_list_dict_de
        self.component_to_string_list_dict_en=component_to_string_list_dict_en
        self.string_to_component_list_dict_de=string_to_component_list_dict_de
        self.string_to_component_list_dict_en=string_to_component_list_dict_en
        
        nmax = 50000  # maximum number of word embeddings to load
        src_embeddings, src_id2word, src_word2id = self.load_vec(de_vectors_txt, nmax)
        tgt_embeddings, tgt_id2word, tgt_word2id = self.load_vec(en_vectors_txt, nmax)
        de_word_en_components_dict=self.generate_de_word_to_en_components_dict(
                string_to_component_list_dict_de, string_to_component_list_dict_en,
                src_embeddings,src_id2word,
                tgt_embeddings, tgt_id2word, 
                number_of_nearest_neighbors)
        de_en_component_dict =self.generate_de_component_to_en_component_list_dict(component_to_string_list_dict_de,de_word_en_components_dict)
        self.de_en_component_dict=de_en_component_dict
        self.en_de_component_dict =self.generate_en_component_to_de_components_list_dict(de_en_component_dict)
        
    def get_keys_de_en(self):
        return self.de_en_component_dict.keys()
    
    def get_keys_en_de(self):
        return self.en_de_component_dict.keys()
    
    def get_node_de_en(self,node):
        if node in self.de_en_component_dict:
            return self.de_en_component_dict[node]
        else:
            return None
    
    def get_node_en_de(self,node):
        if node in self.en_de_component_dict:
            return self.en_de_component_dict[node]
        else:
            return None
        
    def generate_en_component_to_de_components_list_dict(self,de_en_component_dict):
        en_de_component_dict={}
        for de_component, en_component_list in de_en_component_dict.items():
            for component in en_component_list:
                if component in en_de_component_dict:
                    new_list=en_de_component_dict[component]
                    new_list.append(de_component)
                    en_de_component_dict[component]=new_list
                else:
                    en_de_component_dict[component]=[de_component]
        return en_de_component_dict       
        
    def generate_de_component_to_en_component_list_dict(self,component_to_string_list_dict_de,de_word_en_components_dict):
        de_component_to_en_component_list_dict={}
        for component, string_list in component_to_string_list_dict_de.items():
            en_component_list=[]
            for string in string_list:
                if string in de_word_en_components_dict:
                    en_component_list.extend(de_word_en_components_dict[string])
            de_component_to_en_component_list_dict[component]=list(set(en_component_list))
        return de_component_to_en_component_list_dict
        
    def generate_de_word_to_en_components_dict(self,string_to_component_list_dict_de, string_to_component_list_dict_en,
                                src_embeddings,src_id2word,
                                tgt_embeddings, tgt_id2word, number_of_nearest_neighbors):
        de_word_en_components_dict={}
        for string in  string_to_component_list_dict_de.keys():
            if "_" not in string:
                k_best=self.get_nn(string, src_embeddings, src_id2word, tgt_embeddings, tgt_id2word, number_of_nearest_neighbors)
                en_component_list=[]
                for word in k_best:
                    if word in string_to_component_list_dict_en:
                        en_component_list.extend(string_to_component_list_dict_en[word])
                de_word_en_components_dict[string]=en_component_list
        return de_word_en_components_dict
        
    def load_vec(self,emb_path, nmax=50000):
        vectors = []
        word2id = {}
        with io.open(emb_path, 'r', encoding='utf-8', newline='\n', errors='ignore') as f:
            next(f)
            for i, line in enumerate(f):
                word, vect = line.rstrip().split(' ', 1)
                vect = np.fromstring(vect, sep=' ')
                assert word not in word2id, 'word found twice'
                vectors.append(vect)
                word2id[word] = len(word2id)
                if len(word2id) == nmax:
                    break
        id2word = {v: k for k, v in word2id.items()}
        embeddings = np.vstack(vectors)
        return embeddings, id2word, word2id
    
    def get_nn(self,word, src_emb, src_id2word, tgt_emb, tgt_id2word, K=5):
        #print("Nearest neighbors of \"%s\":" % word)
        word2id = {v: k for k, v in src_id2word.items()}
        try:
            word_emb = src_emb[word2id[word]]
        except KeyError:
            return "out of vocabulary"
        scores = (tgt_emb / np.linalg.norm(tgt_emb, 2, 1)[:, None]).dot(word_emb / np.linalg.norm(word_emb))
        k_best = scores.argsort()[-K:][::-1]
        ret_best=[]
        for i, idx in enumerate(k_best):
            #print('%.4f - %s' % (scores[idx], tgt_id2word[idx]))
            ret_best.append(tgt_id2word[idx])
        return ret_best
    
    def parse_graph_from_txt(self,filename):
        passedComponent=False
        passedRightLambda=False
        component_to_string_list_dict={}
        string_to_component_list_dict={}
        component_number=-100
    
        with io.open(filename, 'r', encoding='utf-8', newline='\n', errors='ignore') as inF:
                number=-100
                for line in inF:
                    if "lambda" in line:
                        passedComponent=False
                        passedRightLambda=True
                        continue
                    elif "writing Done" in line and passedRightLambda:
                        return component_to_string_list_dict, string_to_component_list_dict
                    elif "component " in line and passedRightLambda:
                        #print(line)
                        passedComponent=True
                        line=line.rstrip()
                        lineSplit=line.split()
                        number=int(lineSplit[1])
                        component_number=number
                        string_list=[]
                    elif "component " not in line and "(" in line and passedComponent and line!="" and "=>" not in line and passedRightLambda:
                        #print(line)
                        try:
                            first_verb=re.search(r'\((.*?)\.1', line).group(1)
                        except AttributeError:
                            try:
                                first_verb=re.search(r'\((.*?)\.2', line).group(1)
                            except:
                                first_verb="None"
                        string_list.append(first_verb)
                        if component_number!=-100:
                            component_to_string_list_dict[component_number]=string_list
                        if first_verb in string_to_component_list_dict:
                            component_list=string_to_component_list_dict[first_verb]
                            component_list.append(component_number)
                            string_to_component_list_dict[first_verb]=component_list
                        else:
                            string_to_component_list_dict[first_verb]=[component_number]
                    elif line=="":
                        passedComponent=False
