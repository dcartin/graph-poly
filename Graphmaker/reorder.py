# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 07:55:05 2020

@author: cartin
"""

def reorder(pd_list):
    """
    Creates a sorted list of all edge labels
    currently in the PD list, and relabels them
    to use all numbers from 1 to 2N, for N the
    number of nodes in the graph.
    """
    
    label_list = sorted(list(set([label for node in pd_list for label in node])))
    
    return [[label_list.index(node[iii]) + 1 for iii in range(4)] for node in pd_list]